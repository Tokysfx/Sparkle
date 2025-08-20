from PySide6.QtWidgets import QTreeWidget
from PySide6.QtCore import Qt, Signal, QFileSystemWatcher, QTimer
from utils.file_manager_utils import populate_tree
import os
import json

class QTree_Departement (QTreeWidget):

    Departement_selected = Signal(str)
    clear_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderLabel("Departement")
        header = self.headerItem()
        header.setTextAlignment(0, Qt.AlignCenter)
        self.itemClicked.connect(self.handle_item_click)

        self.dir_watcher = QFileSystemWatcher()
        self.dir_watcher.directoryChanged.connect(self.on_directory_changed)
        self.current_path = ""

        ''' Watch json file for project changes '''
        self.json_watcher = QFileSystemWatcher()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        self.json_path = os.path.join(data_dir, "active_project.json")
        if os.path.exists(self.json_path):
            self.json_watcher.addPath(self.json_path)
        with open(self.json_path, 'r') as f:
            data = json.load(f)
            self.currentproject_path = data.get("active_project_path", "")
        self.json_watcher.fileChanged.connect(self.check_path_changes)
        

    def QTree_Departement(self, path: str):

        if path is None:
            path = r""


        ''' Timer Watch json file for project changes '''
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_path_changes)
        self.timer.start(1000)

        self.update_path(path)

    def update_path(self, path):
        max_depth = 0

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

    def handle_item_click(self, item):
        self.clear_signal.emit()
        depth = 0
        current = item
        while current.parent() is not None:
            depth += 1
            current = current.parent()
        if depth == 0:
            departement_path = item.data(0, Qt.UserRole)
            self.Departement_selected.emit(departement_path)
    
    def on_directory_changed(self, changed_path):
        print(f"Directory changed: {changed_path}")
        if self.current_path and (
            changed_path == self.current_path or changed_path.startswith(self.current_path + os.sep)
        ):
            self.update_path(self.current_path)

    def check_path_changes(self):
        #print(f"Checking path changes for: {self.currentproject_path}")
        if os.path.exists(self.json_path):
            with open(self.json_path, 'r') as f:
                data = json.load(f)
                self.new_path = data.get("active_project_path", "")
                #print(f"New path from JSON: {self.new_path}")
                if self.new_path != self.currentproject_path:
                    self.clear()
                    self.currentproject_path = self.new_path
        if self.json_path not in self.json_watcher.files():
            self.json_watcher.addPath(self.json_path)

    def switchshot(self):
        self.clear()
    def switchasset(self):
        self.clear()
