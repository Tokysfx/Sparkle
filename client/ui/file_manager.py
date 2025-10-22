"""
File Manager UI Module

This module provides a professional 4-column file browser interface for the Sparkle
3D Pipeline Management System. This is the UI layer only - all business logic
is handled by specialized managers in src/managers/.

Features:
- 4-column hierarchical file browser (Assets/Departments/Tasks/Files)
- Intelligent server connection with local fallback
- Visual sync status indicators (local, synced, server-only)
- Smart refresh system with selection preservation
- Context menus for CRUD operations
"""


from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                               QLabel, QTreeWidget, QTreeWidgetItem, QMenu, 
                               QMessageBox, QPushButton)
from PySide6.QtGui import QBrush, QColor
from PySide6.QtCore import Signal, Qt, QTimer

# UI imports
from ui.ui_utility import stylesheet
from ui.connection_indicator import ConnectionIndicator

# Manager imports
from src.managers.asset_manager import AssetManager
from src.managers.sync_manager import SyncManager
from src.managers.selection_manager import SelectionManager
from src.managers.ui_population_manager import UIPopulationManager
from src.operations.crud_operations import (CreateAssetDialog, CreateDepartmentDialog, 
                                          CreateTaskDialog, DeleteOperations)

# Core imports
from src.config import configSparkle
from src.connection_manager import connection_manager
import os

class FileManager(QWidget):
    """
    Main file manager widget providing a 4-column browser interface.
    
    This widget manages the UI layer only. All business logic is delegated
    to specialized managers for better maintainability.
    """
    
    def __init__(self):
        """
        Initialize the FileManager widget.
        
        Sets up the 4-column layout, managers, and initial data loading.
        """
        super().__init__()
        
        # Initialize configuration and paths
        config = configSparkle()
        current_config = config.load_config()
        self.project_folder = current_config.get("project_active_folder", "")
        self.production_folder = os.path.join(self.project_folder, "02_Production")
        
        # Initialize managers
        self._setup_managers()

        # Setup main layout
        layout = QVBoxLayout()

        # Create top toolbar with connection indicator and refresh button
        btn_layout = QHBoxLayout()
        
        # Connection status indicator on the left
        self.connection_indicator = ConnectionIndicator()
        btn_layout.addWidget(self.connection_indicator)
        
        # Spacer to push refresh button to the right
        btn_layout.addStretch()
        
        # Manual refresh button on the right
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.asset_manager.clear_all_caches)
        refresh_btn.clicked.connect(self.refresh_all)
        btn_layout.addWidget(refresh_btn)
        
        layout.addLayout(btn_layout)

        # Setup 4-column browser layout
        layout_tree = QHBoxLayout()

        # Column 1: Asset Tree (hierarchical folders and assets)
        self.asset_tree = QTreeWidget()
        self.asset_tree.setHeaderLabel("Asset")
        self.asset_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.asset_tree.customContextMenuRequested.connect(self.asset_menu)
        self.asset_tree.itemSelectionChanged.connect(self.on_asset_selection_changed)
        layout_tree.addWidget(self.asset_tree)

        # Column 2: Department List
        department_layout = QVBoxLayout()
        department_label = QLabel("Department")
        self.department_list = QListWidget()
        self.department_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.department_list.customContextMenuRequested.connect(self.department_menu)
        self.department_list.itemSelectionChanged.connect(self.on_department_selection_changed)
        department_layout.addWidget(department_label)
        department_layout.addWidget(self.department_list)
        layout_tree.addLayout(department_layout)

        # Column 3: Task List
        task_layout = QVBoxLayout()
        task_label = QLabel("Task")
        self.task_list = QListWidget()
        self.task_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.task_list.customContextMenuRequested.connect(self.task_menu)
        self.task_list.itemSelectionChanged.connect(self.on_task_selection_changed)
        task_layout.addWidget(task_label)
        task_layout.addWidget(self.task_list)
        layout_tree.addLayout(task_layout)

        # Column 4: File List
        file_layout = QVBoxLayout()
        file_label = QLabel("File")
        self.file_list = QListWidget()
        self.file_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_list.customContextMenuRequested.connect(self.file_menu)
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.file_list)
        layout_tree.addLayout(file_layout)

        layout.addLayout(layout_tree)

        self.setLayout(layout)
        
        # Initialize connection management and auto-refresh system
        self._setup_connection_management()
        
        # Load initial data
        self.load_assets()

    def _setup_managers(self):
        """
        Initialize all manager instances.
        
        Creates instances of specialized managers and sets up their configurations.
        """
        # Business logic managers
        self.asset_manager = AssetManager(self.production_folder)
        self.sync_manager = SyncManager(self.production_folder)
        
        # UI manager will be initialized after widgets are created
        self.selection_manager = None

    def _setup_connection_management(self):
        """
        Setup connection management system with intelligent server detection.
        
        Configures the connection manager, auto-refresh timer, and initializes
        server connection based on configuration.
        """
        # Connect to connection manager signals before configuration
        connection_manager.connection_changed.connect(self.on_connection_changed)
        
        # Setup auto-refresh timer (only active when connected to server)
        self.auto_refresh_timer = QTimer()
        self.auto_refresh_timer.timeout.connect(self.refresh_all)
        
        # Initialize connection manager with server configuration
        config = configSparkle()
        current_config = config.load_config()
        server_url = current_config.get("url", "")
        
        # Initialize SelectionManager now that UI components exist
        ui_components = {
            'asset_tree': self.asset_tree,
            'department_list': self.department_list,
            'task_list': self.task_list
        }
        self.selection_manager = SelectionManager(ui_components)
        
        if server_url:
            print(f"INFO: Server configuration detected: {server_url}")
            self.connection_indicator.set_status("checking")
            connection_manager.set_server_url(server_url)
        else:
            print("WARNING: No server URL configured")
            self.connection_indicator.set_status("disconnected")
        
        # Start periodic connection checks every 30 seconds
        connection_manager.start_auto_check(30)

    # =============================================================================
    # CONNECTION MANAGEMENT METHODS
    # =============================================================================
    
    def update_connection_indicator(self, status):
        """
        Update the connection status indicator.
        
        Args:
            status (str): Connection status ('connected', 'disconnected', 'checking')
        """
        self.connection_indicator.set_status(status)

    def on_connection_changed(self, connected):
        """
        Handle connection state changes.
        
        Manages auto-refresh behavior and updates UI based on connection status.
        - Connected: Enable auto-refresh every 15 seconds
        - Disconnected: Disable auto-refresh, manual refresh only
        
        Args:
            connected (bool): True if connected to server, False if local mode
        """
        print(f"INFO: Connection status changed - connected: {connected}")
        
        if connected:
            # Collaborative mode: enable auto-refresh every 15 seconds
            self.auto_refresh_timer.setInterval(15000)
            self.auto_refresh_timer.start()
            self.update_connection_indicator("connected")
            print("INFO: Collaborative mode activated - Auto-refresh enabled")
        else:
            # Local mode: disable auto-refresh
            self.auto_refresh_timer.stop()
            self.update_connection_indicator("disconnected")
            print("INFO: Local mode activated - Manual refresh only")

    # =============================================================================
    # DATA REFRESH AND SELECTION MANAGEMENT
    # =============================================================================
    
    def refresh_all(self):
        """
        Refresh all data while preserving current selections and tree expansion state.
        
        This method delegates to the SelectionManager to save/restore UI state
        while reloading data from managers.
        """
        # Save current UI state
        saved_selection = self.selection_manager.save_current_selection()
        expanded_folders = self.selection_manager.save_tree_expanded_state()
        
        # Reload all data
        self.load_assets()
        
        # Restore UI state
        self.selection_manager.restore_tree_expanded_state(expanded_folders)
        
        callbacks = {
            'on_asset_selection_changed': self.on_asset_selection_changed,
            'on_department_selection_changed': self.on_department_selection_changed,
            'on_task_selection_changed': self.on_task_selection_changed
        }
        self.selection_manager.restore_selection(saved_selection, callbacks)

    # =============================================================================
    # DATA LOADING AND POPULATION METHODS
    # =============================================================================
    
    def load_assets(self):
        """
        Load and display assets from both local and server sources.
        
        Uses AssetManager to fetch data and UIPopulationManager to populate the tree.
        """
        self.asset_tree.clear()
        
        # Get project configuration
        config = configSparkle()
        current_config = config.load_config()
        folder_path = current_config.get("project_active_folder", "")
        project_name = os.path.basename(folder_path)

        # Get assets from managers
        local_assets = self.asset_manager.get_local_assets()
        server_assets = self.asset_manager.get_server_assets(project_name)

        # Populate UI using manager
        UIPopulationManager.populate_asset_tree(
            self.asset_tree, local_assets, server_assets, self.asset_manager
        )


    # =============================================================================
    # SELECTION CHANGE HANDLERS
    # =============================================================================
    
    def on_asset_selection_changed(self):
        """
        Handle asset selection change and populate departments.
        
        Clears dependent columns and loads departments for the selected asset
        from both local and server sources with appropriate color coding.
        """
        # Clear dependent columns
        self.department_list.clear()
        self.task_list.clear()
        self.file_list.clear()

        # Get current selection and project info
        asset = self.asset_tree.currentItem()
        if asset is None:
            print("DEBUG: No asset selected")
            return

        folder = asset.parent()
        if folder is None:
            return
        
        asset_name = asset.text(0)
        folder_name = folder.text(0)

        # Load departments for this asset
        self._load_departments(folder_name, asset_name)

    def _load_departments(self, folder_name, asset_name):
        """
        Load departments for the specified asset using managers.
        
        Args:
            folder_name (str): Name of the asset type folder
            asset_name (str): Name of the specific asset
        """
        # Get project configuration
        config = configSparkle()
        current_config = config.load_config()
        folder_path = current_config.get("project_active_folder", "")
        project_name = os.path.basename(folder_path)
        
        # Get departments from managers
        local_departments = self.asset_manager.get_local_departments(folder_name, asset_name)
        server_departments = self.asset_manager.get_server_departments(project_name, folder_name, asset_name)

        # Populate UI using manager with advanced tooltips
        UIPopulationManager.populate_department_list(
            self.department_list, local_departments, server_departments,
            self.asset_manager, folder_name, asset_name
        )


    def on_department_selection_changed(self):
        """
        Handle department selection change and populate tasks.
        
        Clears dependent columns and loads tasks for the selected department
        from both local and server sources with appropriate color coding.
        """
        # Clear dependent columns
        self.task_list.clear()
        self.file_list.clear()

        # Get current selection hierarchy
        asset = self.asset_tree.currentItem()
        department = self.department_list.currentItem()
        
        if asset is None or department is None:
            return
            
        folder = asset.parent()
        if folder is None:
            return

        asset_name = asset.text(0)
        folder_name = folder.text(0)
        department_name = department.text()

        # Load tasks for this department
        self._load_tasks(folder_name, asset_name, department_name)

    def _load_tasks(self, folder_name, asset_name, department_name):
        """
        Load tasks for the specified department using managers.
        
        Args:
            folder_name (str): Name of the asset type folder
            asset_name (str): Name of the specific asset
            department_name (str): Name of the department
        """
        # Get project configuration
        config = configSparkle()
        current_config = config.load_config()
        folder_path = current_config.get("project_active_folder", "")
        project_name = os.path.basename(folder_path)

        # Get tasks from managers
        local_tasks = self.asset_manager.get_local_tasks(folder_name, asset_name, department_name)
        server_tasks = self.asset_manager.get_server_tasks(project_name, folder_name, asset_name, department_name)

        # Populate UI using manager with advanced tooltips
        UIPopulationManager.populate_task_list(
            self.task_list, local_tasks, server_tasks,
            self.asset_manager, folder_name, asset_name, department_name
        )


    def on_task_selection_changed(self):
        """
        Handle task selection change and populate files.
        
        Loads files for the selected task from both local and server sources
        with appropriate color coding.
        """
        # Clear file list
        self.file_list.clear()

        # Get current selection hierarchy
        asset = self.asset_tree.currentItem()
        department = self.department_list.currentItem() 
        task = self.task_list.currentItem()
        
        if asset is None or department is None or task is None:
            return
            
        folder = asset.parent()
        if folder is None:
            return

        asset_name = asset.text(0)
        folder_name = folder.text(0)
        department_name = department.text()
        task_name = task.text()

        # Load files for this task
        self._load_files(folder_name, asset_name, department_name, task_name)

    def _load_files(self, folder_name, asset_name, department_name, task_name):
        """
        Load files for the specified task using managers.
        
        Args:
            folder_name (str): Name of the asset type folder
            asset_name (str): Name of the specific asset
            department_name (str): Name of the department
            task_name (str): Name of the task
        """
        # Get project configuration
        config = configSparkle()
        current_config = config.load_config()
        folder_path = current_config.get("project_active_folder", "")
        project_name = os.path.basename(folder_path)

        # Get files from managers
        local_files = self.asset_manager.get_local_files(folder_name, asset_name, department_name, task_name)
        server_files = self.asset_manager.get_server_files(project_name, folder_name, asset_name, department_name, task_name)

        # Populate UI using advanced manager with conflict detection
        UIPopulationManager.populate_file_list_advanced(
            self.file_list, local_files, server_files, self.asset_manager,
            folder_name, asset_name, department_name, task_name
        )

    # =============================================================================
    # SYNC STATUS AND UPLOAD/DOWNLOAD METHODS
    # =============================================================================
    
    def publish_asset(self, folder_name, asset_name):
        """
        Publish (upload) a local asset folder structure to the server.
        
        Creates the complete folder structure on the server, including empty folders,
        and uploads any files found within the asset.
        
        Args:
            folder_name (str): Asset type folder name (Chara, Props, etc.)
            asset_name (str): Asset name to publish
        """
        print(f"INFO: Publishing asset {asset_name} from {folder_name} to server...")
        
        # Use SyncManager to handle the publish operation
        success = self.sync_manager.publish_asset(folder_name, asset_name)
        
        if success:
            message = f"Asset {asset_name} published successfully!"
            QMessageBox.information(self, "Publish Complete", message)
        else:
            message = f"Failed to publish asset {asset_name}"
            QMessageBox.warning(self, "Publish Failed", message)
        
        print(f"INFO: Publish complete")
        self.asset_manager.clear_all_caches()
        self.refresh_all()

    def download_asset(self, folder_name, asset_name):
        """
        Download a server asset to local.
        
        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name to download
        """
        print(f"INFO: Downloading asset {asset_name} from server to {folder_name}...")
        
        # Use SyncManager to handle the download operation
        success = self.sync_manager.download_asset(folder_name, asset_name)
        
        if success:
            message = f"Asset {asset_name} downloaded successfully!"
            QMessageBox.information(self, "Download Complete", message)
        else:
            message = f"Failed to download asset {asset_name}"
            QMessageBox.warning(self, "Download Failed", message)
            
        print(f"INFO: Download complete")
        self.refresh_all()

    def sync_asset(self, folder_name, asset_name):
        """
        Synchronize asset between local and server (bidirectional).
        
        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name to sync
        """
        print(f"INFO: Syncing asset {asset_name} in {folder_name}...")
        
        # For now, simple sync: upload local changes, then download server changes
        self.publish_asset(folder_name, asset_name)
        self.download_asset(folder_name, asset_name)
        
        QMessageBox.information(self, "Sync Complete", f"Asset {asset_name} synchronized!")

    def publish_department(self, folder_name, asset_name, department_name):
        """
        Publish (create) a local department folder to the server.
        
        Args:
            folder_name (str): Asset type folder name (Chara, Props, etc.)
            asset_name (str): Asset name
            department_name (str): Department name to publish
        """
        print(f"INFO: Publishing department {department_name} for asset {asset_name} to server...")
        
        # Use SyncManager to handle the publish operation
        success = self.sync_manager.publish_department(folder_name, asset_name, department_name)
        
        if success:
            message = f"Department {department_name} published successfully!"
            QMessageBox.information(self, "Publish Complete", message)
        else:
            message = f"Failed to publish department {department_name}"
            QMessageBox.warning(self, "Publish Failed", message)
        
        print(f"INFO: Department publish complete")
        self.asset_manager.clear_all_caches()
        self.refresh_all()

    def download_department(self, folder_name, asset_name, department_name):
        """
        Download (create) a server department folder to local.
        
        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            department_name (str): Department name to download
        """
        # Use SyncManager to handle the download operation
        success = self.sync_manager.download_department(folder_name, asset_name, department_name)
        
        if success:
            message = f"Department {department_name} downloaded successfully!"
            QMessageBox.information(self, "Download Complete", message)
        else:
            message = f"Failed to download department {department_name}"
            QMessageBox.warning(self, "Download Failed", message)
        
        print(f"INFO: Department download complete")
        self.refresh_all()

    def publish_task(self, folder_name, asset_name, department_name, task_name):
        """
        Publish (create) a local task folder to the server using SyncManager.
        
        Args:
            folder_name (str): Asset type folder name (Chara, Props, etc.)
            asset_name (str): Asset name
            department_name (str): Department name
            task_name (str): Task name to publish
        """
        print(f"INFO: Publishing task {task_name} for {asset_name}/{department_name} to server...")
        
        # Use SyncManager to handle the publish operation
        success = self.sync_manager.publish_task(folder_name, asset_name, department_name, task_name)
        
        if success:
            message = f"Task {task_name} published successfully!"
            QMessageBox.information(self, "Publish Complete", message)
        else:
            message = f"Failed to publish task {task_name}"
            QMessageBox.warning(self, "Publish Failed", message)
        
        print(f"INFO: Task publish complete")
        self.asset_manager.clear_all_caches()
        self.refresh_all()

    def download_task(self, folder_name, asset_name, department_name, task_name):
        """
        Download (create) a server task folder to local.
        
        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            department_name (str): Department name
            task_name (str): Task name to download
        """
        # Use SyncManager to handle the download operation
        success = self.sync_manager.download_task(folder_name, asset_name, department_name, task_name)
        
        if success:
            message = f"Task {task_name} downloaded successfully!"
            QMessageBox.information(self, "Download Complete", message)
        else:
            message = f"Failed to download task {task_name}"
            QMessageBox.warning(self, "Download Failed", message)
        
        print(f"INFO: Task download complete")
        self.refresh_all()

    def publish_file(self, folder_name, asset_name, department_name, task_name, file_name):

        success = self.sync_manager.publish_file(folder_name, asset_name, department_name, task_name, file_name)

        if success:
            message = f"File {file_name} published successfully!"
            QMessageBox.information(self, "Publish Complete", message)
        else:
            message = f"Failed to publish file {file_name}"
            QMessageBox.warning(self, "Publish Failed", message)
        
        print(f"INFO: File publish complete")
        self.refresh_all()

    def download_file(self, folder_name, asset_name, department_name, task_name, file_name):

        success = self.sync_manager.download_file(folder_name, asset_name, department_name, task_name, file_name)

        if success:
            message = f"File {file_name} download successfully!"
            QMessageBox.information(self, "Download Complete", message)
        else:
            message = f"Failed to download file {file_name}"
            QMessageBox.warning(self, "Download Failed", message)
        
        print(f"INFO: File download complete")
        self.refresh_all()


    # =============================================================================
    # CONTEXT MENU HANDLERS
    # =============================================================================

    def asset_menu(self, position):
        """
        Show context menu for asset tree items.
        
        Args:
            position (QPoint): Position where the menu was requested
        """

        # Retrieve clicked asset
        asset_item = self.asset_tree.itemAt(position)
        if not asset_item or not asset_item.parent():
            return # We only use asset not parent folder

        # Retrieve asset name
        asset_name = asset_item.text(0)
        folder_name = asset_item.parent().text(0)

        # Get status using AssetManager
        local_assets = self.asset_manager.get_local_assets()
        
        config = configSparkle()
        current_config = config.load_config()
        folder_path = current_config.get("project_active_folder", "")
        project_name = os.path.basename(folder_path)
        server_assets = self.asset_manager.get_server_assets(project_name)
        
        status = self.asset_manager.get_asset_status(folder_name, asset_name, local_assets, server_assets)

        asset_menu = QMenu()
        new_action = asset_menu.addAction("New Asset")
        new_action.triggered.connect(self.create_new_asset)

        asset_menu.addSeparator()

        # Adding Publish/Download/Sync based on status
        if status == "local_only":
            publish_action = asset_menu.addAction("📤 Publish to Server")
            publish_action.triggered.connect(lambda: self.publish_asset(folder_name, asset_name))
            
        elif status == "server_only":
            download_action = asset_menu.addAction("📥 Download from Server")  
            download_action.triggered.connect(lambda: self.download_asset(folder_name, asset_name))
            
        elif status == "synced":
            sync_action = asset_menu.addAction("🔄 Sync with Server")
            sync_action.triggered.connect(lambda: self.sync_asset(folder_name, asset_name))

        asset_menu.addSeparator()

        # Adding delete action
        delete_action = asset_menu.addAction("Delete")
        delete_action.triggered.connect(self.delete)

        asset_menu.exec(self.asset_tree.mapToGlobal(position))

    def department_menu(self, position):
        """
        Show context menu for department list items with intelligent actions.
        
        Args:
            position (QPoint): Position where the menu was requested
        """
        # Get current selection hierarchy
        asset = self.asset_tree.currentItem()
        department_item = self.department_list.itemAt(position)
        
        if not asset or not asset.parent() or not department_item:
            return
        
        # Get names
        asset_name = asset.text(0)
        folder_name = asset.parent().text(0)
        department_name = department_item.text()
        
        # Get department status using AssetManager
        status = self.asset_manager.get_department_status(folder_name, asset_name, department_name)
        
        # Create menu
        department_menu = QMenu()
        new_action = department_menu.addAction("New Department")
        new_action.triggered.connect(self.create_new_department)
        
        department_menu.addSeparator()
        
        # Adding Publish/Download/Sync based on status
        if status == "local_only":
            publish_action = department_menu.addAction("📤 Publish to Server")
            publish_action.triggered.connect(lambda: self.publish_department(folder_name, asset_name, department_name))
            
        elif status == "server_only":
            download_action = department_menu.addAction("📥 Download from Server")  
            download_action.triggered.connect(lambda: self.download_department(folder_name, asset_name, department_name))
            
        elif status == "synced":
            sync_action = department_menu.addAction("🔄 Sync with Server")
            # For now, sync does both publish and download
            sync_action.triggered.connect(lambda: (
                self.publish_department(folder_name, asset_name, department_name),
                self.download_department(folder_name, asset_name, department_name)
            ))
        
        department_menu.addSeparator()
        
        delete_action = department_menu.addAction("Delete")
        delete_action.triggered.connect(self.delete)

        department_menu.exec(self.department_list.mapToGlobal(position))
    
    def task_menu(self, position):
        """
        Show context menu for task list items with intelligent actions.
        
        Args:
            position (QPoint): Position where the menu was requested
        """
        # Get current selection hierarchy
        asset = self.asset_tree.currentItem()
        department = self.department_list.currentItem()
        task_item = self.task_list.itemAt(position)
        
        if not asset or not asset.parent() or not department or not task_item:
            return
        
        # Get names
        asset_name = asset.text(0)
        folder_name = asset.parent().text(0)
        department_name = department.text()
        task_name = task_item.text()
        
        # Get task status using AssetManager
        status = self.asset_manager.get_task_status(folder_name, asset_name, department_name, task_name)
        
        # Create menu
        task_menu = QMenu()
        new_action = task_menu.addAction("New Task")
        new_action.triggered.connect(self.create_new_task)
        
        task_menu.addSeparator()
        
        # Adding Publish/Download/Sync based on status
        if status == "local_only":
            publish_action = task_menu.addAction("📤 Publish to Server")
            publish_action.triggered.connect(lambda: self.publish_task(folder_name, asset_name, department_name, task_name))
            
        elif status == "server_only":
            download_action = task_menu.addAction("📥 Download from Server")  
            download_action.triggered.connect(lambda: self.download_task(folder_name, asset_name, department_name, task_name))
            
        elif status == "synced":
            sync_action = task_menu.addAction("🔄 Sync with Server")
            # For now, sync does both publish and download
            sync_action.triggered.connect(lambda: (
                self.publish_task(folder_name, asset_name, department_name, task_name),
                self.download_task(folder_name, asset_name, department_name, task_name)
            ))
        
        task_menu.addSeparator()
        
        delete_action = task_menu.addAction("Delete")
        delete_action.triggered.connect(self.delete)

        task_menu.exec(self.task_list.mapToGlobal(position))
    
    def file_menu(self, position):
        """
        Show context menu for file list items.
        
        Args:
            position (QPoint): Position where the menu was requested
        """
        asset = self.asset_tree.currentItem()
        department = self.department_list.currentItem()
        task_item = self.task_list.currentItem()
        file_item = self.file_list.itemAt(position)

        asset_name = asset.text(0)
        folder_name = asset.parent().text(0)
        department_name = department.text()
        task_name = task_item.text()
        file_name = file_item.text()

        # Get file status using local method
        status = self.asset_manager.get_file_status(folder_name, asset_name, department_name, task_name, file_name)

        file_menu = QMenu()
        new_action = file_menu.addAction("New File")

        file_menu.addSeparator()
        
        # Adding Publish/Download/Sync based on status
        if status == "local_only":
            publish_action = file_menu.addAction("📤 Publish to Server")
            publish_action.triggered.connect(lambda: self.publish_file(folder_name, asset_name, department_name, task_name, file_name))
            
        elif status == "server_only":
            download_action = file_menu.addAction("📥 Download from Server")  
            download_action.triggered.connect(lambda: self.download_file(folder_name, asset_name, department_name, task_name, file_name))
            
        elif status == "synced":
            sync_action = file_menu.addAction("🔄 Sync with Server")
            # For now, sync does both publish and download
            sync_action.triggered.connect(lambda: (
                self.publish_task(folder_name, asset_name, department_name, task_name, file_name),
                self.download_task(folder_name, asset_name, department_name, task_name, file_name)
            ))
        
        file_menu.addSeparator()

        delete_action = file_menu.addAction("Delete")

        # TODO: Implement create_new_file method
        # new_action.triggered.connect(self.create_new_file)
        delete_action.triggered.connect(self.delete)

        file_menu.exec(self.file_list.mapToGlobal(position))
    # =============================================================================
    # CRUD OPERATIONS
    # =============================================================================

    def create_new_asset(self):
        """
        Open dialog to create a new asset in the selected folder.
        """
        asset = self.asset_tree.currentItem()
        if asset is None:
            return
            
        folder = asset.parent()
        if folder is None:
            # Selected item is a folder itself
            folder_name = asset.text(0)
        else:
            # Selected item is an asset within a folder
            folder_name = folder.text(0)
        
        folder_path = os.path.join(self.production_folder, folder_name)
        self.create_asset_window = CreateAssetDialog(self, folder_path)
        self.create_asset_window.show()

    def create_new_department(self):
        """
        Open dialog to create a new department for the selected asset.
        """
        asset = self.asset_tree.currentItem()
        if asset is None:
            return
            
        folder = asset.parent()
        if folder is None:
            return
            
        asset_name = asset.text(0)
        folder_name = folder.text(0)
        asset_path = os.path.join(self.production_folder, folder_name, asset_name)

        self.create_department_window = CreateDepartmentDialog(self, asset_path)
        self.create_department_window.show()

    def create_new_task(self):
        """
        Open dialog to create a new task for the selected department.
        """
        asset = self.asset_tree.currentItem()
        department = self.department_list.currentItem()
        
        if asset is None or department is None:
            return
            
        folder = asset.parent()
        if folder is None:
            return
            
        asset_name = asset.text(0)
        folder_name = folder.text(0)
        department_name = department.text()

        department_path = os.path.join(self.production_folder, folder_name, 
                                     asset_name, department_name)

        self.create_task_window = CreateTaskDialog(self, department_path)
        self.create_task_window.show()

    def delete(self):
        """
        Delete the currently selected item.
        
        Delegates to the DeleteOperations class.
        """
        DeleteOperations.delete_item(self)