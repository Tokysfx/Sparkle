from PySide6.QtWidgets import QPushButton, QWidget, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Signal

class AssetShotButton(QWidget):
    assetSignal = Signal()
    shotSignal = Signal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #4b4b4b; border: 0px white; border-radius: 5px;")

        # Asset button
        self.asset_button = QPushButton("Asset")
        self.asset_button.setStyleSheet("background-color: #da814d; border: 0px white; border-radius: 5px;")
        self.asset_button.setFixedSize(100, 30)
        self.asset_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Shot button
        self.shot_button = QPushButton("Shot")
        self.shot_button.setFixedSize(100, 30)
        self.shot_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Set initial styles
        self.asset_button.setStyleSheet("""QPushButton {
            background-color: #da814d;
            color: white;
            border: 0px white;
            border-top-left-radius: 5px;
            border-bottom-left-radius: 5px;
            border-top-right-radius: 0px;
            border-bottom-right-radius: 0px;
        }
        QPushButton:hover {background-color: #c76a3c;}""")
        self.shot_button.setStyleSheet("""QPushButton {
            background-color: #2e2e2e;
            color: white; border: 0px white;
            border-top-left-radius: 0px;
            border-bottom-left-radius: 0px;
            border-top-right-radius: 5px;
            border-bottom-right-radius: 5px;
        }
        QPushButton:hover {background-color: #141414;}""")

        self.asset_button.clicked.connect(self.on_asset_button_clicked)
        self.shot_button.clicked.connect(self.on_shot_button_clicked)

        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.asset_button)
        layout.addWidget(self.shot_button)

    def on_asset_button_clicked(self):
        """Handle asset button click and update styles."""
        self.asset_button.setStyleSheet("""QPushButton {
            background-color: #da814d;
            color: white;
            border: 0px white;
            border-top-left-radius: 5px;
            border-bottom-left-radius: 5px;
            border-top-right-radius: 0px;
            border-bottom-right-radius: 0px;
        }
        QPushButton:hover {background-color: #c76a3c;}""")
        self.shot_button.setStyleSheet("""QPushButton {
            background-color: #2e2e2e;
            color: white; border: 0px white;
            border-top-left-radius: 0px;
            border-bottom-left-radius: 0px;
            border-top-right-radius: 5px;
            border-bottom-right-radius: 5px;
        }
        QPushButton:hover {background-color: #141414;}""")
        self.assetSignal.emit()

    def on_shot_button_clicked(self):
        """Handle shot button click and update styles."""
        self.asset_button.setStyleSheet("""QPushButton {
            background-color: #2e2e2e;
            color: white; border: 0px white;
            border-top-left-radius: 5px;
            border-bottom-left-radius: 5px;
            border-top-right-radius: 0px;
            border-bottom-right-radius: 0px;
        }
        QPushButton:hover {background-color: #141414;}""")
        self.shot_button.setStyleSheet("""QPushButton {
            background-color: #da814d;
            color: white;
            border: 0px white;
            border-top-left-radius: 0px;
            border-bottom-left-radius: 0px;
            border-top-right-radius: 5px;
            border-bottom-right-radius: 5px;
        }
        QPushButton:hover {background-color: #c76a3c;}""")
        self.shotSignal.emit()
