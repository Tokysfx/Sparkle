import sys
import requests
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QFileDialog, QApplication, QWidget, QLineEdit, QMessageBox

from src.config import configSparkle

class settings(QWidget):


    def __init__(self):
        super().__init__()

        self.config = configSparkle()
        layout = QVBoxLayout()


        self.load_config = QPushButton ("load_config")
        self.load_config.clicked.connect(self.load_settings)
        layout.addWidget(self.load_config)

        self.layout_path = QHBoxLayout()
        self.path_label = QLabel("No folder selected")
        self.layout_path.addWidget(self.path_label)
        self.browse_btn = QPushButton("browse")
        self.browse_btn.clicked.connect(self.choose_folder)
        self.layout_path.addWidget(self.browse_btn)
        layout.addLayout(self.layout_path)

        self.selected_folder = ""

        self.url_input = QLineEdit("http://")
        self.url_input.textChanged.connect(self.save_url)
        layout.addWidget(self.url_input)

        test_server_btn = QPushButton("Test Server")
        test_server_btn.clicked.connect(self.testServer)
        layout.addWidget(test_server_btn)

        
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        self.load_settings()

    def load_settings (self):
        """Load default setting store in JSON"""
        current_config = self.config.load_config()
        folder = current_config.get("projects_folder", "")
        if folder:
            self.selected_folder = folder
            self.path_label.setText(f"Folder: {folder}")
        server_url = current_config.get("url", "")
        if server_url:
            self.url_input.setText(f"{server_url}")

    def choose_folder(self):
        """Choose project folder"""
        file = QFileDialog.getExistingDirectory(None, "Choose a project folder")
        if file:
            self.selected_folder = file
            self.path_label.setText(f"Folder: {self.selected_folder}")
            self.config.update_project_folder(file)
    
    def save_url(self):
        server_url = self.url_input.text()
        if server_url:
            self.config.uptdate_url(server_url)

    def testServer(self):
        current_config = self.config.load_config()
        server_url = current_config.get("url", "")

        try:
            response = requests.get(f"{server_url}/health", timeout=2)
            if response.status_code == 200 and response.json().get("status") == "OK":
                QMessageBox.information(self, "Test Server", "Server online")
                return True
            else:
                QMessageBox.warning(self, "Test Server", "Server offline")                
                return False
        except Exception as e:
            QMessageBox.critical(self, "Test Server", f"Error - {e}")
            return False

            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = settings()
    window.show()
    sys.exit(app.exec())




