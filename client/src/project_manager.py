import os
import json
from PySide6.QtWidgets import QMainWindow, QLineEdit, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QMessageBox, QWidget, QListWidget
from pathlib import Path
from src.config import configSparkle
from src.config_project import project_config
from src.connection_manager import connection_manager
from ui.ui_utility import stylesheet
from ui.settings import settings

class createProject(QMainWindow):
    def __init__(self):
        super().__init__()

        stylesheet(self)

        self.projectConfig = project_config()
        self.settings = settings

        self.config = configSparkle()
        current_config = self.config.load_config()
        self.project_folder = current_config.get("projects_folder", "")

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.name_input = QLineEdit("Name: ")
        layout.addWidget(self.name_input)
        project_folder_label = QLabel(self.project_folder)
        layout.addWidget(project_folder_label)

        layout_btn = QHBoxLayout()
        create_btn = QPushButton("Create")
        create_btn.clicked.connect(self.create_project)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)
        layout_btn.addWidget(create_btn)
        layout_btn.addWidget(cancel_btn)

        layout.addLayout(layout_btn)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
    

    def create_project(self):
        """
        Create Project on the server and local
        """

        project_folder = self.project_folder
        project_name = self.name_input.text()

        if not project_folder:
            QMessageBox.warning(None, "Error", "Please configure projects folder in Settings first!")
            return
        
        if not project_name:
            QMessageBox.warning(self, "Error", "Please enter a project name!")
            return
        
        project_path = os.path.join(project_folder, project_name)
        
        # Check if project already exists locally
        if os.path.exists(project_path):
            QMessageBox.warning(self, "Error", f"Project '{project_name}' already exists locally!")
            return
        status = self.settings.testServer()
        try:
            if status == True:
                # 1. Create project on server first
                server_response = connection_manager.make_request(
                    f"/projects/{project_name}",
                    method="POST",
                    data={"name": project_name}
                )
                print(f"Server response: {server_response}")
                
                # Check if server creation failed
                if server_response and "error" in server_response:
                    QMessageBox.warning(self, "Server Error", server_response["error"])
                    return
            
            # 2. Create project locally
            for main_folders, subfolders in self.projectConfig.config_project.items():
                for subfolder in subfolders:
                    full_path = os.path.join(project_path, main_folders, subfolder)
                    os.makedirs(full_path, exist_ok=True)

            # 3. Update active project
            self.config.update_active_project(project_path)
            
            # 4. Success message
            message = f"Project '{project_name}' created successfully on both local and server!"
            QMessageBox.information(self, "Success", message)
            self.close()
            
        except Exception as e:
            # If local creation fails, we should ideally clean up server project too
            QMessageBox.critical(self, "Error", f"Failed to create project: {str(e)}")
            # TODO: Consider calling server delete endpoint to cleanup


class load_project(QMainWindow):
    def __init__(self):
        super().__init__()
        
        stylesheet(self)
        
        self.projectConfig = project_config()
        self.config = configSparkle()
        current_config = self.config.load_config()
        self.project_folder = current_config.get("projects_folder", "")

    
        central_widget = QWidget()
        layout = QVBoxLayout()

     
        title_label = QLabel("Select a Project to Load:")
        layout.addWidget(title_label)


        self.project_list = QListWidget()
        self.load_projects_in_list() 
        layout.addWidget(self.project_list)

  
        button_layout = QHBoxLayout()
        load_btn = QPushButton("Load Selected")
        load_btn.clicked.connect(self.load_selected_project)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)
        
        button_layout.addWidget(load_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_projects_in_list(self):
        """Scan le dossier et remplit la liste"""
        if not os.path.exists(self.project_folder):
            return
            
        projects = [
            folder for folder in os.listdir(self.project_folder) 
            if os.path.isdir(os.path.join(self.project_folder, folder))
        ]
        
        for project in projects:
            self.project_list.addItem(project)

    def load_selected_project(self):
        """Récupère le projet sélectionné"""
        current_item = self.project_list.currentItem()
        
        if current_item:
            selected_project = current_item.text()
            project_path = os.path.join(self.project_folder, selected_project)
            
            self.config.update_active_project(project_path)
            check_config = self.config.load_config()

            QMessageBox.information(self, "Project Loaded", f"Loading: {selected_project}")
            self.close()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a project first!")