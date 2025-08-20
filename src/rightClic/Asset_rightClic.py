import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QSizePolicy, QDialog)
from PySide6.QtCore import Qt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from build.Asset_build import AssetBuildWindow
from build.AssetFolder_build import AssetFolderBuild

class RightClickPopup(QDialog):
    def __init__(self, parent=None, path=None):
        super().__init__(parent)
        self.path = path  # Stocke le path reçu
        self.asset_build_window = AssetBuildWindow()
        self.asset_folder_build = AssetFolderBuild()
        self.setWindowFlags(Qt.Popup)
        self.setStyleSheet("background-color: #4b4b4b;")
        self.setFixedWidth(200)
        layout = QVBoxLayout()
        btnCreate = QPushButton("Create Asset")
        btnCreate.setStyleSheet("QPushButton { border: none; color: white; background-color: transparent; } QPushButton:hover { background-color: #da814d; color: white; }")
        btnCreate.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btnCreate.clicked.connect(self.create_asset_structure)
        layout.addWidget(btnCreate)
        btnCreateFolder = QPushButton("Create Folder")
        btnCreateFolder.setStyleSheet("QPushButton { border: none; color: white; background-color: transparent; } QPushButton:hover { background-color: #da814d; color: white; }")
        btnCreateFolder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btnCreateFolder.clicked.connect(self.create_folder)
        layout.addWidget(btnCreateFolder)
        btnDelete = QPushButton("Delete")
        btnDelete.setStyleSheet("QPushButton { border: none; color: white; background-color: transparent; } QPushButton:hover { background-color: #da814d; color: white; }")
        btnDelete.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btnDelete.clicked.connect(self.delete)
        layout.addWidget(btnDelete)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

    def create_asset_structure(self):
        self.asset_build_window.show()
        self.asset_build_window.raise_()
        self.close()
    
    def create_folder(self):
        self.asset_folder_build.show()
        self.asset_folder_build.raise_()
        self.close()

    def delete(self):
        parent = self.parent()
        watcher_removed = False
        while parent:
            if hasattr(parent, 'dir_watcher'):
                try:
                    parent.dir_watcher.removePath(self.path)
                    watcher_removed = True
                except Exception:
                    pass
            parent = getattr(parent, 'parent', lambda: None)()

        if self.path:
            if os.path.exists(self.path):
                import shutil
                try:
                    if os.path.isfile(self.path):
                        os.remove(self.path)
                    else:
                        shutil.rmtree(self.path)
                    print(f"Deleted: {self.path}")
                except Exception as e:
                    print(f"Error deleting {self.path}: {e}")
            else:
                print(f"Path does not exist: {self.path}")
        else:
            print("No path provided to delete.")
        self.close()