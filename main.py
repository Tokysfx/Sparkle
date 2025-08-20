import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QSizePolicy, QWidget, QVBoxLayout
from src.project_new import NewProjectWindow
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QStackedWidget
from gui.toolbar import VerticalToolBar
from gui.fileManager import FileManagerBox
from gui.project import ProjectView
from gui.shotManager import shotManager


class mainwindows(QMainWindow):
    def __init__(self):
        super().__init__()
        windowPage = 1

        self.setWindowTitle("Sparkle")
        self.setMinimumSize(1200, 600)
        self.setStyleSheet("background-color: #4b4b4b;")

        # Toolbar
        self.toolbar = VerticalToolBar()
        self.toolbar.setStyleSheet("background-color: #da814d;")
        self.toolbar.setFixedWidth(45)
        self.toolbar.setObjectName("ToolBar")
        self.toolbar.setMovable(False)
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # main_layout.setContentsMargins(0, 20, 0, 0)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.stacked_widget)
        self.setCentralWidget(central_widget)
        

        # Page 0: File Manager
        self.shared_new_project_window = NewProjectWindow()
        self.file_manager_widget = FileManagerBox("File Manager", shared_new_project_window=self.shared_new_project_window)
        self.file_manager_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stacked_widget.addWidget(self.file_manager_widget)  # index 0

        # Page 1: Project Home Page
        self.project = ProjectView(self, shared_new_project_window=self.shared_new_project_window)
        self.project.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stacked_widget.addWidget(self.project)  # index 1

        # Page 2: Shot Manager
        self.shotManager = shotManager(self, shared_new_project_window=self.shared_new_project_window)
        self.project.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stacked_widget.addWidget(self.shotManager)  # index 2

        # Set default page (0 or 1)
        self.stacked_widget.setCurrentIndex(0)

        self.toolbar.homeClicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.toolbar.projectClicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

def main():
    app = QApplication(sys.argv)
    window = mainwindows()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()