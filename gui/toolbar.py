from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QToolBar 
from PySide6.QtCore import Qt, Signal 
from PySide6.QtGui import QAction
import sys

class VerticalToolBar(QToolBar):

    homeClicked = Signal()  # Signal emitted when the home button is clicked
    projectClicked = Signal()  # Signal emitted when the project button is clicked

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.setOrientation(Qt.Vertical)

        """ Configuration Boutons """
        #Offset 8 pixels
        offset = QWidget(self)
        offset.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        offset.setMinimumHeight(8)
        self.addWidget(offset)

        # Espaceur supérieur pour centrer Home
        top_spacer = QWidget(self) # Create a spacer widget
        top_spacer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding) # Set the size policy to expand vertically
        self.addWidget(top_spacer)   # Add the spacer widget to the toolbar
        # Bouton Home
        home_action = QAction("Home", self)
        home_action.setStatusTip("Retour à l'accueil")
        home_action.triggered.connect(self.home_button)  # Connect the action to the homeClicked signal
        self.addAction(home_action)  # Add the action to the toolbar
        # Espaceur inférieur pour centrer Home
        middle_spacer = QWidget(self) # Create another spacer widget
        middle_spacer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding) # Set the size policy to expand vertically
        self.addWidget(middle_spacer)   # Add the second spacer widget to the toolbar
        # Bouton Project
        project_action = QAction("Project", self)
        project_action.setStatusTip("Gérer le projet")
        project_action.triggered.connect(self.project_button)  # Connect the action to the projectClicked signal
        self.addAction(project_action)
        
        # offset 8 pixels
        offset = QWidget(self)
        offset.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        offset.setMinimumHeight(8)
        self.addWidget(offset)
    
    def home_button(self):
        self.homeClicked.emit()

    def project_button(self):
        self.projectClicked.emit()

if __name__ == '__main__':
    app = QToolBar(sys.argv)
    toolbar = VerticalToolBar()
    toolbar.show()
    sys.exit(app.exec_())