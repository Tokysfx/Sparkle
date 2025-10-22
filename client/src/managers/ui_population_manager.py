"""
UI Population Manager Module

Handles UI widget population and visual feedback:
- Populating asset tree with color coding
- Populating department and task lists
- Visual status indicators
"""

from PySide6.QtWidgets import QTreeWidgetItem, QListWidgetItem
from PySide6.QtGui import QBrush, QColor


class UIPopulationManager:
    """
    Manages population of UI widgets with data and visual feedback.
    
    This class handles populating tree widgets and lists with appropriate
    color coding based on sync status.
    """
    
    @staticmethod
    def populate_asset_tree(asset_tree, local_assets, server_assets, asset_manager):
        """
        Populate asset tree with local and server data, applying color coding.
        
        Args:
            asset_tree: QTreeWidget to populate
            local_assets (dict): Local assets data
            server_assets (dict): Server assets data
            asset_manager: AssetManager instance for status detection
        """
        # Get all unique folder types from both sources
        all_folders = set(local_assets.keys()) | set(server_assets.keys())
        
        for folder_name in sorted(all_folders):
            folder_item = QTreeWidgetItem(asset_tree)
            folder_item.setText(0, folder_name)
            
            # Get all unique assets in this folder from both sources
            local_set = local_assets.get(folder_name, set())
            server_set = set(server_assets.get(folder_name, []))  # Convert to set
            all_assets = local_set | server_set
            
            for asset_name in sorted(all_assets):
                asset_item = QTreeWidgetItem(folder_item)
                asset_item.setText(0, asset_name)
                
                # Apply color coding based on sync status
                # Use advanced status for detailed feedback
                status_info = asset_manager.get_advanced_asset_status(folder_name, asset_name, local_assets, server_assets)
                color = UIPopulationManager._get_status_color(status_info['status'])
                asset_item.setForeground(0, QBrush(color))
                asset_item.setToolTip(0, status_info['tooltip'])
    
    @staticmethod
    def populate_department_list(department_list, local_departments, server_departments, asset_manager=None, folder_name=None, asset_name=None):
        """
        Populate department list with color coding based on sync status.
        
        Args:
            department_list: QListWidget to populate
            local_departments (set): Set of local department names
            server_departments (set): Set of server department names
            asset_manager: AssetManager instance for advanced status (optional)
            folder_name (str): Asset type folder name (optional)
            asset_name (str): Asset name (optional)
        """
        department_list.clear()
        
        # Get all unique departments from both sources
        all_departments = local_departments | server_departments
        
        for department_name in sorted(all_departments):
            item = QListWidgetItem(department_name)
            
            if asset_manager and folder_name and asset_name:
                # Use advanced status with tooltips
                status_info = asset_manager.get_advanced_department_status(folder_name, asset_name, department_name)
                color = UIPopulationManager._get_status_color(status_info['status'])
                item.setForeground(QBrush(color))
                item.setToolTip(status_info['tooltip'])
            else:
                # Fallback to basic color coding
                if department_name in local_departments and department_name in server_departments:
                    item.setForeground(QBrush(QColor(255, 165, 0)))  # Orange
                elif department_name in local_departments:
                    item.setForeground(QBrush(QColor(255, 255, 255)))  # White
                else:
                    item.setForeground(QBrush(QColor(0, 0, 0)))  # Black
            
            department_list.addItem(item)
    
    @staticmethod
    def populate_task_list(task_list, local_tasks, server_tasks, asset_manager=None, folder_name=None, asset_name=None, department_name=None):
        """
        Populate task list with color coding based on sync status.
        
        Args:
            task_list: QListWidget to populate
            local_tasks (set): Set of local task names
            server_tasks (set): Set of server task names
            asset_manager: AssetManager instance for advanced status (optional)
            folder_name (str): Asset type folder name (optional)
            asset_name (str): Asset name (optional)
            department_name (str): Department name (optional)
        """
        task_list.clear()
        
        # Get all unique tasks from both sources
        all_tasks = local_tasks | server_tasks
        
        for task_name in sorted(all_tasks):
            item = QListWidgetItem(task_name)
            
            if asset_manager and folder_name and asset_name and department_name:
                # Use advanced status with tooltips
                status_info = asset_manager.get_advanced_task_status(folder_name, asset_name, department_name, task_name)
                color = UIPopulationManager._get_status_color(status_info['status'])
                item.setForeground(QBrush(color))
                item.setToolTip(status_info['tooltip'])
            else:
                # Fallback to basic color coding
                if task_name in local_tasks and task_name in server_tasks:
                    item.setForeground(QBrush(QColor(255, 165, 0)))  # Orange
                elif task_name in local_tasks:
                    item.setForeground(QBrush(QColor(255, 255, 255)))  # White
                else:
                    item.setForeground(QBrush(QColor(0, 0, 0)))  # Black
            
            task_list.addItem(item)
    
    @staticmethod
    def populate_file_list(file_list, local_files, server_files):
        """
        Populate file list with color coding based on sync status.
        
        Args:
            file_list: QListWidget to populate
            local_files (set): Set of local file names
            server_files (set): Set of server file names
        """
        file_list.clear()
        
        # Get all unique files from both sources
        all_files = local_files | server_files
        
        for file_name in sorted(all_files):
            item = QListWidgetItem(file_name)
            
            # Apply color coding based on presence in local/server
            if file_name in local_files and file_name in server_files:
                # Synced - Orange
                item.setForeground(QBrush(QColor(255, 165, 0)))
            elif file_name in local_files:
                # Local only - White (default)
                item.setForeground(QBrush(QColor(255, 255, 255)))
            else:
                # Server only - Black
                item.setForeground(QBrush(QColor(0, 0, 0)))
            
            file_list.addItem(item)

    @staticmethod
    def populate_file_list_advanced(file_list, local_files, server_files, asset_manager, folder_name, asset_name, department_name, task_name):
        """
        Populate file list with advanced color coding and tooltips.
        
        Args:
            file_list: QListWidget to populate
            local_files (set): Set of local file names
            server_files (set): Set of server file names
            asset_manager: AssetManager instance for advanced status detection
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            department_name (str): Department name
            task_name (str): Task name
        """
        file_list.clear()
        
        # Get all unique files from both sources
        all_files = local_files | server_files
        
        for file_name in sorted(all_files):
            item = QListWidgetItem(file_name)
            
            # Get advanced status with conflict detection
            status_info = asset_manager.get_advanced_file_status(
                folder_name, asset_name, department_name, task_name, file_name
            )
            
            # Apply advanced color coding
            color = UIPopulationManager._get_status_color(status_info['status'])
            item.setForeground(QBrush(color))
            item.setToolTip(status_info['tooltip'])
            
            file_list.addItem(item)
    
    @staticmethod
    def _get_status_color(status):
        """
        Get color for a given sync status.
        
        Args:
            status (str): Sync status ('synced', 'local_only', 'server_only', 'needs_sync', 'conflict')
            
        Returns:
            QColor: Color for the status
        """
        if status == "synced":
            return QColor(255, 165, 0)  # Orange - Synchronized
        elif status == "local_only":
            return QColor(255, 255, 255)  # White - Local only
        elif status == "server_only":
            return QColor(0, 0, 0)  # Black - Server only
        elif status == "needs_sync":
            return QColor(255, 255, 0)  # Yellow - Needs synchronization
        elif status == "conflict":
            return QColor(255, 0, 0)  # Red - Conflict detected
        else:
            return QColor(128, 128, 128)  # Gray - Unknown status