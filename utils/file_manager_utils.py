from PySide6.QtWidgets import QTreeWidgetItem , QTreeWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
import os
import json


def populate_tree(path, parent_widget, max_depth, current_depth=0):
    if current_depth > max_depth:
        return
    try:
        for entry in sorted(os.listdir(path)):
            full_path = os.path.join(path, entry)
            # Création d’un item pour ce fichier ou dossier
            item = QTreeWidgetItem([entry])
            item.setIcon(0, QIcon("folder.png") if os.path.isdir(full_path) else QIcon("file.png"))
            
            item.setData(0, Qt.UserRole, full_path)  # Stocke le chemin complet dans les données de l'item

            # Ajout selon le niveau : racine ou enfant
            if isinstance(parent_widget, QTreeWidget):
                parent_widget.addTopLevelItem(item)
            else:
                parent_widget.addChild(item)

            # Si c’est un dossier et qu’on n’a pas atteint la profondeur max
            if os.path.isdir(full_path) and current_depth < max_depth:
                populate_tree(full_path, item, max_depth, current_depth + 1)

    except Exception as e:
        print(f"Erreur lecture de {path} : {e}")

def refresh_current_directory(self, changed_path):
    print(f"Directory changed: {changed_path}")
    
    # If the changed path is our current directory or a subdirectory
    if (self.current_path and 
        (changed_path == self.current_path or 
            changed_path.startswith(self.current_path + os.sep))):
        
        # Re-add watches as they might be removed when directories are deleted
        if not self.dir_watcher.directories():
            self.update_path(self.current_path)
        else:
            self.refresh_tree()

def get_expanded_paths(tree_widget):
    """Retourne la liste des chemins (tuple de textes) des items expandus dans un QTreeWidget."""
    expanded = []
    def recurse(item, path):
        if item.isExpanded():
            expanded.append(tuple(path + [item.text(0)]))
        for i in range(item.childCount()):
            recurse(item.child(i), path + [item.text(0)])
    root = tree_widget.invisibleRootItem()
    for i in range(root.childCount()):
        recurse(root.child(i), [])
    return expanded

def restore_expanded_paths(tree_widget, expanded_paths):
    """Déplie les items dont le chemin (tuple de textes) est dans expanded_paths dans un QTreeWidget."""
    def recurse(item, path):
        current_path = tuple(path + [item.text(0)])
        if current_path in expanded_paths:
            item.setExpanded(True)
        for i in range(item.childCount()):
            recurse(item.child(i), path + [item.text(0)])
    root = tree_widget.invisibleRootItem()
    for i in range(root.childCount()):
        recurse(root.child(i), [])

