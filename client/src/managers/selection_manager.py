"""
Selection Manager Module

Handles selection state and tree expansion management:
- Saving and restoring current selections
- Saving and restoring tree expansion states
- Selection restoration across refreshes
"""


class SelectionManager:
    """
    Manages UI selection state and tree expansion.
    
    This class handles saving and restoring selection states
    and tree expansion states across data refreshes.
    """
    
    def __init__(self, ui_components):
        """
        Initialize SelectionManager with UI components.
        
        Args:
            ui_components (dict): Dictionary containing UI widgets
                - asset_tree: QTreeWidget for assets
                - department_list: QListWidget for departments
                - task_list: QListWidget for tasks
        """
        self.asset_tree = ui_components['asset_tree']
        self.department_list = ui_components['department_list']
        self.task_list = ui_components['task_list']
    
    def save_current_selection(self):
        """
        Save current selection state across all columns.
        
        Returns:
            dict: Dictionary containing selection names for each column
        """
        selection = {
            'folder_name': None,
            'asset_name': None,
            'department_name': None,
            'task_name': None
        }
        
        # Save asset selection
        asset_selected = self.asset_tree.currentItem()
        if asset_selected:
            selection['asset_name'] = asset_selected.text(0)
            folder = asset_selected.parent()
            if folder:
                selection['folder_name'] = folder.text(0)
        
        # Save department selection
        department_selected = self.department_list.currentItem()
        if department_selected:
            selection['department_name'] = department_selected.text()
            
        # Save task selection
        task_selected = self.task_list.currentItem()
        if task_selected:
            selection['task_name'] = task_selected.text()

        return selection
    
    def restore_selection(self, selection, callbacks):
        """
        Restore selection state from saved selection data.
        
        Args:
            selection (dict): Previously saved selection state
            callbacks (dict): Dictionary containing callback functions
                - on_asset_selection_changed: Asset selection callback
                - restore_department_selection: Department restore callback
        """
        if not selection['folder_name'] or not selection['asset_name']:
            return
            
        # Restore asset selection
        for i in range(self.asset_tree.topLevelItemCount()):
            folder_item = self.asset_tree.topLevelItem(i)
            if folder_item.text(0) == selection['folder_name']:
                for j in range(folder_item.childCount()):
                    asset_item = folder_item.child(j)
                    if asset_item.text(0) == selection['asset_name']:
                        self.asset_tree.setCurrentItem(asset_item)
                        callbacks['on_asset_selection_changed']()
                        
                        # Restore department selection
                        if selection['department_name']:
                            self._restore_department_selection(
                                selection['department_name'], 
                                selection['task_name'],
                                callbacks
                            )
                        break

    def _restore_department_selection(self, department_name, task_name, callbacks):
        """
        Restore department and task selection.
        
        Args:
            department_name (str): Name of department to select
            task_name (str): Name of task to select (optional)
            callbacks (dict): Dictionary containing callback functions
        """
        for k in range(self.department_list.count()):
            dept_item = self.department_list.item(k)
            if dept_item.text() == department_name:
                self.department_list.setCurrentItem(dept_item)
                callbacks['on_department_selection_changed']()
                
                # Restore task selection if specified
                if task_name:
                    self._restore_task_selection(task_name, callbacks)
                break

    def _restore_task_selection(self, task_name, callbacks):
        """
        Restore task selection.
        
        Args:
            task_name (str): Name of task to select
            callbacks (dict): Dictionary containing callback functions
        """
        for l in range(self.task_list.count()):
            task_item = self.task_list.item(l)
            if task_item.text() == task_name:
                self.task_list.setCurrentItem(task_item)
                callbacks['on_task_selection_changed']()
                break

    def save_tree_expanded_state(self):
        """
        Save the expanded state of all items in the asset tree.
        
        Returns:
            set: Set of folder names that are currently expanded
        """
        expanded_folders = set()
        
        # Iterate through all top-level items (folders)
        for i in range(self.asset_tree.topLevelItemCount()):
            folder_item = self.asset_tree.topLevelItem(i)
            if folder_item.isExpanded():
                expanded_folders.add(folder_item.text(0))
                
        return expanded_folders

    def restore_tree_expanded_state(self, expanded_folders):
        """
        Restore the expanded state of tree items.
        
        Args:
            expanded_folders (set): Set of folder names that should be expanded
        """
        if not expanded_folders:
            return
            
        # Iterate through all top-level items (folders)
        for i in range(self.asset_tree.topLevelItemCount()):
            folder_item = self.asset_tree.topLevelItem(i)
            folder_name = folder_item.text(0)
            
            if folder_name in expanded_folders:
                folder_item.setExpanded(True)