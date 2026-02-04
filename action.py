import csv
import os
import sys
import re
import wx
from kipy import KiCad
from kipy.board import BoardLayer, BoardOriginType
from kipy.board_types import Field
from kipy.geometry import Vector2
from kipy.proto.board.board_types_pb2 import FootprintMountingStyle
from gui import ComponentPositionDialog
from version import version

class ComponentPosition(ComponentPositionDialog):
    def __init__(self):
        ComponentPositionDialog.__init__(self, None)
        self.SetTitle('Component Position Exporter v%s' % version)
        
        self.kicad = None
        self.board = None
        self.footprints = []
        self.fields = []
        
        try:
            self.kicad = KiCad()
            self.board = self.kicad.get_board()
            
            # --- SORTING LOGIC ---
            def sort_key_logic(fp):
                # 1. Priority: DNP Status
                # getattr returns False if attribute is missing, True if it is DNP
                is_dnp = getattr(fp.attributes, 'do_not_populate', False)
                
                # 2. Priority: Reference Designator (Natural Sort)
                # Split "R10" into ['R', 10] to compare numerically rather than lexicographically
                ref_text = fp.reference_field.text.value
                # Split text and numbers
                natural_key = [int(text) if text.isdigit() else text.lower() 
                               for text in re.split(r'(\d+)', ref_text)]
                
                # Return tuple: (DNP status first, then Reference key)
                # Python compares the first element first (False < True), so non-DNP comes first
                return (is_dnp, natural_key)

            # Get list and sort immediately using the logic defined above
            self.footprints = sorted(
                self.board.get_footprints(), 
                key=sort_key_logic
            )
            # ---------------------
            
            self.basefilename = os.path.join(
                self.board.document.project.path,
                os.path.splitext(self.board.document.board_filename)[0],
            )

            self.textLog.WriteText(f"Connected to KiCad {self.kicad.get_version()}\n")
            self.textLog.WriteText(f"Opening file {self.board.document.board_filename}\n")
            
            print(f"Connected to KiCad {self.kicad.get_version()}")
            print(f"Opening file {self.board.document.board_filename}")

            self.get_field_name()
            self.add_data_file()
            
        except Exception as e:
            # Catch generic Exception to avoid catching SystemExit
            print(f"Not connected to KiCad: {e}")
            self.textLog.WriteText(f"Not connected to KiCad: {e}\n")
        
    def OnGenerate(self, event):
        self.textLog.WriteText("OnGenerate \n")
        if self.board:
            self.create_file()
        else:
            self.textLog.WriteText("Error: No board loaded.\n")

    def OnClear(self, event):
        self.textLog.WriteText("OnClear \n")
        self.textLog.Clear()
    
    def OnCopy(self, event):
        self.textLog.WriteText("OnCopy \n")
        data = wx.TextDataObject()
        data.SetText(self.textLog.GetValue())
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(data)
            wx.TheClipboard.Close()
        
    def get_field_name(self):
        """
        Scan all footprints to find unique field names.
        """
        unique_fields = set()
        for footprint in self.footprints:
            for item in footprint.definition.items:
                if isinstance(item, Field):
                    if item.name:
                        unique_fields.add(item.name)
        self.fields = sorted(list(unique_fields))
        print(f"Found fields: {self.fields}")
    
    def add_data_file(self):
        """
        Display the found fields in the GUI list.
        """
        self.dataFields.DeleteAllItems()
        for i, field in enumerate(self.fields, start=1):
            # Format: [Index, Checked(False), FieldName]
            self.dataFields.AppendItem([str(i), False, field])

    def create_file(self):
        project_path = self.board.document.project.path
        board_filename = os.path.splitext(self.board.document.board_filename)[0]
        output_filename = f"pos_{board_filename}.csv"
        assembly_dir = os.path.join(project_path, "assembly")
        if not os.path.exists(assembly_dir):
            os.makedirs(assembly_dir)
        csv_filepath = os.path.join(assembly_dir, output_filename)
        print(f"Writing to: {csv_filepath}")

        # 1. Collect selected Custom Fields
        # IMPORTANT: Reset this list every run to avoid duplicates
        selected_custom_fields = [] 
        COLUMN_ADD = 1
        COLUMN_NAME = 2
        
        # Iterate through GUI list to see which items are checked
        count = self.dataFields.GetItemCount()
        for i in range(count):
            if self.dataFields.GetToggleValue(i, COLUMN_ADD):
                field_name = self.dataFields.GetTextValue(i, COLUMN_NAME)
                selected_custom_fields.append(field_name)

        # 2. Setup CSV Headers
        headers = [
            'Item', 'References', 'Value', 'Footprint', 'Layer', 'Angle', 
            'PosX (mm)', 'PosY (mm)', 'PosX (mil)', 'PosY (mil)', 'SMD', 'DNP'
        ]

        # Check DNP Checkbox (Assuming True means "Hide DNP Column")
        skip_dnp_column = self.checkDNP.IsChecked()
        if skip_dnp_column:
            headers.remove("DNP")

        headers.extend(selected_custom_fields)

        # 3. Write Data
        try:
            # Use 'with' context manager for safer file handling
            with open(csv_filepath, 'w', encoding="utf-8", newline='') as f:
                out = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                out.writerow(headers)

                IU_PER_MM = 1000000.0
                IU_PER_MILS = 25400.0

                # Coordinate Settings
                origin_sel = self.radioOrigin.GetStringSelection()
                x_dir_sel = self.radioXAxis.GetStringSelection()
                y_dir_sel = self.radioYAxis.GetStringSelection()
                
                x_scale = -1 if x_dir_sel == "Increases left" else 1
                y_scale = -1 if y_dir_sel == "Increases up" else 1

                offset = Vector2.from_xy(0, 0)
                if origin_sel == 'Grid Origin':
                    offset = self.board.get_origin(BoardOriginType.BOT_GRID)
                elif origin_sel == 'Drill Origin':
                    offset = self.board.get_origin(BoardOriginType.BOT_DRILL)
                
                print(f"Origin: {origin_sel} @ {offset}")

                # Loop to write data (already sorted in __init__)
                for i, footprint in enumerate(self.footprints, start=1):
                    # Calculate positions
                    delta_x = footprint.position.x - offset.x
                    delta_y = footprint.position.y - offset.y

                    mmX = round((delta_x * x_scale) / IU_PER_MM, 4)
                    mmY = round((delta_y * y_scale) / IU_PER_MM, 4)
                    milX = round((delta_x * x_scale) / IU_PER_MILS, 4)
                    milY = round((delta_y * y_scale) / IU_PER_MILS, 4)

                    # Extract basic data
                    fp_name = footprint.definition.id.name
                    reference = footprint.reference_field.text.value
                    value = footprint.value_field.text.value
                    # Format rotation angle
                    angle = f"{footprint.orientation.degrees:.1f}" 
                    
                    smd = "Yes" if footprint.attributes.mounting_style == FootprintMountingStyle.FMS_SMD else "No"
                    layer = "Top" if footprint.layer == BoardLayer.BL_F_Cu else "Bottom"
                    
                    row = [i, reference, value, fp_name, layer, angle, mmX, mmY, milX, milY, smd]
                    
                    if not skip_dnp_column:
                        # Re-check DNP attribute to populate column
                        is_dnp = getattr(footprint.attributes, 'do_not_populate', False)
                        dnp_val = "Yes" if is_dnp else ""
                        row.append(dnp_val)

                    # Optimize Custom Field retrieval
                    # Create a dictionary map for current footprint fields for O(1) lookup
                    current_fp_fields = {}
                    for field in footprint.texts_and_fields:
                        if isinstance(field, Field):
                            current_fp_fields[field.name] = field.text.value
                    
                    # Append selected custom fields to row
                    for custom_field_name in selected_custom_fields:
                        row.append(current_fp_fields.get(custom_field_name, ""))

                    out.writerow(row)
            
            self.textLog.WriteText(f"Success: File saved to {output_filename}\n")

        except IOError as e:
            error_msg = f"Error writing file: {e}"
            print(error_msg, file=sys.stderr)
            self.textLog.WriteText(error_msg + "\n")