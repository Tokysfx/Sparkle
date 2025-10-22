from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton
from PySide6.QtCore import Signal

class SideBar(QFrame):

    menu_signal = Signal()
    home_signal = Signal()
    settings_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("SideBar")
        self.setFixedWidth(60)
        self.setStyleSheet("""
            QFrame#SideBar {
                background-color: #db7515;
            }            
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        menu_btn = QPushButton("Menu")
        menu_btn.clicked.connect(self.menu_signal.emit)
        layout.addWidget(menu_btn)
        layout.addStretch()
        home_btn = QPushButton("Home")
        home_btn.clicked.connect(self.home_signal.emit)
        layout.addWidget(home_btn)
        layout.addStretch()
        setting_btn = QPushButton("Settings")
        setting_btn.clicked.connect(self.settings_signal.emit)
        layout.addWidget(setting_btn)