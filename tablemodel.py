from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

class TableModel(QAbstractTableModel):
    def __init__(self, fields=None):
        super().__init__()
        # Internal data storage: [Check State, Field Name]
        # Item (Row Number) is calculated dynamically, no need to store it.
        self._data = [] 
        self.headers = ["Item", "Add", "Name"]
        
        # If input data is provided, load it immediately
        if fields:
            self.set_field_list(fields)

    def set_field_list(self, field_names):
        """
        Accepts a list of names: ['Datasheet', 'Note']
        Converts to: [[False, 'Datasheet'], [False, 'Note']]
        """

        if field_names is None: 
            field_names = []

        self.beginResetModel()
        # Default is False (Unchecked)
        self._data = [[False, name] for name in field_names]
        self.endResetModel()
    
    def get_data_checked(self):
        """Returns a list of checked field names."""
        results = []
        for row in self._data:
            if row[0]:
                results.append(row[1])       # Field Name
        return results

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return 3 # 3 Columns: Item, Add, Name

    def data(self, index, role):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        # --- TEXT DISPLAY (DisplayRole) ---
        if role == Qt.DisplayRole:
            if col == 0: 
                # Item Column: Return row number (index 0 -> shows 1)
                return str(row + 1)
            if col == 2:
                # Name Column: Return field name
                return self._data[row][1]
            # Column 1 (Add) returns no text, only displays the checkbox
            return None

        # --- CHECKBOX DISPLAY (CheckStateRole) ---
        # Only for Column 1 (Add)
        if role == Qt.CheckStateRole and col == 1:
            # Return Unchecked (False) or Checked (True) based on data
            return Qt.Checked if self._data[row][0] else Qt.Unchecked

        # --- CENTER ALIGNMENT (TextAlignmentRole) ---
        if role == Qt.TextAlignmentRole:
            if col == 0: return Qt.AlignCenter # Center align row number
            
        return None

    def setData(self, index, value, role):
        # Allow user to tick Column 1 (Add)
        if role == Qt.CheckStateRole and index.column() == 1:
            self._data[index.row()][0] = (value == Qt.Checked.value)
            self.dataChanged.emit(index, index, [role])
            return True
        return False

    def flags(self, index):
        flags = super().flags(index)
        if index.column() == 1: # Only 'Add' column is checkable
            flags |= Qt.ItemIsUserCheckable | Qt.ItemIsEnabled
        else:
            flags |= Qt.ItemIsEnabled # Other columns are read-only
        return flags

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section < len(self.headers):
                return self.headers[section]
        return None