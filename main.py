import sys
from PyQt5 import QtWidgets
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class FortinetBackup(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Set the title, size, and layout for the main window
        self.setWindowTitle("Fortinet Backup")
        self.setGeometry(100, 100, 300, 300)
        layout = QtWidgets.QVBoxLayout()

        # Create a label for displaying the status of the backup process
        self.status_label = QtWidgets.QLabel("")
        layout.addWidget(self.status_label)
        # Create input text boxes for the device IP addresses, username, and password
        self.device_ips_input = QtWidgets.QLineEdit()
        self.username_input = QtWidgets.QLineEdit()
        self.password_input = QtWidgets.QLineEdit()

        device_ips_label = QtWidgets.QLabel("Device IP Addresses (comma-separated):")
        username_label = QtWidgets.QLabel("Username:")
        password_label = QtWidgets.QLabel("Password:")

        layout.addWidget(device_ips_label)
        layout.addWidget(self.device_ips_input)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.backup_button = QtWidgets.QPushButton("Backup Devices")
        self.backup_button.clicked.connect(self.start_backup)
        layout.addWidget(self.backup_button)

        self.setLayout(layout)

    def start_backup(self):
        # Get the list of device IP addresses from the GUI
        device_ips = self.device_ips_input.text().split(",")

        # Get the username and password from the GUI
        username = self.username_input.text()
        password = self.password_input.text()

        # Start a new instance of a web browser
        driver = webdriver.Firefox()

        # Loop through each device IP address and backup the device
        for device_ip in device_ips:
            self.status_label.setText(f"Backing up device at {device_ip}...")
            QtWidgets.QApplication.processEvents()

            # Navigate to the login page for the Fortinet device
            driver.get(f"http://{device_ip}")

            # Find the username and password input fields and enter the credentials
            username_input = driver.find_element(By.ID, 'email')
            password_input = driver.find_element(By.ID, 'password')
            username_input.send_keys(username)
            password_input.send_keys(password)
            time.sleep(3)
            # Submit the login form
            driver.find_element(By.XPATH, '//button[text()="Login"]').click()

            # Wait for the page to load
            time.sleep(2)

            # Navigate to the System > Backup & Restore page
            # driver.get(f"https://{device_ip}/system_backup.php")
            driver.find_element(By.XPATH, '//div[text()="Logout"]').click()
            # Find the backup button and click it
            # backup_button = driver.find_element(By.NAME, "backup")
            # backup_button.click()

            # Wait for the backup to complete
            time.sleep(2)

        # Close the web browser
        driver.close()

        self.status_label.setText("Backup complete")


app = QtWidgets.QApplication(sys.argv)
window = FortinetBackup()
window.show()
sys.exit(app.exec_())
