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
    
    def export_file_csv(self, custom_fields, dnpChecked, xLeftChecked, yUpChecked, gridChecked, drillChecked):
        project_path = self.board.document.project.path
        board_filename = os.path.splitext(self.board.document.board_filename)[0]
        output_filename = f"pos_{board_filename}.csv"
        assembly_dir = os.path.join(project_path, "assembly")
        if not os.path.exists(assembly_dir):
            os.makedirs(assembly_dir)
        csv_filepath = os.path.join(assembly_dir, output_filename)
        print(custom_fields)
        print(f"Writing to: {csv_filepath}")
        # 2. Setup CSV Headers
        headers = [
            'Item', 'References', 'Value', 'Footprint', 'Layer', 'Angle', 
            'PosX (mm)', 'PosY (mm)', 'PosX (mil)', 'PosY (mil)', 'SMD', 'DNP'
        ]

        # Check DNP Checkbox (Assuming True means "Hide DNP Column")
        skip_dnp_column = dnpChecked
        if skip_dnp_column:
            headers.remove("DNP")

        headers.extend(custom_fields)

        # 3. Write Data
        try:
            # Use 'with' context manager for safer file handling
            with open(csv_filepath, 'w', encoding="utf-8", newline='') as f:
                out = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                out.writerow(headers)

                IU_PER_MM = 1000000.0
                IU_PER_MILS = 25400.0

                x_scale = 1
                y_scale = 1
                if xLeftChecked:
                    x_scale = -1
                if yUpChecked:
                    y_scale = -1
                
                offset = Vector2.from_xy(0, 0)
                if gridChecked:
                    offset = self.board.get_origin(BoardOriginType.BOT_GRID)
                elif drillChecked:
                    offset = self.board.get_origin(BoardOriginType.BOT_DRILL)
                
                #print(f"Origin: {origin_sel} @ {offset}")

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
                    for custom_field_name in custom_fields:
                        row.append(current_fp_fields.get(custom_field_name, ""))

                    out.writerow(row)
            
            #self.textLog.WriteText(f"Success: File saved to {output_filename}\n")
            return True, csv_filepath

        except IOError as e:
            error_msg = f"Error writing file: {e}"
            print(error_msg, file=sys.stderr)
            return False, str(e)

    def sort_key_logic(self, fp):
        """Hàm này chỉ nhận vào 1 footprint và trả về Key để so sánh"""
        
        # 1. Priority: DNP Status (False < True, nên linh kiện thường sẽ lên đầu)
        # Lưu ý: Cần chắc chắn fp.attributes tồn tại, nếu không dùng getattr an toàn hơn
        is_dnp = getattr(fp.attributes, 'do_not_populate', False)
        
        # 2. Priority: Reference Designator (Natural Sort)
        # Split "R10" thành ['r', 10] để so sánh số học thay vì chuỗi
        # Xử lý trường hợp fp chưa có reference
        if hasattr(fp, 'reference_field') and hasattr(fp.reference_field.text, 'value'):
            ref_text = fp.reference_field.text.value
        else:
            ref_text = ""

        # Tách số và chữ: R10 -> ['', 'R', '10', '']
        # Dùng list comprehension để convert số thành int
        natural_key = [int(text) if text.isdigit() else text.lower() 
                        for text in re.split(r'(\d+)', ref_text)]
        
        # Trả về tuple. Python sẽ so sánh phần tử thứ nhất trước (is_dnp),
        # nếu bằng nhau thì so sánh tiếp phần tử thứ hai (natural_key).
        return (is_dnp, natural_key)
    