import sys
import os
import threading
import base64
import logging
import uiautomator2 as u2
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QCheckBox,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QInputDialog,
    QHBoxLayout
)
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
        self.tableWidget.setColumnCount(5)  # Increased column count to accommodate status columns
        self.tableWidget.setHorizontalHeaderLabels(
            ["Select", "Name", "Index", "ID", "Status"]
        )

        self.tableWidget.setColumnWidth(0, 30)
        self.tableWidget.setColumnWidth(2, 30)
        self.tableWidget.setColumnWidth(3, 30)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.populateTable()
        self.button_panel = ButtonPanel(self)

        layout.addWidget(self.button_panel)

    def openLDPlayer(self, emulator_name):
        ld_player = LDPlayer()
        ld_player.Info('name', emulator_name)
        ld_player.Start()
        self.updateDeviceStatus(emulator_name, "Running")

    def closeLDPlayer(self, emulator_name):
        ld_player = LDPlayer()
        ld_player.Info('name', emulator_name)
        ld_player.Close()
        self.updateDeviceStatus(emulator_name, "Closed")

    def startAutomation(self):
        for device in self.selected_devices:
            emulator_name = device["name"]
            threading.Thread(target=self.automationThread, args=(emulator_name,)).start()



    def populateTable(self):
        for index, device in enumerate(self.devices):
            self.tableWidget.setRowCount(len(self.devices))
            self.tableWidget.setHorizontalHeaderLabels(["Select", "Name", "Index", "ID", "Status"])

            self.tableWidget.setColumnWidth(0, 30)
            self.tableWidget.setColumnWidth(2, 30)
            self.tableWidget.setColumnWidth(3, 30)

            for index, device in enumerate(self.devices):
                checkbox = QCheckBox(self)
                checkbox.stateChanged.connect(self.deviceSelected)

                self.tableWidget.setCellWidget(index, 0, checkbox)
                self.tableWidget.setItem(index, 1, QTableWidgetItem(device["name"]))
                self.tableWidget.setItem(index, 2, QTableWidgetItem(device["index"]))
                self.tableWidget.setItem(index, 3, QTableWidgetItem(device["id"]))
                self.tableWidget.setItem(index, 4, QTableWidgetItem("Chưa khởi động"))

    def createButton(self, text, callback):
        button = QPushButton(text, self)
        button.clicked.connect(callback)
        return button

    def deviceSelected(self, state):
        checkbox = self.sender()
        index = self.tableWidget.indexAt(checkbox.pos()).row()
        device = self.devices[index]

        if state == Qt.Checked:
            self.selected_devices.append(device)
        else:
            self.selected_devices.remove(device)

    def automationThread(self, emulator_name:str):
        try:
            with u2.connect() as d:
                app_package_name = "com.highbrow.games.dv"  # Replace with the actual package name
                d.app_start(app_package_name)

                # Implement your automation logic using uiautomator2 here
                # For example, you can interact with UI elements, simulate clicks, etc.

            self.updateDeviceStatus(emulator_name, "Completed")
        except Exception as e:
            print("Error occurred while automating the app: {}".format(e))
            self.updateDeviceStatus(emulator_name, "Error")

    def updateDeviceStatus(self, emulator_name, status):
        index = next((i for i, device in enumerate(self.devices) if device["name"] == emulator_name), None)
        if index is not None:
            status_item = self.tableWidget.item(index, 4)
            status_item.setText(status)
class ButtonPanel(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        self.open_button = QPushButton("Open", self)
        self.close_button = QPushButton("Close", self)
        self.start_automation_button = QPushButton("Start Automation", self)

        layout = QHBoxLayout()
        layout.addWidget(self.open_button)
        layout.addWidget(self.close_button)
        layout.addWidget(self.start_automation_button)

        self.setLayout(layout)

        self.connectSlots()

    def connectSlots(self):
        self.open_button.clicked.connect(self.openDevices)
        self.close_button.clicked.connect(self.closeDevices)
        self.start_automation_button.clicked.connect(self.startAutomation)

    def openDevices(self):
        for device in self.main_app.selected_devices:
            emulator_name = device["name"]
            self.main_app.openLDPlayer(emulator_name)

    def closeDevices(self):
        for device in self.main_app.selected_devices:
            emulator_name = device["name"]
            self.main_app.closeLDPlayer(emulator_name)

    def startAutomation(self):
        self.main_app.startAutomation()

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
