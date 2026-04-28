from PySide6.QtWidgets import QMainWindow, QMessageBox, QHeaderView, QTableView
from PySide6.QtCore import QTimer, QUrl
from PySide6.QtGui import QDesktopServices
from gui import Ui_MainWindow
from tablemodel import TableModel, PreviewTableModel
from version import version
from kicad_pcb import KiCadPCB
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(f"Component Position Exporter v{version}")

        self.pcb = KiCadPCB()

        self.preview_model = PreviewTableModel()
        self.ui.tablePreview.setModel(self.preview_model)

        header = self.ui.tablePreview.horizontalHeader()
        header.setSectionsMovable(True)
        header.setDragEnabled(True)
        header.setDragDropMode(QTableView.InternalMove)

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
        self.ui.buttonPosition.clicked.connect(self.button_position_clicked)
        self.ui.buttonBOM.clicked.connect(self.button_bom_clicked)
        self.ui.buttonFolder.clicked.connect(self.button_folder_clicked)
        self.ui.buttonClose.clicked.connect(self.close)
        
        # Connect Radio Buttons
        self.tablemodel.dataChanged.connect(self.refresh_preview)
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
            self.refresh_preview()
        else:
            self.ui.statusbar.showMessage(status)
            QMessageBox.warning(self, "Warning", status)

    def refresh_preview(self):
        """Fetch data and display it on the Preview table"""
        if not self.pcb.connected:
            return
            
        # Get both Headers and Data from the CSV export logic
        headers, data = self.pcb.get_preview_data(
            self.tablemodel.get_data_checked(),
            self.ui.checkDNP.isChecked(),
            self.ui.radioIncreasesLeft.isChecked(),
            self.ui.radioIncreasesUp.isChecked(),
            self.ui.radioGridOrigin.isChecked(),
            self.ui.radioDrillOrigin.isChecked()
        )
        
        # Update the table interface
        self.preview_model.update_data(headers, data)

    def button_position_clicked(self):
        if not self.pcb.connected:
            QMessageBox.warning(self, "Warning", "Not connected to a KiCad PCB!")
            return

        # Get the current column order from the tablePreview Header
        header = self.ui.tablePreview.horizontalHeader()
        count = header.count()
        
        # Map from visual index to logical index
        visual_order = []
        for i in range(count):
            logical_index = header.logicalIndex(i)
            visual_order.append(logical_index)

        # Pass visual_order to the export function
        status, message = self.pcb.export_position_csv(
            self.tablemodel.get_data_checked(),
            self.ui.checkDNP.isChecked(),
            self.ui.radioIncreasesLeft.isChecked(),
            self.ui.radioIncreasesUp.isChecked(),
            self.ui.radioGridOrigin.isChecked(),
            self.ui.radioDrillOrigin.isChecked(),
            column_order=visual_order
        )
        
        # Handle displaying the result message
        if status:
            QMessageBox.information(self, "Success", f"CSV file exported successfully!\nPath: {message}")
        else:
            QMessageBox.critical(self, "Error", f"Failed to export file:\n{message}")

    def button_bom_clicked(self):
        if not self.pcb.connected:
            QMessageBox.warning(self, "Warning", "Not connected to a KiCad PCB!")
            return
        status, message = self.pcb.export_bom_csv()

        if status:
            QMessageBox.information(self, "Success", f"CSV file exported successfully!\nPath: {message}")
        else:
            QMessageBox.critical(self, "Error", f"Failed to export file:\n{message}")

    def button_folder_clicked(self):
        if not self.pcb.connected:
            QMessageBox.warning(self, "Warning", "Not connected to a KiCad PCB!")
            return

        project_path = self.pcb.board.document.project.path
        assembly_dir = os.path.join(project_path, "assembly")

        if os.path.exists(assembly_dir):
            QDesktopServices.openUrl(QUrl.fromLocalFile(assembly_dir))
        else:
            QMessageBox.information(self, "Information", "The 'assembly' folder does not exist yet. Please Export first!")

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
        self.refresh_preview()

    def on_xaxis_changed(self, checked):
        if not checked:
            return
        sender = self.sender()
        if sender == self.ui.radioIncreasesLeft:
            print("-> X Axis: Increases Left")
        elif sender == self.ui.radioIncreasesRight:
            print("-> X Axis: Increases Right")
        self.refresh_preview()

    def on_yaxis_changed(self, checked):
        if not checked:
            return
        sender = self.sender()
        if sender == self.ui.radioIncreasesUp:
            print("-> Y Axis: Increases Up")
        elif sender == self.ui.radioIncreasesDown:
            print("-> Y Axis: Increases Down")
        self.refresh_preview()
