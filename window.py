from PySide6.QtWidgets import QMainWindow, QMessageBox, QHeaderView, QTableView
from PySide6.QtCore import QTimer
from gui import Ui_MainWindow
from tablemodel import TableModel
from version import version
from kicad_pcb import KiCadPCB

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(f"Component Position Exporter v{version}")

        self.pcb = KiCadPCB()

        # Initialize Model (The 3-column model created previously)
        self.tablemodel = TableModel()
        self.ui.tableView.setModel(self.tablemodel)
        header = self.ui.tableView.horizontalHeader()
        # Column 0 (Item): Resize to fit contents (displaying index numbers)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # Column 1 (Add): Resize to fit contents (displaying checkboxes)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # Column 2 (Name): Stretch to fill the remaining space
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        # Initialize with an empty list
        self.tablemodel.set_field_list([])
        # Customize table appearance
        self.ui.tableView.verticalHeader().setVisible(False) # Hide the default vertical header (left side)
        self.ui.tableView.setSelectionBehavior(QTableView.SelectRows) # Select entire row on click
        self.ui.tableView.setAlternatingRowColors(True) # (Optional) Enable alternating row colors

        # Connect signals to slots
        self.ui.btnExport.clicked.connect(self.button_export_clicked)
        self.ui.btnClose.clicked.connect(self.button_close_clicked)
        
        # Connect Radio Buttons
        self.ui.radioGridOrigin.toggled.connect(self.on_origin_changed)
        self.ui.radioDrillOrigin.toggled.connect(self.on_origin_changed)
        self.ui.radioPageOrigin.toggled.connect(self.on_origin_changed)
        self.ui.radioIncreasesLeft.toggled.connect(self.on_xaxis_changed)
        self.ui.radioIncreasesRight.toggled.connect(self.on_xaxis_changed)
        self.ui.radioIncreasesUp.toggled.connect(self.on_yaxis_changed)
        self.ui.radioIncreasesDown.toggled.connect(self.on_yaxis_changed)
        
        # Delay initialization (500ms) to ensure UI is ready before connecting to KiCad
        QTimer.singleShot(500, self.load_initial_data)

    def load_initial_data(self):
        connected, status = self.pcb.connect_kicad()
        if connected:
            self.ui.statusbar.showMessage(f"Connected to KiCad {self.pcb.kicad.get_version()}")
            print(f"Connected to KiCad {self.pcb.kicad.get_version()}")
            print(f"Opening file {self.pcb.board.document.board_filename}")
            self.pcb.get_footprints_fields_name()
            self.tablemodel.set_field_list(self.pcb.fields)
        else:
            self.ui.statusbar.showMessage(status)
            QMessageBox.information(self, "Message", status)

    def button_close_clicked(self):
        self.close()

    def button_export_clicked(self):
        connected, status = self.pcb.connect_kicad()
        if not connected:
            self.ui.statusbar.showMessage(status)
            QMessageBox.information(self, "Message", status)
            return
        status, message = self.pcb.export_file_csv(
            self.tablemodel.get_data_checked(),
            self.ui.checkDNP.isChecked(),
            self.ui.radioIncreasesLeft.isChecked(),
            self.ui.radioIncreasesUp.isChecked(),
            self.ui.radioGridOrigin.isChecked(),
            self.ui.radioDrillOrigin.isChecked()
        )
        if status:
            self.ui.statusbar.showMessage(f"Success: File saved to {message}")
        else:
            self.ui.statusbar.showMessage(f"Error: {message}")

    def on_origin_changed(self, checked):
        if not checked:
            return
        sender = self.sender()
        if sender == self.ui.radioGridOrigin:
            print("-> Grid Origin selected")
        elif sender == self.ui.radioDrillOrigin:
            print("-> Drill Origin selected")
        elif sender == self.ui.radioPageOrigin:
            print("-> Page Origin selected")

    def on_xaxis_changed(self, checked):
        if not checked:
            return
        sender = self.sender()
        if sender == self.ui.radioIncreasesLeft:
            print("-> X Axis: Increases Left")
        elif sender == self.ui.radioIncreasesRight:
            print("-> X Axis: Increases Right")

    def on_yaxis_changed(self, checked):
        if not checked:
            return
        sender = self.sender()
        if sender == self.ui.radioIncreasesUp:
            print("-> Y Axis: Increases Up")
        elif sender == self.ui.radioIncreasesDown:
            print("-> Y Axis: Increases Down")
