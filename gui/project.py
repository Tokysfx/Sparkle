from PySide6.QtWidgets import QHBoxLayout, QWidget, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from src.project_browser import projectBrowser
from src.project_new import NewProjectWindow

class ProjectView(QWidget):
    def __init__(self, parent=None, shared_new_project_window=None):
        super().__init__(parent)
        self.shared_new_project_window = shared_new_project_window

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 60, 8, 8)
        main_layout.setSpacing(8)

        # Button layout at the top right
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.setContentsMargins(0, 0, 8, 0)
        button = QPushButton("New Project")
        button.setStyleSheet("""
            QPushButton {
                background-color: #da814d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 0;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ff9a4d;
            }
            QPushButton:pressed {
                background-color: #b85c1e;
            }
        """)
        button.setFixedSize(100, 30)
        button_layout.addWidget(button)
        button.clicked.connect(self.open_new_project_window)
        main_layout.addLayout(button_layout)

        # Project browser below the button
        layout_Project = projectBrowser()
        main_layout.addWidget(layout_Project)

        self.setLayout(main_layout)

    def open_new_project_window(self):
        if self.shared_new_project_window is not None:
            self.shared_new_project_window.reset_fields()
            self.shared_new_project_window.show()
            self.shared_new_project_window.raise_()

