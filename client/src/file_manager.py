import os
import shutil
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QWidget
from ui.ui_utility import stylesheet
from src.config_project import project_config

class create_new_asset_dialog(QMainWindow):
    def __init__(self, parent, folder_path):
        super().__init__()

        self.setWindowTitle("Create New Asset")
        self.setFixedSize(300, 150)
        self.raise_()
        self.activateWindow()

        stylesheet(self)
        
        #config = project_config()
        #self.department = config.department
        #self.task =  config.task

        self.parent = parent

        self.folder_path = folder_path

        layout = QVBoxLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("Name :")
        layout.addWidget(self.name)

        create_btn = QPushButton("Create")
        create_btn.clicked.connect(self.create_new_asset_btn)
        layout.addWidget(create_btn)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def create_new_asset_btn(self):
        name = self.name.text()
        if not name:
            QMessageBox.warning(self, "Error", "Please input a name !")
            return
        
        asset_path = os.path.join(self.folder_path, name)
        os.makedirs(asset_path, exist_ok=True)

        if self.parent and hasattr(self.parent, 'load_assets'):
            expanded_items = []
            for i in range(self.parent.asset_tree.topLevelItemCount()):
                item = self.parent.asset_tree.topLevelItem(i)
                if item.isExpanded():
                    expanded_items.append(item.text(0))
            
            self.parent.load_assets()
            
            for i in range(self.parent.asset_tree.topLevelItemCount()):
                item = self.parent.asset_tree.topLevelItem(i)
                if item.text(0) in expanded_items:
                    item.setExpanded(True)

        self.close()

class create_new_department_dialog(QMainWindow):
    def __init__(self, parent, asset_path):
        super().__init__()

        self.setWindowTitle("Create New Department")
        self.setFixedSize(300, 150)
        self.raise_()
        self.activateWindow()

        stylesheet(self)
        
        #config = project_config()
        #self.department = config.department
        #self.task =  config.task

        self.parent = parent

        self.asset_path = asset_path

        layout = QVBoxLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("Name :")
        layout.addWidget(self.name)

        create_btn = QPushButton("Create")
        create_btn.clicked.connect(self.create_new_department_btn)
        layout.addWidget(create_btn)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def create_new_department_btn(self):
        name = self.name.text()
        if not name:
            QMessageBox.warning(self, "Error", "Please input a name !")
            return
        
        department_path = os.path.join(self.asset_path, name)
        os.makedirs(department_path, exist_ok=True)

        if self.parent and hasattr(self.parent, 'load_assets'):
            expanded_items = []
            for i in range(self.parent.asset_tree.topLevelItemCount()):
                item = self.parent.asset_tree.topLevelItem(i)
                if item.isExpanded():
                    expanded_items.append(item.text(0))
            
            self.parent.on_asset_clicked()
            
            for i in range(self.parent.asset_tree.topLevelItemCount()):
                item = self.parent.asset_tree.topLevelItem(i)
                if item.text(0) in expanded_items:
                    item.setExpanded(True)

        self.close()

class create_new_task_dialog(QMainWindow):
    def __init__(self, parent, department_path):
        super().__init__()

        self.setWindowTitle("Create New Department")
        self.setFixedSize(300, 150)
        self.raise_()
        self.activateWindow()

        stylesheet(self)
        
        #config = project_config()
        #self.department = config.department
        #self.task =  config.task

        self.parent = parent

        self.department_path = department_path

        layout = QVBoxLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("Name :")
        layout.addWidget(self.name)

        create_btn = QPushButton("Create")
        create_btn.clicked.connect(self.create_new_task_btn)
        layout.addWidget(create_btn)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def create_new_task_btn(self):
        name = self.name.text()
        if not name:
            QMessageBox.warning(self, "Error", "Please input a name !")
            return
        
        task_path = os.path.join(self.department_path, name)
        os.makedirs(task_path, exist_ok=True)

        if self.parent and hasattr(self.parent, 'load_assets'):
            expanded_items = []
            for i in range(self.parent.asset_tree.topLevelItemCount()):
                item = self.parent.asset_tree.topLevelItem(i)
                if item.isExpanded():
                    expanded_items.append(item.text(0))
            
            self.parent.on_department_clicked()
            
            for i in range(self.parent.asset_tree.topLevelItemCount()):
                item = self.parent.asset_tree.topLevelItem(i)
                if item.text(0) in expanded_items:
                    item.setExpanded(True)

        self.close()

def delete(parent):
    asset = parent.asset_tree.currentItem()
    department = parent.department_list.currentItem()
    task = parent.task_list.currentItem()
    file_item = parent.file_list.currentItem()
    
    asset_name = asset.text(0) if asset else None
    folder = asset.parent() if asset else None
    folder_name = folder.text(0) if folder else None
    department_name = department.text() if department else None
    task_name = task.text() if task else None
    file_name = file_item.text() if file_item else None
    
    if parent.asset_tree.hasFocus():
        if asset is None or folder is None:
            return
        
        result = QMessageBox.question(
            parent, 
            "Delete Asset", 
            f"Delete '{asset_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if result == QMessageBox.Yes:
            asset_path = os.path.join(parent.production_folder, folder_name, asset_name)
            shutil.rmtree(asset_path)
            
            expanded_items = []
            for i in range(parent.asset_tree.topLevelItemCount()):
                item = parent.asset_tree.topLevelItem(i)
                if item.isExpanded():
                    expanded_items.append(item.text(0))
            
            parent.load_assets()
            
            for i in range(parent.asset_tree.topLevelItemCount()):
                item = parent.asset_tree.topLevelItem(i)
                if item.text(0) in expanded_items:
                    item.setExpanded(True)
                    
    elif parent.department_list.hasFocus():
        if asset is None or folder is None or department is None:
            return
        
        result = QMessageBox.question(
            parent, 
            "Delete Department", 
            f"Delete '{department_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if result == QMessageBox.Yes:
            dept_path = os.path.join(parent.production_folder, folder_name, asset_name, department_name)
            shutil.rmtree(dept_path)
            parent.on_asset_clicked()
            
    elif parent.task_list.hasFocus():
        if asset is None or folder is None or department is None or task is None:
            return
        
        result = QMessageBox.question(
            parent, 
            "Delete Task", 
            f"Delete '{task_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if result == QMessageBox.Yes:
            task_path = os.path.join(parent.production_folder, folder_name, asset_name, department_name, task_name)
            shutil.rmtree(task_path)
            parent.on_department_clicked()
            
    elif parent.file_list.hasFocus():
        if asset is None or folder is None or department is None or task is None or file_item is None:
            return
        
        result = QMessageBox.question(
            parent, 
            "Delete File", 
            f"Delete '{file_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if result == QMessageBox.Yes:
            file_path = os.path.join(parent.production_folder, folder_name, asset_name, department_name, task_name, file_name)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
            parent.on_task_clicked()