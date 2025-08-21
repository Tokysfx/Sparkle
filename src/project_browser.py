import os
import json
from PySide6.QtWidgets import (
    QGridLayout, QHBoxLayout, QLabel, QWidget, QVBoxLayout, QSizePolicy, QFrame,
    QDialog, QPushButton
)
from PySide6.QtCore import Qt, QTimer, Signal, QPoint
from PySide6.QtGui import QCursor
from utils.Path_Catcher import get_projectPath_Active
import shutil

class ProjectMenu(QDialog):
    def __init__(self, parent=None, path=None, project_data=None):
        super().__init__(parent)
        self.path = path
        self.project_data = project_data
        self.setWindowFlags(Qt.Popup)
        self.setStyleSheet("background-color: #4b4b4b;")
        self.setFixedWidth(200)
        layout = QVBoxLayout()

        btnDelete = QPushButton("Delete Project")
        btnDelete.setStyleSheet("QPushButton { border: none; color: white; background-color: transparent; } QPushButton:hover { background-color: #da814d; color: white; }")
        btnDelete.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btnDelete.clicked.connect(self.delete_project)
        layout.addWidget(btnDelete)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

    def delete_project(self):
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
        confirm_dialog = QDialog(self)
        confirm_dialog.setWindowTitle("Confirmation")
        confirm_dialog.setStyleSheet("background-color: #4b4b4b; border-radius: 8px;")
        confirm_dialog.setFixedSize(350, 140)
        layout = QVBoxLayout()
        label = QLabel(f"Are you sure you want to delete this project?\n{self.path}")
        label.setStyleSheet("color: white; font-size: 15px; font-weight: bold;")
        layout.addWidget(label)
        btn_layout = QHBoxLayout()
        btn_yes = QPushButton("Yes")
        btn_yes.setStyleSheet("QPushButton { border: none; color: white; background-color: #da814d; border-radius: 5px; padding: 6px 18px; font-weight: bold; } QPushButton:hover { background-color: #c76a3c; }")
        btn_no = QPushButton("No")
        btn_no.setStyleSheet("QPushButton { border: none; color: white; background-color: #888; border-radius: 5px; padding: 6px 18px; font-weight: bold; } QPushButton:hover { background-color: #555; }")
        btn_layout.addWidget(btn_yes)
        btn_layout.addWidget(btn_no)
        layout.addLayout(btn_layout)
        confirm_dialog.setLayout(layout)

        def on_yes():
            print("Project deleted.")
            import os
            name = self.project_data.get("name")
            projectPath = os.path.join(self.project_data.get("path"), name)
            projects_active = os.path.join(projectPath, "02_Production")
            sparkle_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            projects_dir = os.path.join(sparkle_dir, "data", "projects")
            activeprojectpath = os.path.join(sparkle_dir, "data", "active_project.json")
            projectJSONPath = os.path.join(projects_dir, f"{name}_project.json")
            # UI formatting only for display, not for comparison
            print(f"Projects Active path (UI): {projects_active.replace('/', '\\').replace('\\', '\\\\')}")
            with open(activeprojectpath, 'r') as f:
                data = json.load(f)
            activeprojectpath_raw = data.get("active_project_path", "")
            # Normalize both paths for comparison
            compare_projects_active = os.path.normpath(projects_active)
            compare_activeprojectpath = os.path.normpath(activeprojectpath_raw)
            if compare_activeprojectpath == compare_projects_active:
                if os.path.isdir(activeprojectpath):
                    activeprojectfile = os.path.join(activeprojectpath, "active_project.json")
                else:
                    activeprojectfile = activeprojectpath
                print(f"Changing path: {activeprojectfile}")
                with open(activeprojectfile, 'w') as f:
                    json.dump({"active_project_path": None}, f)
            else:
                print(f"Active project path does not match: {activeprojectpath} != {projects_active}")
            if os.path.exists(projectJSONPath):
                os.remove(projectJSONPath)
            else:
                print(f"Fail to find {projectJSONPath}")
            if os.path.exists(projectPath):
                shutil.rmtree(projectPath)
            else:
                print(f"Fail to find {projectPath}")
            confirm_dialog.accept()

        def on_no():
            confirm_dialog.reject()

        btn_yes.clicked.connect(on_yes)
        btn_no.clicked.connect(on_no)
        confirm_dialog.exec()


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
        if event.button() == Qt.LeftButton:
            self.parent_browser.clicked(self.project_data)
        elif event.button() == Qt.RightButton:
            self.parent_browser.projectMenu(self.project_data)


class projectBrowser(QWidget):
    def refresh_projects(self):
        # Remove all widgets from the layout
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        # Ajouter les ProjectBox pour chaque projet
        for idx, json_file in enumerate(os.listdir(self.projectdata_dir)):
            if json_file.endswith(".json"):
                row_count = idx // self.Column
                col_count = idx % self.Column
                with open(os.path.join(self.projectdata_dir, json_file), 'r') as file:
                    project_data = json.load(file)
                box_widget = ProjectBox(project_data, parent_browser=self)
                self.layout.addWidget(box_widget, row_count, col_count)

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

    def clicked(self, project_data):
        print("Project clicked:", project_data.get("name"))
        project_root = os.path.join(project_data.get("path"), project_data.get("name"))
        production_path = os.path.join(project_root, "02_Production")
        production_path = os.path.normpath(production_path)
        print("Project Path (normalized):", production_path)
        get_projectPath_Active(production_path)

    def projectMenu(self, project_data):
        """
        Affiche le menu contextuel pour le projet sélectionné.
        """
        print(f"Right click on project: {project_data.get('name')}")
        projectPath = os.path.join(project_data.get("path"), project_data.get("name"))
        menu = ProjectMenu(parent=self, path=projectPath, project_data=project_data)
        # Affiche le menu à la position du curseur
        cursor_pos = self.mapFromGlobal(QCursor.pos()) if hasattr(Qt, 'QCursor') else QPoint(100, 100)
        menu.move(QCursor.pos())
        menu.exec()