"""
CRUD Operations Module

Handles all Create, Read, Update, Delete operations including:
- Create dialogs for assets, departments, and tasks
- Delete operations with confirmation
- File and folder management
"""

import os
import shutil
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QHBoxLayout, QVBoxLayout, QLineEdit, 
                               QPushButton, QMessageBox, QWidget)
from ui.ui_utility import stylesheet


class CreateAssetDialog(QMainWindow):
    """Dialog for creating new assets."""
    
    def __init__(self, parent, folder_path):
        """
        Initialize create asset dialog.
        
        Args:
            parent: Parent widget (FileManager)
            folder_path (str): Path where asset will be created
        """
        super().__init__()
        self.setWindowTitle("Create New Asset")
        self.setFixedSize(300, 150)
        self.raise_()
        self.activateWindow()

        stylesheet(self)
        
        self.parent = parent
        self.folder_path = folder_path

        layout = QVBoxLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("Name :")
        layout.addWidget(self.name)

        create_btn = QPushButton("Create")
        create_btn.clicked.connect(self.create_asset)
        layout.addWidget(create_btn)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def create_asset(self):
        """Create new asset with validation."""
        name = self.name.text()
        if not name:
            QMessageBox.warning(self, "Error", "Please input a name !")
            return
        
        asset_path = os.path.join(self.folder_path, name)
        os.makedirs(asset_path, exist_ok=True)

        # Refresh parent view if available
        if self.parent and hasattr(self.parent, 'refresh_all'):
            self.parent.refresh_all()

        self.close()


class CreateDepartmentDialog(QMainWindow):
    """Dialog for creating new departments."""
    
    def __init__(self, parent, asset_path):
        """
        Initialize create department dialog.
        
        Args:
            parent: Parent widget (FileManager)
            asset_path (str): Path to asset where department will be created
        """
        super().__init__()
        self.setWindowTitle("Create New Department")
        self.setFixedSize(300, 150)
        self.raise_()
        self.activateWindow()

        stylesheet(self)
        
        self.parent = parent
        self.asset_path = asset_path

        layout = QVBoxLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("Name :")
        layout.addWidget(self.name)

        create_btn = QPushButton("Create")
        create_btn.clicked.connect(self.create_department)
        layout.addWidget(create_btn)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def create_department(self):
        """Create new department with validation."""
        name = self.name.text()
        if not name:
            QMessageBox.warning(self, "Error", "Please input a name !")
            return
        
        department_path = os.path.join(self.asset_path, name)
        os.makedirs(department_path, exist_ok=True)

        # Refresh parent view if available
        if self.parent and hasattr(self.parent, 'refresh_current_asset'):
            self.parent.refresh_current_asset()

        self.close()


class CreateTaskDialog(QMainWindow):
    """Dialog for creating new tasks."""
    
    def __init__(self, parent, department_path):
        """
        Initialize create task dialog.
        
        Args:
            parent: Parent widget (FileManager)
            department_path (str): Path to department where task will be created
        """
        super().__init__()
        self.setWindowTitle("Create New Task")
        self.setFixedSize(300, 150)
        self.raise_()
        self.activateWindow()

        stylesheet(self)
        
        self.parent = parent
        self.department_path = department_path

        layout = QVBoxLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("Name :")
        layout.addWidget(self.name)

        create_btn = QPushButton("Create")
        create_btn.clicked.connect(self.create_task)
        layout.addWidget(create_btn)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def create_task(self):
        """Create new task with validation."""
        name = self.name.text()
        if not name:
            QMessageBox.warning(self, "Error", "Please input a name !")
            return
        
        task_path = os.path.join(self.department_path, name)
        os.makedirs(task_path, exist_ok=True)

        # Refresh parent view if available
        if self.parent and hasattr(self.parent, 'refresh_current_department'):
            self.parent.refresh_current_department()

        self.close()


class DeleteOperations:
    """Handles delete operations for assets, departments, tasks, and files."""
    
    @staticmethod
    def delete_item(parent):
        """
        Delete currently selected item with confirmation.
        
        Args:
            parent: FileManager instance containing the UI components
        """
        asset = parent.asset_tree.currentItem()
        department = parent.department_list.currentItem()
        task = parent.task_list.currentItem()
        file_item = parent.file_list.currentItem() if hasattr(parent, 'file_list') else None
        
        asset_name = asset.text(0) if asset else None
        folder = asset.parent() if asset else None
        folder_name = folder.text(0) if folder else None
        department_name = department.text() if department else None
        task_name = task.text() if task else None
        file_name = file_item.text() if file_item else None
        
        if parent.asset_tree.hasFocus():
            DeleteOperations._delete_asset(parent, asset_name, folder_name)
        elif parent.department_list.hasFocus():
            DeleteOperations._delete_department(parent, folder_name, asset_name, department_name)
        elif parent.task_list.hasFocus():
            DeleteOperations._delete_task(parent, folder_name, asset_name, department_name, task_name)
        elif hasattr(parent, 'file_list') and parent.file_list.hasFocus():
            DeleteOperations._delete_file(parent, folder_name, asset_name, department_name, task_name, file_name)
    
    @staticmethod
    def _delete_asset(parent, asset_name, folder_name):
        """Delete asset with confirmation."""
        if not asset_name or not folder_name:
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
            parent.refresh_all()
    
    @staticmethod
    def _delete_department(parent, folder_name, asset_name, department_name):
        """Delete department with confirmation."""
        if not folder_name or not asset_name or not department_name:
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
            parent.refresh_current_asset()
    
    @staticmethod
    def _delete_task(parent, folder_name, asset_name, department_name, task_name):
        """Delete task with confirmation."""
        if not folder_name or not asset_name or not department_name or not task_name:
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
            parent.refresh_current_department()
    
    @staticmethod
    def _delete_file(parent, folder_name, asset_name, department_name, task_name, file_name):
        """Delete file with confirmation."""
        if not folder_name or not asset_name or not department_name or not task_name or not file_name:
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
            parent.refresh_current_task()


# Legacy compatibility functions (to be removed later)
def delete(parent):
    """Legacy delete function - delegates to DeleteOperations."""
    DeleteOperations.delete_item(parent)


# Legacy dialog aliases (to be removed later)
create_new_asset_dialog = CreateAssetDialog
create_new_department_dialog = CreateDepartmentDialog
create_new_task_dialog = CreateTaskDialog