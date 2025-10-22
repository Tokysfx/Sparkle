"""
Main client python file of Sparkle
"""

import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QStackedWidget, QSizePolicy
from PySide6.QtCore import Qt

from ui.startMenu import startMenu
from ui.settings import settings
from src.config import configSparkle
from ui.ui_utility import stylesheet
from ui.file_manager import FileManager
from ui.SideBar import SideBar

class Sparkle (QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sparkle 3D Pipeline")
        self.setFixedSize(800,600)

        stylesheet(self)

        #Load settings config
        self.config = configSparkle()
        self.config.load_config()

        self.central_widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sideBar = SideBar()
        self.sideBar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout.addWidget(self.sideBar)

        self.stackedWidgets = QStackedWidget()
        self.stackedWidgets.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.startMenu = startMenu()
        self.settings = settings()
        self.fileManager = FileManager()

        self.stackedWidgets.addWidget(self.startMenu)
        self.stackedWidgets.addWidget(self.settings)
        self.stackedWidgets.addWidget(self.fileManager)

        self.stackedWidgets.setCurrentWidget(self.fileManager)
        layout.addWidget(self.stackedWidgets)
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        self.sideBar.menu_signal.connect(self.show_menu)
        self.sideBar.home_signal.connect(self.show_home)
        self.sideBar.settings_signal.connect(self.show_settings)
    
    def show_settings(self):
        self.stackedWidgets.setCurrentWidget(self.settings)
    def show_home(self):
        self.stackedWidgets.setCurrentWidget(self.fileManager)
    def show_menu(self):
        self.stackedWidgets.setCurrentWidget(self.startMenu)

if __name__=="__main__":
    print ("Sparkle Client Starting ...")
    print ("Version:v.0.1.0")
    app = QApplication(sys.argv)
    window = Sparkle()
    window.show()
    sys.exit(app.exec())
    print ("Client ready")