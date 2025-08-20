import os
import json
from PySide6.QtWidgets import (
    QMainWindow, QGridLayout, QVBoxLayout, QLabel, QWidget,
    QLineEdit, QTextEdit, QPushButton, QFileDialog, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import (Qt, Signal)
from utils.Path_Catcher import get_projectPath_Active

class NewProjectWindow(QMainWindow):
    
    new_project_signal = Signal(str)

    def reset_fields(self):
        self.name_input.clear()
        self.path_input.clear()
        self.desc_input.clear()

    

    def __init__(self):
        super().__init__()

        data = {}

        self.setWindowTitle("New Project")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #4b4b4b;")
        self.setMaximumSize(400, 300)

        layout = QVBoxLayout()
        layout.setSpacing(8)

        # Name input
        layout_name = QHBoxLayout()
        name_label = QLabel("Name:")
        name_label.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
        name_input = QLineEdit()
        name_input.setStyleSheet("background-color: #2e2e2e; color: white; border: none; border-radius: 4px;")
        layout_name.addWidget(name_label)
        layout_name.addWidget(name_input)
        layout.addLayout(layout_name)

        # Path input with browser
        layout_path = QHBoxLayout()
        path_label = QLabel("Path:")
        path_label.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setStyleSheet("background-color : #2e2e2e; color: white; border: none; border-radius: 4px;")
        browse_button = QPushButton("Browse")
        browse_button.setFixedSize(60, 18)
        browse_button.setStyleSheet("""
            QPushButton {
                background-color: #da814d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0px 0;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ff9a4d;
            }
            QPushButton:pressed {
                background-color: #b85c1e;
            }
        """)
        browse_button.clicked.connect(self.browse_path)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_button)
        layout_path.addWidget(path_label)
        layout_path.addLayout(path_layout)
        layout.addLayout(layout_path)

        # Description input
        desc_label = QLabel("Description:")
        desc_label.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
        self.desc_input = QTextEdit()
        self.desc_input.setStyleSheet("background-color: #2e2e2e; color: white; border: none; border-radius: 4px;")
        self.desc_input.setMinimumHeight(20)
        layout.addWidget(desc_label)
        layout.addWidget(self.desc_input)

        validate_button = QPushButton("Validate")
        validate_button.setFixedSize(70, 22)
        validate_button.setStyleSheet("""
            QPushButton {
                background-color: #da814d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0px 0;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #ff9a4d;
            }
            QPushButton:pressed {
                background-color: #b85c1e;
            }
        """)
        layout.addWidget(validate_button, alignment=Qt.AlignHCenter)
        validate_button.clicked.connect(self.on_validate_clicked)

        # Set layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.name_input = name_input


    def on_validate_clicked(self):

        """
                Validate and save project data
        """
        name = self.name_input.text()
        path = self.path_input.text()
        description = self.desc_input.toPlainText()

        data = {
            "name": name,
            "path": path,
            "description": description
        }

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, "data\projects")
        os.makedirs(data_dir, exist_ok=True)

        json_path = os.path.join(data_dir, f"{name}_project.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)


        """            Create project folders
        """

        data_assets_shots = ("assets", "shots")
        project_forlders = ("01_Preproduction", "02_Production", "03_Postproduction", "04_Editing")
        project_data_dir = os.path.join(base_dir, "data", "build")

        project_root = os.path.join(path, name)
        production_path = os.path.join(project_root, "02_Production")

        os.makedirs(project_root, exist_ok=True)
        for folder in project_forlders:
            folder_path = os.path.join(project_root, folder)
            os.makedirs(folder_path, exist_ok=True)

            for folder in data_assets_shots:
                folder_path = os.path.join(project_root, "02_Production", folder)
                os.makedirs(folder_path, exist_ok=True)

                if folder == "assets":
                    template_json_path = os.path.join(project_data_dir, "New_project.json")
                    if os.path.exists(template_json_path):
                        with open(template_json_path, "r", encoding="utf-8") as template_file:
                            project_data = json.load(template_file)
                            for ProjectSetting, folders in project_data.get("new_project_settings", {}).items():
                                if ProjectSetting == "DefaultProjectName":
                                    for folder_name in folders:
                                        subfolder_path = os.path.join(folder_path, folder_name)
                                        os.makedirs(subfolder_path, exist_ok=True)
                    else:
                        print(f"Le fichier {template_json_path} est introuvable.")
                        
        get_projectPath_Active(production_path)

        QMessageBox.information(self, "Project Saved", f"Project data saved to {json_path}")

    def browse_path(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        if dialog.exec():
            selected = dialog.selectedFiles()
            if selected:
                self.path_input.setText(selected[0])

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = NewProjectWindow()
    window.show()
    sys.exit(app.exec())
