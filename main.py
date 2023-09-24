import sys
import os
import threading
import subprocess
import base64
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QVBoxLayout, QWidget, QPushButton, QTableWidget, QTableWidgetItem, QInputDialog
from PyQt5.QtCore import Qt

from CBAutoHelper import LDPlayer

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.pathLD = "C:\LDPlayer\LDPlayer9"
        self.selected_devices = []  # Store selected LDPlayer devices

    def initUI(self):
        self.setWindowTitle("Auto Automation App")
        self.setGeometry(100, 100, 1000, 600)  # Increased window width

        self.ldplayer = LDPlayer()  # Initialize your LDPlayer object

        self.devices = self.ldplayer.GetDevices2()  # Get LDPlayer device information

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(8)  # Increased column count to accommodate status columns
        self.tableWidget.setHorizontalHeaderLabels(["Select", "Name", "Index", "ID", "Status", "Start Automation", "Open", "Close", "Rename"])

        self.tableWidget.setColumnWidth(0, 30)
        self.tableWidget.setColumnWidth(2, 30)
        self.tableWidget.setColumnWidth(3, 30)
        
        self.start_button = QPushButton("Start Automation", self)
        self.start_button.clicked.connect(self.startAutomation)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.start_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.populateTable()

    def populateTable(self):
        for index, device in enumerate(self.devices):
            name_item = QTableWidgetItem(device["name"])
            index_item = QTableWidgetItem(device["index"])
            id_item = QTableWidgetItem(device["id"])
            status_item = QTableWidgetItem("Not Started")  # Initialize status as "Not Started"

            checkbox = QCheckBox(self)
            checkbox.stateChanged.connect(self.deviceSelected)

            self.tableWidget.setRowCount(index + 1)
            self.tableWidget.setCellWidget(index, 0, checkbox)
            self.tableWidget.setItem(index, 1, name_item)
            self.tableWidget.setItem(index, 2, index_item)
            self.tableWidget.setItem(index, 3, id_item)
            self.tableWidget.setItem(index, 4, status_item)

            # Add buttons for actions
            open_button = QPushButton("Open", self)
            open_button.clicked.connect(lambda _, dev=device: self.openLDPlayer(dev["name"]))

            close_button = QPushButton("Close", self)
            close_button.clicked.connect(lambda _, dev=device: self.closeLDPlayer(dev["name"]))

            rename_button = QPushButton("Rename", self)
            rename_button.clicked.connect(lambda _, dev=device: self.renameLDPlayer(dev["name"]))

            self.tableWidget.setCellWidget(index, 5, open_button)
            self.tableWidget.setCellWidget(index, 6, close_button)
            self.tableWidget.setCellWidget(index, 7, rename_button)
    def deviceSelected(self, state):
        checkbox = self.sender()
        index = self.tableWidget.indexAt(checkbox.pos()).row()
        device = self.devices[index]

        if state == Qt.Checked:
            self.selected_devices.append(device)
        else:
            self.selected_devices.remove(device)

    def startAutomation(self):
        for device in self.selected_devices:
            emulator_name = device["name"]
            ld_player = LDPlayer()
            ld_player.Info('name', emulator_name)  # Use 'name' instead of 'index'
            threading.Thread(target=self.automationThread, args=(ld_player,)).start()

    def automationThread(self, ld_player):
        emulator_name = ld_player.NameOrId  # Get the LDPlayer name
        ld_player.Info('name', emulator_name)
        ld_player.Start()  # Start the selected LDPlayer
        # Implement your automation logic for each selected device
        # Update the status in the table when automation starts
        index = None
        for i, device in enumerate(self.devices):
            if device["name"] == emulator_name:
                index = i
                break
        if index is not None:
            status_item = self.tableWidget.item(index, 4)
            status_item.setText("Running")  # Update the status to "Running"
        
        # Implement your automation logic here...
        # You can open the device or perform other actions here

    def openLDPlayer(self, emulator_name):
        ld_player = LDPlayer()
        ld_player.Info('name', emulator_name)
        ld_player.Start()
        # Update the status in the table
        index = None
        for i, device in enumerate(self.devices):
            if device["name"] == emulator_name:
                index = i
                break
        if index is not None:
            status_item = self.tableWidget.item(index, 4)
            status_item.setText("Running")  # Update the status to "Running"


    def closeLDPlayer(self, emulator_name):
        ld_player = LDPlayer()
        ld_player.Info('name', emulator_name)
        ld_player.Close()
        # Update the status in the table
        index = None
        for i, device in enumerate(self.devices):
            if device["name"] == emulator_name:
                index = i
                break
        if index is not None:
            status_item = self.tableWidget.item(index, 4)
            status_item.setText("Closed")  # Update the status to "Closed"

    def renameLDPlayer(self, emulator_name):
        ld_player = LDPlayer()
        ld_player.Info('name', emulator_name)
        new_name, ok = QInputDialog.getText(self, "Rename LDPlayer", "Enter new name:")
        if ok:
            ld_player.Rename(new_name)


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
