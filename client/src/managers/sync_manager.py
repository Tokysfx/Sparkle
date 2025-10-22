"""
Sync Manager Module

Handles all synchronization operations including:
- Publishing assets, departments, and tasks to server
- Downloading assets, departments, and tasks from server
- Server communication for folder creation
"""

import os
from src.config import configSparkle
from src.connection_manager import connection_manager


class SyncManager:
    """
    Manages synchronization operations between local and server.
    
    This class handles publish/download operations for assets,
    departments, and tasks with the server.
    """
    
    def __init__(self, production_folder):
        """
        Initialize SyncManager with production folder path.
        
        Args:
            production_folder (str): Path to the 02_Production folder
        """
        self.production_folder = production_folder
    
    def _get_project_name(self):
        """
        Get current project name from configuration.
        
        Returns:
            str: Current project name
        """
        config = configSparkle()
        current_config = config.load_config()
        folder_path = current_config.get("project_active_folder", "")
        return os.path.basename(folder_path)
    
    def publish_asset(self, folder_name, asset_name):
        """
        Publish (create) an asset folder on the server.
        
        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name to publish
            
        Returns:
            bool: True if successful, False otherwise
        """
        project_name = self._get_project_name()
        
        # Create folder structure on server using the correct endpoint format
        folder_path = f"{folder_name}/{asset_name}"
        
        response = connection_manager.make_post_request(
            f"/create_folder/{project_name}/{folder_path}"
        )
        
        if response and response.get("message"):
            print(f"INFO: Published asset '{asset_name}' to server")
            return True
        else:
            print(f"ERROR: Failed to publish asset '{asset_name}'")
            return False
    
    def download_asset(self, folder_name, asset_name):
        """
        Download (create) an asset folder locally.
        
        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name to download
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create local folder structure
            local_path = os.path.join(self.production_folder, folder_name, asset_name)
            os.makedirs(local_path, exist_ok=True)
            
            print(f"INFO: Downloaded asset '{asset_name}' locally")
            return True
        except Exception as e:
            print(f"ERROR: Failed to download asset '{asset_name}': {e}")
            return False
    
    def publish_department(self, folder_name, asset_name, department_name):
        """
        Publish (create) a department folder on the server.
        
        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            department_name (str): Department name to publish
            
        Returns:
            bool: True if successful, False otherwise
        """
        project_name = self._get_project_name()
        
        # Create folder structure on server using the correct endpoint format
        folder_path = f"{folder_name}/{asset_name}/{department_name}"
        
        response = connection_manager.make_post_request(
            f"/create_folder/{project_name}/{folder_path}"
        )
        
        if response and response.get("message"):
            print(f"INFO: Published department '{department_name}' to server")
            return True
        else:
            print(f"ERROR: Failed to publish department '{department_name}'")
            return False
    
    def download_department(self, folder_name, asset_name, department_name):
        """
        Download (create) a department folder locally.
        
        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            department_name (str): Department name to download
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create local folder structure
            local_path = os.path.join(self.production_folder, folder_name, asset_name, department_name)
            os.makedirs(local_path, exist_ok=True)
            
            print(f"INFO: Downloaded department '{department_name}' locally")
            return True
        except Exception as e:
            print(f"ERROR: Failed to download department '{department_name}': {e}")
            return False
    
    def publish_task(self, folder_name, asset_name, department_name, task_name):
        """
        Publish (create) a task folder on the server.
        
        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            department_name (str): Department name
            task_name (str): Task name to publish
            
        Returns:
            bool: True if successful, False otherwise
        """
        project_name = self._get_project_name()
        
        # Create folder structure on server using the correct endpoint format
        folder_path = f"{folder_name}/{asset_name}/{department_name}/{task_name}"
        
        response = connection_manager.make_post_request(
            f"/create_folder/{project_name}/{folder_path}"
        )
        
        if response and response.get("message"):
            print(f"INFO: Published task '{task_name}' to server")
            return True
        else:
            print(f"ERROR: Failed to publish task '{task_name}'")
            return False
    
    def download_task(self, folder_name, asset_name, department_name, task_name):
        """
        Download (create) a task folder locally.
        
        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            department_name (str): Department name
            task_name (str): Task name to download
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create local folder structure
            local_path = os.path.join(self.production_folder, folder_name, asset_name, department_name, task_name)
            os.makedirs(local_path, exist_ok=True)
            
            print(f"INFO: Downloaded task '{task_name}' locally")
            return True
        except Exception as e:
            print(f"ERROR: Failed to download task '{task_name}': {e}")
            return False
        
    def publish_file(self, folder_name, asset_name, department_name, task_name, file_name):
        """
        Publish upload a file on the server

        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            department_name (str): Department name
            task_name (str): Task name
            file_name (str): File to Publish

        Returns:
            bool: True if succesful, False otherwise
        """
        project_name = self._get_project_name()
        server_path = f"{folder_name}/{asset_name}/{department_name}/{task_name}/{file_name}"
        local_path = os.path.join(self.production_folder, folder_name, asset_name, department_name, task_name, file_name)

        success = connection_manager.upload_file_to_server(
            f"/upload/{project_name}/{server_path}",
            local_path
        )
        if success:
            return True
        else:
            return False
    
    def download_file(self, folder_name, asset_name, department_name, task_name, file_name):
        """
        Publish upload a file on the server

        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            department_name (str): Department name
            task_name (str): Task name
            file_name (str): File to download

        Returns:
            bool: True if succesful, False otherwise
        """

        project_name = self._get_project_name()
        server_path = f"{folder_name}/{asset_name}/{department_name}/{task_name}/{file_name}"
        local_path = os.path.join(self.production_folder, folder_name, asset_name, department_name, task_name, file_name)
        
        # Use the new download method from connection_manager
        success = connection_manager.download_file_from_server(
            f"/download/{project_name}/{server_path}",
            local_path
        )
        if success:
            return True
        else:
            return False