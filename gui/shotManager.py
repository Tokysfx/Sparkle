from PySide6.QtWidgets import QHBoxLayout, QWidget

class shotManager(QWidget):
    def __init__(self, parent=None, shared_new_project_window=None):
        super().__init__(parent)
        self.shared_new_project_window = shared_new_project_window

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.black_box = QWidget(self)
        self.black_box.setStyleSheet("background-color: #2e2e2e;")
        layout.addWidget(self.black_box)
