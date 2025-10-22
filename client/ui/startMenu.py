from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget
from PySide6.QtCore import Qt, Signal
from src.project_manager import createProject, load_project

class startMenu (QWidget):

    load_project_signal = Signal()

    def __init__(self):
        super().__init__()
        """
        Config UI default menu - No project
        """

        layout = QVBoxLayout()
        title_label = QLabel("Welcome to Sparkle")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)


        layout_btn = QHBoxLayout()
        new_project_btn = QPushButton("New project")
        new_project_btn.clicked.connect(self.open_create_project)
        layout_btn.addWidget(new_project_btn)

        load_project_btn = QPushButton("Load project")
        load_project_btn.clicked.connect(self.load_project)
        layout_btn.addWidget(load_project_btn)
        
        layout.addLayout(layout_btn)
        
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def open_create_project(self):
        self.create_window = createProject()
        self.create_window.show()
    def load_project(self):
        self.load_window = load_project()
        self.load_window.show()




        