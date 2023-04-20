import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel, QProgressBar
from bleak import BleakScanner
from bt_utils import find_devices, pair_device, connect_device


class BluetoothApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.scan_button = QPushButton("Scan Devices", self)
        self.scan_button.setGeometry(20, 200, 100, 40)
        self.scan_button.clicked.connect(self.scan_or_stop_devices)
        self.is_scanning = False
        self.scan_task = None

    def initUI(self):
        self.setWindowTitle("Bluetooth Device Scanner")
        self.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()

        scan_button = QPushButton("Scan Devices", self)
        scan_button.clicked.connect(self.scan_devices)

        self.device_list = QListWidget(self)
        self.device_list.itemDoubleClicked.connect(self.connect_to_device)

        layout.addWidget(scan_button)
        layout.addWidget(self.device_list)

        self.status_label = QLabel("Ready to scan devices.")
        layout.addWidget(self.status_label)

        self.battery_progress = QProgressBar(self)
        layout.addWidget(self.battery_progress)

        self.alarm_label = QLabel("Alarm status will be shown here.")
        layout.addWidget(self.alarm_label)

        self.setLayout(layout)

    async def scan_devices(self):
        scanner = BleakScanner()
        while self.is_scanning:
            devices = await scanner.discover()
            self.devices = [(device.address, device.name) for device in devices]
            self.device_list.clear()
            for address, name in self.devices:
                self.device_list.addItem(f"{name} ({address})")
            await asyncio.sleep(1)

    def connect_to_device(self):
        selected_device = self.device_list.currentRow()
        device_data = connect_device(self.devices, selected_device)
        self.status_label.setText(f"Connected to the selected device. Battery: {device_data['battery']}")

        # Update battery progress
        self.battery_progress.setValue(int(device_data['battery'].rstrip('%')))

        # Update alarm status
        self.alarm_label.setText(f"Alarm status: {device_data['alarm']}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    bluetooth_app = BluetoothApp()
    bluetooth_app.show()
    sys.exit(app.exec_())
