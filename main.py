import sys
import requests as requests
from PyQt5 import QtWidgets
import time


class FortiGateBackup(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Set the title, size, and layout for the main window
        self.setWindowTitle("FortiGate Backup")
        self.setGeometry(100, 100, 300, 300)
        layout = QtWidgets.QVBoxLayout()

        # Create input text boxes for the device IP addresses, username, and password
        self.device_ips_input = QtWidgets.QLineEdit()
        device_ips_label = QtWidgets.QLabel("Device IP Addresses (comma-separated):")

        layout.addWidget(device_ips_label)
        layout.addWidget(self.device_ips_input)
        self.backup_button = QtWidgets.QPushButton("Backup Devices")
        self.backup_button.clicked.connect(self.start_backup)
        layout.addWidget(self.backup_button)
        self.setLayout(layout)

    def start_backup(self):
        # Get the list of device IP addresses from the GUI
        device_ips = self.device_ips_input.text().split(",")
        # Get config via REST API calls
        for device_ip in device_ips:
            api_url = f'https:/{device_ip}/api/v2/monitor/system/config/backup?scope=global&access_token=API_Token'
            requests.packages.urllib3.disable_warnings()
            data = requests.get(api_url, verify=False)
            time.sleep(2)
            # Save Backup in file
            with open(f'/home/config-backup_{device_ip}.conf', 'wb') as f:
                for line in data:
                    f.write(line)


app = QtWidgets.QApplication(sys.argv)
window = FortiGateBackup()
window.show()
sys.exit(app.exec_())
