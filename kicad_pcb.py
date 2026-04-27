import re
import csv
import os
import sys
from typing import Optional, Sequence
from kipy import KiCad
from kipy.board import Board, BoardLayer, BoardOriginType
from kipy.board_types import FootprintInstance, Field
from kipy.board_types import Field
from kipy.geometry import Vector2
from kipy.proto.board.board_types_pb2 import FootprintMountingStyle

class KiCadPCB:
    def __init__(self):
        self.kicad: Optional[KiCad] = None
        self.board: Optional[Board] = None
        self.footprints: Optional[Sequence[FootprintInstance]] = None
        self.fields: list[str] | None = None
        self.connected: bool = False

    def connect_kicad(self)-> tuple[bool, str]:
        try:
            self.kicad = KiCad()
            self.board = self.kicad.get_board()
            self.footprints = sorted(self.kicad.get_board().get_footprints(), key=self.sort_key_logic)
            self.connected = True
            #self.kicad.get_version()
            return True, "Connected to KiCad"
        except Exception as e:
            print(f"{e}")
            return False, str(e)
    
    def get_footprints_fields_name(self):
        """
        Scan all footprints to find unique field names (ignoring simulation fields).
        """
        unique_fields = set()
        for footprint in self.footprints:
            for item in footprint.definition.items:
                if isinstance(item, Field):
                    # Check if the name exists and does NOT start with "Sim."
                    if item.name and not item.name.startswith("Sim."):
                        unique_fields.add(item.name)
                        
        self.fields = sorted(list(unique_fields))
        print(f"Found fields: {self.fields}")
    
    def export_file_csv(self, custom_fields, dnpChecked, xLeftChecked, yUpChecked, gridChecked, drillChecked, column_order=None):
        """
        Export data to a CSV file with all configurations from the GUI.
        :param column_order: List of indices representing the column order arranged by the user on the UI.
        """
        # 1. Determine the file save path
        project_path = self.board.document.project.path
        board_filename = os.path.splitext(self.board.document.board_filename)[0]
        output_filename = f"pos_{board_filename}.csv"
        assembly_dir = os.path.join(project_path, "assembly")
        
        if not os.path.exists(assembly_dir):
            os.makedirs(assembly_dir)
        csv_filepath = os.path.join(assembly_dir, output_filename)

        # 2. Set default Headers (Logical Order)
        headers = [
            'Item', 'References', 'Value', 'Footprint', 'Layer', 'Angle', 
            'PosX (mm)', 'PosY (mm)', 'PosX (mil)', 'PosY (mil)', 'SMD', 'DNP'
        ]

        # Handle hiding/showing the DNP column
        skip_dnp_column = dnpChecked
        if skip_dnp_column:
            headers.remove("DNP")

        # Add custom columns to the end of the logical list
        headers.extend(custom_fields)

        # NOTE: If column_order is provided from UI, rearrange the Header according to user preference
        if column_order and len(column_order) == len(headers):
            headers = [headers[i] for i in column_order]

        # 3. Write data
        try:
            with open(csv_filepath, 'w', encoding="utf-8", newline='') as f:
                out = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                out.writerow(headers)

                # Conversion constants
                IU_PER_MM = 1000000.0
                IU_PER_MILS = 25400.0

                # Set axis direction
                x_scale = -1 if xLeftChecked else 1
                y_scale = -1 if yUpChecked else 1
                
                # Set Origin
                offset = Vector2.from_xy(0, 0)
                if gridChecked:
                    offset = self.board.get_origin(BoardOriginType.BOT_GRID)
                elif drillChecked:
                    offset = self.board.get_origin(BoardOriginType.BOT_DRILL)
                
                # Iterate through the component list (pre-sorted in __init__)
                counter = 1
                for footprint in self.footprints:
                    # Check DNP (Do Not Populate) attribute
                    is_dnp = getattr(footprint.attributes, 'do_not_populate', False)
                    
                    # If the user selects "Remove Components with DNP", skip this row entirely
                    if dnpChecked and is_dnp:
                        continue

                    # Calculate coordinates
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
                    angle = f"{footprint.orientation.degrees:.1f}" 
                    smd = "Yes" if footprint.attributes.mounting_style == FootprintMountingStyle.FMS_SMD else "No"
                    layer = "Top" if footprint.layer == BoardLayer.BL_F_Cu else "Bottom"
                    
                    # Create data row according to the initial "Logical Order"
                    full_row = [counter, reference, value, fp_name, layer, angle, mmX, mmY, milX, milY, smd]
                    
                    if not skip_dnp_column:
                        full_row.append("Yes" if is_dnp else "")

                    # Add Custom Fields data
                    current_fp_fields = {field.name: field.text.value 
                                        for field in footprint.texts_and_fields if isinstance(field, Field)}
                    
                    for custom_field_name in custom_fields:
                        full_row.append(current_fp_fields.get(custom_field_name, ""))

                    # 4. Rearrange cells in the row according to "Visual Order" (column_order)
                    if column_order and len(column_order) == len(full_row):
                        final_row = [full_row[idx] for idx in column_order]
                    else:
                        final_row = full_row

                    out.writerow(final_row)
                    counter += 1
            
            return True, csv_filepath

        except Exception as e:
            return False, str(e)

    def get_preview_data(self, custom_fields, dnpChecked, xLeftChecked, yUpChecked, gridChecked, drillChecked):
        """Generate preview data identical to the exported CSV file."""
        # 1. Setup dynamic Headers
        headers = [
            'Item', 'References', 'Value', 'Footprint', 'Layer', 'Angle', 
            'PosX (mm)', 'PosY (mm)', 'PosX (mil)', 'PosY (mil)', 'SMD', 'DNP'
        ]

        skip_dnp_column = dnpChecked
        if skip_dnp_column:
            headers.remove("DNP")

        headers.extend(custom_fields)

        preview_rows = []

        # 2. Setup scale factors and Origin
        IU_PER_MM = 1000000.0
        IU_PER_MILS = 25400.0

        x_scale = -1 if xLeftChecked else 1
        y_scale = -1 if yUpChecked else 1
        
        offset = Vector2.from_xy(0, 0)
        if gridChecked:
            offset = self.board.get_origin(BoardOriginType.BOT_GRID)
        elif drillChecked:
            offset = self.board.get_origin(BoardOriginType.BOT_DRILL)
            
        # 3. Generate data for each row
        for i, footprint in enumerate(self.footprints, start=1):
            delta_x = footprint.position.x - offset.x
            delta_y = footprint.position.y - offset.y

            mmX = round((delta_x * x_scale) / IU_PER_MM, 4)
            mmY = round((delta_y * y_scale) / IU_PER_MM, 4)
            milX = round((delta_x * x_scale) / IU_PER_MILS, 4)
            milY = round((delta_y * y_scale) / IU_PER_MILS, 4)

            fp_name = footprint.definition.id.name
            reference = footprint.reference_field.text.value
            value = footprint.value_field.text.value
            angle = f"{footprint.orientation.degrees:.1f}" 
            
            smd = "Yes" if footprint.attributes.mounting_style == FootprintMountingStyle.FMS_SMD else "No"
            layer = "Top" if footprint.layer == BoardLayer.BL_F_Cu else "Bottom"
            
            # Create row according to default header order
            row = [i, reference, value, fp_name, layer, angle, mmX, mmY, milX, milY, smd]
            
            # Add DNP column if not hidden
            if not skip_dnp_column:
                is_dnp = getattr(footprint.attributes, 'do_not_populate', False)
                dnp_val = "Yes" if is_dnp else ""
                row.append(dnp_val)

            # Add Custom fields
            current_fp_fields = {}
            for field in footprint.texts_and_fields:
                if isinstance(field, Field):
                    current_fp_fields[field.name] = field.text.value
            
            for custom_field_name in custom_fields:
                row.append(current_fp_fields.get(custom_field_name, ""))

            preview_rows.append(row)

        # Return both Header list and Data
        return headers, preview_rows

    def sort_key_logic(self, fp):
        """This function takes 1 footprint and returns a Key for comparison"""
        
        # 1. Priority: DNP Status (False < True, so populated components usually come first)
        # Note: Ensure fp.attributes exists, otherwise using getattr is safer
        is_dnp = getattr(fp.attributes, 'do_not_populate', False)
        
        # 2. Priority: Reference Designator (Natural Sort)
        # Handle case where fp does not have a reference yet
        if hasattr(fp, 'reference_field') and hasattr(fp.reference_field.text, 'value'):
            ref_text = fp.reference_field.text.value
        else:
            ref_text = ""

        # Separate numbers and letters: R10 -> ['', 'R', '10', '']
        # Use list comprehension to convert numbers to int
        natural_key = [int(text) if text.isdigit() else text.lower() 
                        for text in re.split(r'(\d+)', ref_text)]
        
        # Return a tuple. Python will compare the first element first (is_dnp),
        # if they are equal, it will compare the second element (natural_key).
        return (is_dnp, natural_key)
