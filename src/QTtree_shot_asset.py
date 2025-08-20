from PySide6.QtWidgets import QTreeWidget
from PySide6.QtCore import Qt, Signal, QTimer, QFileSystemWatcher, QTimer
import os
import json
from utils.file_manager_utils import populate_tree, get_expanded_paths, restore_expanded_paths
from src.rightClic.Asset_rightClic import RightClickPopup

class QTree_Asset(QTreeWidget):
    Asset_Shot_selected = Signal(str)
    clear_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.asset_or_shot = "assets"
        self.itemClicked.connect(self.handle_item_click)
        self.current_path = ""
        self.json_watcher = QFileSystemWatcher()
        self.json_watcher.fileChanged.connect(self.check_path_changes)

        self.dir_watcher = QFileSystemWatcher()
        self.dir_watcher.directoryChanged.connect(self.on_directory_changed)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        self.json_path = os.path.join(data_dir, "active_project.json")

        if os.path.exists(self.json_path):
            self.json_watcher.addPath(self.json_path)

    def QTree_Asset_Shot(self, path):
        self.clear()
        self.setHeaderLabel("Asset")
        header = self.headerItem()
        header.setTextAlignment(0, Qt.AlignCenter)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_path_changes)
        self.timer.start(50)

    def handle_item_click(self, item):
        self.clear_signal.emit()
        depth = 0
        current = item
        while current.parent() is not None:
            depth += 1
            current = current.parent()
        if depth == 1:
            departement_path = item.data(0, Qt.UserRole)
            if self.asset_or_shot == "assets":
                departementScene_path = os.path.join(departement_path, "Scenefiles")
            else:
                departementScene_path = departement_path
            self.Asset_Shot_selected.emit(departementScene_path)

    def update_path(self, path):
        max_depth = 1

        expanded_paths = get_expanded_paths(self)

        self.current_path = path
        self.clear()

        self.dir_watcher.blockSignals(True)
        self.dir_watcher.removePaths(self.dir_watcher.directories())
        if path and os.path.exists(path):
            dirs_to_watch = []
            for root, dirs, files in os.walk(path):
                rel_root = os.path.relpath(root, path)
                depth = 0 if rel_root == '.' else rel_root.count(os.sep) + 1
                if depth <= max_depth:
                    dirs_to_watch.append(root)
                if depth >= max_depth:
                    dirs[:] = []
            if dirs_to_watch:
                self.dir_watcher.addPaths(dirs_to_watch)
        self.dir_watcher.blockSignals(False)

        if path and os.path.exists(path):
            populate_tree(path, self, max_depth=max_depth)
            restore_expanded_paths(self, expanded_paths)
        else:
            print("Le chemin n'existe pas :", path)

    def on_directory_changed(self, changed_path):
        if self.current_path and (
            changed_path == self.current_path or changed_path.startswith(self.current_path + os.sep)
        ):
            self.update_path(self.current_path)

    def check_path_changes(self):
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                new_path = data.get("active_project_path", "")
                new_path = os.path.join(new_path, self.asset_or_shot)
                if new_path and new_path != self.current_path:
                    self.update_path(new_path)
            except Exception as e:
                print(f"Erreur lecture JSON projet actif : {e}")
        if self.json_path not in self.json_watcher.files():
            self.json_watcher.addPath(self.json_path)

    def contextMenuEvent(self, event):
        item = self.itemAt(event.pos())
        if item:
            path = item.data(0, Qt.UserRole)
            menu = RightClickPopup(self, path=path)
            menu.move(event.globalPos())
            menu.show()

    def set_asset_mode(self):
        self.asset_or_shot = "assets"
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                new_path = data.get("active_project_path", "")
                new_path = os.path.join(new_path, self.asset_or_shot)
                if new_path and new_path != self.current_path:
                    self.update_path(new_path)
            except Exception as e:
                print(f"Erreur lecture JSON projet actif : {e}")

    def set_shot_mode(self):
        self.asset_or_shot = "shots"
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                new_path = data.get("active_project_path", "")
                new_path = os.path.join(new_path, self.asset_or_shot)
            except Exception as e:
                print(f"Erreur lecture JSON projet actif : {e}")
        self.update_path(new_path)

    def switchshot(self):
        self.asset_or_shot = "shots"
        self.setHeaderLabel("Shot")
        print(f"Switched to shot mode : {self.asset_or_shot}")

    def switchasset(self):
        self.asset_or_shot = "assets"
        self.setHeaderLabel("Asset")
        print(f"Switched to asset mode : {self.asset_or_shot}")
