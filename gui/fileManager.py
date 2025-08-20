from PySide6.QtWidgets import (QWidget, QHBoxLayout , QSizePolicy, QVBoxLayout)
from PySide6.QtCore import Qt
import os

from src.QTtree_shot_asset import QTree_Asset
from src.QTtree_Departement import QTree_Departement
from src.QTtree_Task import QTree_Task
from src.QTtree_File import QTree_File
from gui.Shot_Asset_button import AssetShotButton

class FileManagerBox(QWidget):
    def __init__(self, title, parent=None, ratio=None, shared_new_project_window=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 20, 8, 8)
        layout_Qtree = QHBoxLayout()
        layout_Qtree.setContentsMargins(8, 0, 8, 8)
        layout_Qtree.setSpacing(8)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.tree_asset_shot = QTree_Asset()
        self.tree_departement = QTree_Departement()
        self.tree_task = QTree_Task()
        self.tree_file = QTree_File()

        self.asset_shot_button = AssetShotButton()
        self.asset_shot_button.shotSignal.connect(self.tree_asset_shot.switchshot)
        self.asset_shot_button.shotSignal.connect(self.tree_departement.switchshot)
        self.asset_shot_button.shotSignal.connect(self.tree_task.switchshot)
        self.asset_shot_button.shotSignal.connect(self.tree_file.switchshot)

        self.asset_shot_button.assetSignal.connect(self.tree_asset_shot.switchasset)
        self.asset_shot_button.assetSignal.connect(self.tree_departement.switchasset)
        self.asset_shot_button.assetSignal.connect(self.tree_task.switchasset)
        self.asset_shot_button.assetSignal.connect(self.tree_file.switchasset)

        layout.addWidget(self.asset_shot_button, alignment=Qt.AlignHCenter)

        tree_style = """
        QTreeWidget, QTreeView {
            background-color: #2e2e2e;
            color: white;
            border: none;
            border-top-left-radius: 0px;
            border-top-right-radius: 0px;
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;
        }
        QHeaderView::section {
            background-color: #2e2e2e;
            color: white;
            border: none;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            border-bottom-left-radius: 0px;
            border-bottom-right-radius: 0px;
            font-size: 12.5px;
            font-weight: bold;
        }
        """
        self.tree_asset_shot.setStyleSheet(tree_style)
        self.tree_departement.setStyleSheet(tree_style)
        self.tree_task.setStyleSheet(tree_style)
        self.tree_file.setStyleSheet(tree_style)

        self.tree_asset_shot.Asset_Shot_selected.connect(self.tree_departement.QTree_Departement)
        self.tree_asset_shot.clear_signal.connect(self.tree_task.clear)
        self.tree_asset_shot.clear_signal.connect(self.tree_file.clear)
        self.tree_departement.Departement_selected.connect(self.tree_task.QTree_Task)
        self.tree_departement.clear_signal.connect(self.tree_file.clear)
        self.tree_task.Task_selected.connect(self.tree_file.QTree_File)

        self.tree_asset_shot.QTree_Asset_Shot(None)
        self.tree_departement.QTree_Departement(None)
        self.tree_task.QTree_Task(None)
        self.tree_file.QTree_File(None)

        layout_Qtree.addWidget(self.tree_asset_shot)
        layout_Qtree.addWidget(self.tree_departement)
        layout_Qtree.addWidget(self.tree_task)
        layout_Qtree.addWidget(self.tree_file)
        layout.addLayout(layout_Qtree)

        if ratio is None:
            ratio = [0.2, 0.15, 0.2, 0.45]
        layout_Qtree.setStretch(0, int(ratio[0] * 100))
        layout_Qtree.setStretch(1, int(ratio[1] * 100))
        layout_Qtree.setStretch(2, int(ratio[2] * 100))
        layout_Qtree.setStretch(3, int(ratio[3] * 100))
