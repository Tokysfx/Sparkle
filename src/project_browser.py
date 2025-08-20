import os
import json
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QWidget, QVBoxLayout, QSizePolicy, QFrame
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import QWidget
from utils.Path_Catcher import get_projectPath_Active


class ProjectBox(QFrame):
    def __init__(self, project_data, parent_browser):
        super().__init__()
        self.project_data = project_data
        self.parent_browser = parent_browser
        self.setFixedHeight(120)

        self.setObjectName("ProjectBox")
    
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(6)

        left_box = QVBoxLayout()
        label_name = QLabel(project_data.get("name", "Project Name"))
        label_path = QLabel(project_data.get("path", "Project Path"))
        label_description = QLabel(project_data.get("description", "Project description goes here."))
        label_name.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
        label_path.setStyleSheet("color: #cccccc; font-size: 12px;")
        label_description.setStyleSheet("color: #bbbbbb; font-size: 12px; background: transparent;")

        left_box.addWidget(label_name, alignment=Qt.AlignLeft | Qt.AlignVCenter)
        left_box.addWidget(label_path, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        left_widget = QWidget()
        left_widget.setLayout(left_box)
        left_widget.setStyleSheet("background: transparent;")

        main_layout.addWidget(left_widget, alignment=Qt.AlignLeft | Qt.AlignVCenter)
        main_layout.addWidget(label_description, alignment=Qt.AlignRight | Qt.AlignVCenter)

        self.setLayout(main_layout)
        self.setStyleSheet("background: #2e2e2e; border-radius: 6px;")

    def mousePressEvent(self, event):
        self.parent_browser.clicked(self.project_data)
        super().mousePressEvent(event)


class projectBrowser(QWidget):

    projectPath = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.Column = 3

        self.basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.projectdata_dir = os.path.join(self.basedir, "data", "projects")

        self.layout = QGridLayout()
        self.layout.setContentsMargins(8, 8, 8, 8)  # Marge standard
        self.layout.setSpacing(8)
        self.setLayout(self.layout)
        self.setStyleSheet("""border: 0px solid #888;border-radius: 8px;background: #4e4e4e;""")

        self.refresh_projects()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_projects)
        self.timer.start(100)

    def refresh_projects(self):
        # Remove all widgets from the layout
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        # Add project boxes
        for idx, json_file in enumerate(os.listdir(self.projectdata_dir)):
            if json_file.endswith(".json"):
                row_count = idx // self.Column
                col_count = idx % self.Column
                with open(os.path.join(self.projectdata_dir, json_file), 'r') as file:
                    project_data = json.load(file)

                box_widget = ProjectBox(project_data, parent_browser=self)
                self.layout.addWidget(box_widget, row_count, col_count)

    def clicked(self, project_data):
        print("Project clicked:", project_data.get("name"))
        project_root = os.path.join(project_data.get("path"), project_data.get("name"))
        production_path = os.path.join(project_root, "02_Production")
        production_path = os.path.normpath(production_path)
        print("Project Path (normalized):", production_path)
        get_projectPath_Active(production_path)
