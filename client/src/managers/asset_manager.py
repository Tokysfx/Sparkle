"""
Asset Manager Module

Handles all asset-related data operations including:
- Loading assets from local and server sources
- Asset data population and status detection
- Asset hierarchy management
"""

import os
import time
from datetime import datetime
from src.config import configSparkle
from src.connection_manager import connection_manager


class AssetManager:
    """
    Manages asset data loading, population and status detection.
    
    This class handles all backend operations related to assets,
    departments, tasks and their synchronization status.
    """
    
    def __init__(self, production_folder):
        """
        Initialize AssetManager with production folder path.
        
        Args:
            production_folder (str): Path to the 02_Production folder
        """
        self.production_folder = production_folder
        self.asset_cache = None
        self.department_cache = None
        self.task_cache = None
        self.file_cache = None

        
    def get_local_assets(self):
        """
        Scan local filesystem for assets.
        
        Returns:
            dict: Dictionary mapping asset types to sets of asset names
        """
        local_assets = {}
        
        if not os.path.exists(self.production_folder):
            return local_assets
            
        for asset_type in os.listdir(self.production_folder):
            # Skip shot folders as they're handled separately
            if asset_type == "00_Shot":
                continue
                
            asset_type_path = os.path.join(self.production_folder, asset_type)
            if os.path.isdir(asset_type_path):
                local_assets[asset_type] = set(os.listdir(asset_type_path))
                
        return local_assets
    
    def get_server_assets(self, project_name):
        """
        Fetch assets from server.
        
        Args:
            project_name (str): Name of the current project
            
        Returns:
            dict: Server assets data or empty dict if not connected
        """
        valide = self.is_assetCache_valide()

        if valide == False:
            server_assets = connection_manager.make_request(f"/projects/{project_name}/assets")
            timesstamp = time.time()
            ttl = 60
            self.asset_cache = {
                "data": server_assets,
                "timestamp": timesstamp,
                "ttl": ttl
            }
        else:
            server_assets = self.asset_cache.get("data")
        return server_assets if server_assets is not None else {}
        
    
    def is_assetCache_valide(self):
        """
        Compare time of creation and actual time > ttl of the asset cache

        return:
            if still valide
        """
        
        valide = False
        currentTime = time.time()

        if not self.asset_cache:
            valide = False
        else:
            try:
                timestamp = self.asset_cache.get("timestamp")
                ttl = self.asset_cache.get("ttl")
                interval = currentTime-timestamp
                if interval > ttl:
                    valide = False
                else:
                    valide = True
            except Exception as e:
                print (f"Error - {e}")
        return valide
            

    
    def get_local_departments(self, folder_name, asset_name):
        """
        Get local departments for a specific asset.
        
        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            
        Returns:
            set: Set of department names found locally
        """
        asset_path = os.path.join(self.production_folder, folder_name, asset_name)
        
        if not os.path.exists(asset_path):
            return set()
            
        return {item for item in os.listdir(asset_path) 
                if os.path.isdir(os.path.join(asset_path, item))}
    
    def get_server_departments(self, project_name, folder_name, asset_name):
        """
        Get server departments for a specific asset.
        
        Args:
            project_name (str): Name of the current project
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            
        Returns:
            set: Set of department names found on server
        """
        valide = self.is_departmentCache_valide()
        if valide == False:
            response = connection_manager.make_request(
                f"/projects/{project_name}/{folder_name}/{asset_name}/department"
            )
            if response and "departments" in response:
                timesstamp = time.time()
                ttl = 60
                self.department_cache = {
                    "data": set(response["departments"]),
                    "timestamp": timesstamp,
                    "ttl": ttl,
                    "project_name": project_name,
                    "folder_name": folder_name,
                    "asset_name": asset_name
                }
                return set(response["departments"])
            else:
                return set()
        else:     
            return self.department_cache.get("data", set())
        
    
    def is_departmentCache_valide(self):
        """
        Compare time of creation and actual time > ttl of the department cache

        return:
            if still valide
        """
        
        valide = False
        currentTime = time.time()

        if not self.department_cache:
            valide = False
        else:
            try:
                timestamp = self.department_cache.get("timestamp")
                ttl = self.department_cache.get("ttl")
                interval = currentTime-timestamp
                if interval > ttl:
                    valide = False
                else:
                    valide = True
            except Exception as e:
                print (f"Error - {e}")
        return valide
    
    def get_local_tasks(self, folder_name, asset_name, department_name):
        """
        Get local tasks for a specific department.
        
        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            department_name (str): Department name
            
        Returns:
            set: Set of task names found locally
        """
        dept_path = os.path.join(self.production_folder, folder_name, asset_name, department_name)
        
        if not os.path.exists(dept_path):
            return set()
            
        return {item for item in os.listdir(dept_path) 
                if os.path.isdir(os.path.join(dept_path, item))}
    
    
    def get_server_tasks(self, project_name, folder_name, asset_name, department_name):
        """
        Get server tasks for a specific department.
        
        Args:
            project_name (str): Name of the current project
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            department_name (str): Department name
            
        Returns:
            set: Set of task names found on server
        """

        valide = self.is_taskCache_valide()

        if valide == False:
            response = connection_manager.make_request(
                f"/projects/{project_name}/{folder_name}/{asset_name}/{department_name}/task"
            )
            if response and "task" in response:
                timesstamp = time.time()
                ttl = 60
                self.task_cache = {
                    "data": set(response["task"]),
                    "timestamp": timesstamp,
                    "ttl": ttl,
                    "project_name": project_name,
                    "folder_name": folder_name,
                    "asset_name": asset_name,
                    "department_name": department_name
                }
                return set(response["task"])
            else:
                return set()
        else:
            return self.task_cache.get("data", set())
    
    def is_taskCache_valide(self):
        """
        Compare time of creation and actual time > ttl of the task cache

        return:
            if still valide
        """
        
        valide = False
        currentTime = time.time()

        if not self.task_cache:
            valide = False
        else:
            try:
                timestamp = self.task_cache.get("timestamp")
                ttl = self.task_cache.get("ttl")
                interval = currentTime-timestamp
                if interval > ttl:
                    valide = False
                else:
                    valide = True
            except Exception as e:
                print (f"Error - {e}")
        return valide
    
    def get_local_files(self, folder_name, asset_name, department_name, task_name):
        """
        Get local files for a specific task.
        
        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            department_name (str): Department name
            task_name (str): Task name
            
        Returns:
            set: Set of file names found locally
        """
        task_path = os.path.join(self.production_folder, folder_name, asset_name, department_name, task_name)
        
        if not os.path.exists(task_path):
            return set()
            
        return {item for item in os.listdir(task_path) 
                if os.path.isfile(os.path.join(task_path, item))}
    
    def get_server_files(self, project_name, folder_name, asset_name, department_name, task_name):
        """
        Get server files for a specific task.
        
        Args:
            project_name (str): Name of the current project
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            department_name (str): Department name
            task_name (str): Task name
            
        Returns:
            set: Set of file names found on server
        """

        valide = self.is_fileCache_valide()
        if valide == False: 
            response = connection_manager.make_request(
                f"/projects/{project_name}/{folder_name}/{asset_name}/{department_name}/{task_name}/file"
            )
            if response and "file" in response:
                timesstamp = time.time()
                ttl = 20
                self.file_cache = {
                    "data": set(response["file"]),
                    "timestamp": timesstamp,
                    "ttl": ttl,
                    "project_name": project_name,
                    "folder_name": folder_name,
                    "asset_name": asset_name,
                    "department_name": department_name,
                    "task_name": task_name
                }
                return set(response["file"])
            else:
                return set()
        
        else:
            return self.file_cache.get("data", set())
    
    def is_fileCache_valide(self):
        """
        Compare time of creation and actual time > ttl of the task cache

        return:
            if still valide
        """
        
        valide = False
        currentTime = time.time()

        if not self.file_cache:
            valide = False
        else:
            try:
                timestamp = self.file_cache.get("timestamp")
                ttl = self.file_cache.get("ttl")
                interval = currentTime-timestamp
                if interval > ttl:
                    valide = False
                else:
                    valide = True
            except Exception as e:
                print (f"Error - {e}")
        return valide
    
    def get_asset_status(self, folder_name, asset_name, local_assets, server_assets):
        """
        Determine sync status of a specific asset.
        
        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            local_assets (dict): Local assets data
            server_assets (dict): Server assets data
            
        Returns:
            str: Status - 'local_only', 'server_only', or 'synced'
        """
        local_has = folder_name in local_assets and asset_name in local_assets[folder_name]
        server_has = folder_name in server_assets and asset_name in server_assets[folder_name]
        
        if local_has and server_has:
            return "synced"
        elif local_has:
            return "local_only"
        elif server_has:
            return "server_only"
        else:
            return "unknown"
    
    def get_department_status(self, folder_name, asset_name, department_name):
        """
        Determine sync status of a specific department.
        
        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            department_name (str): Department name
            
        Returns:
            str: Status - 'local_only', 'server_only', or 'synced'
        """
        # Get project name
        config = configSparkle()
        current_config = config.load_config()
        folder_path = current_config.get("project_active_folder", "")
        project_name = os.path.basename(folder_path)
        
        local_departments = self.get_local_departments(folder_name, asset_name)
        server_departments = self.get_server_departments(project_name, folder_name, asset_name)
        
        local_has = department_name in local_departments
        server_has = department_name in server_departments
        
        if local_has and server_has:
            return "synced"
        elif local_has:
            return "local_only"
        elif server_has:
            return "server_only"
        else:
            return "unknown"
    
    def get_task_status(self, folder_name, asset_name, department_name, task_name):
        """
        Determine sync status of a specific task.
        
        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            department_name (str): Department name
            task_name (str): Task name
            
        Returns:
            str: Status - 'local_only', 'server_only', or 'synced'
        """
        # Get project name
        config = configSparkle()
        current_config = config.load_config()
        folder_path = current_config.get("project_active_folder", "")
        project_name = os.path.basename(folder_path)
        
        local_tasks = self.get_local_tasks(folder_name, asset_name, department_name)
        server_tasks = self.get_server_tasks(project_name, folder_name, asset_name, department_name)
        
        local_has = task_name in local_tasks
        server_has = task_name in server_tasks
        
        if local_has and server_has:
            return "synced"
        elif local_has:
            return "local_only"
        elif server_has:
            return "server_only"
        else:
            return "unknown"
        
    def get_file_status(self, folder_name, asset_name, department_name, task_name, file_name):
        """
        Determine sync status of a specific task.
        
        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            department_name (str): Department name
            task_name (str): Task name
            
        Returns:
            str: Status - 'local_only', 'server_only', or 'synced'
        """

        config = configSparkle()
        current_config = config.load_config()
        folder_path = current_config.get("project_active_folder", "")
        project_name = os.path.basename(folder_path)
        
        local_file = self.get_local_files(folder_name, asset_name, department_name, task_name)
        server_file = self.get_server_files(project_name, folder_name, asset_name, department_name, task_name)

        local_has = file_name in local_file
        server_has = file_name in server_file

        if local_has and server_has:
            return "synced"
        elif local_has:
            return "local_only"
        elif server_has:
            return "server_only"
        else:
            return "unknown"


    def get_file_modification_time(self, file_path):
        """
        Get file modification time.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            datetime: Modification time or None if file doesn't exist
        """
        try:
            if os.path.exists(file_path):
                return datetime.fromtimestamp(os.path.getmtime(file_path))
        except Exception:
            pass
        return None
    
    def get_advanced_asset_status(self, folder_name, asset_name, local_assets, server_assets):
        """
        Determine advanced sync status with conflict detection.
        
        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            local_assets (dict): Local assets data
            server_assets (dict): Server assets data
            
        Returns:
            dict: Status info with 'status', 'local_time', 'server_time', 'tooltip'
        """
        local_has = folder_name in local_assets and asset_name in local_assets[folder_name]
        server_has = folder_name in server_assets and asset_name in server_assets[folder_name]
        
        result = {
            'status': 'unknown',
            'local_time': None,
            'server_time': None,
            'tooltip': ''
        }
        
        if local_has and server_has:
            # Both exist - for folders, this means they're synced
            asset_path = os.path.join(self.production_folder, folder_name, asset_name)
            local_time = self.get_file_modification_time(asset_path)
            
            result['status'] = 'synced'
            result['tooltip'] = f"🟠 Asset synchronisé (local: {local_time.strftime('%H:%M') if local_time else 'N/A'})"
                
        elif local_has:
            asset_path = os.path.join(self.production_folder, folder_name, asset_name)
            local_time = self.get_file_modification_time(asset_path)
            result['status'] = 'local_only'
            result['tooltip'] = f"⚪ Asset local uniquement (créé: {local_time.strftime('%H:%M') if local_time else 'N/A'})"
            
        elif server_has:
            result['status'] = 'server_only'
            result['tooltip'] = "⚫ Asset serveur uniquement"
            
        return result
    
    def get_advanced_department_status(self, folder_name, asset_name, department_name):
        """
        Determine advanced sync status for department (folder-based).
        
        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            department_name (str): Department name
            
        Returns:
            dict: Status info with 'status', 'tooltip'
        """
        config = configSparkle()
        current_config = config.load_config()
        folder_path = current_config.get("project_active_folder", "")
        project_name = os.path.basename(folder_path)
        
        local_departments = self.get_local_departments(folder_name, asset_name)
        server_departments = self.get_server_departments(project_name, folder_name, asset_name)
        
        local_has = department_name in local_departments
        server_has = department_name in server_departments
        
        result = {'status': 'unknown', 'tooltip': ''}
        
        if local_has and server_has:
            dept_path = os.path.join(self.production_folder, folder_name, asset_name, department_name)
            mod_time = self.get_file_modification_time(dept_path)
            result['status'] = 'synced'
            result['tooltip'] = f"🟠 Department synchronisé ({mod_time.strftime('%H:%M') if mod_time else 'N/A'})"
                
        elif local_has:
            dept_path = os.path.join(self.production_folder, folder_name, asset_name, department_name)
            mod_time = self.get_file_modification_time(dept_path)
            result['status'] = 'local_only'
            result['tooltip'] = f"⚪ Department local uniquement (créé: {mod_time.strftime('%H:%M') if mod_time else 'N/A'})"
            
        elif server_has:
            result['status'] = 'server_only'
            result['tooltip'] = "⚫ Department serveur uniquement"
            
        return result
    
    def get_advanced_task_status(self, folder_name, asset_name, department_name, task_name):
        """
        Determine advanced sync status for task (folder-based).
        
        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name  
            department_name (str): Department name
            task_name (str): Task name
            
        Returns:
            dict: Status info with 'status', 'tooltip'
        """
        config = configSparkle()
        current_config = config.load_config()
        folder_path = current_config.get("project_active_folder", "")
        project_name = os.path.basename(folder_path)
        
        local_tasks = self.get_local_tasks(folder_name, asset_name, department_name)
        server_tasks = self.get_server_tasks(project_name, folder_name, asset_name, department_name)
        
        local_has = task_name in local_tasks
        server_has = task_name in server_tasks
        
        result = {'status': 'unknown', 'tooltip': ''}
        
        if local_has and server_has:
            task_path = os.path.join(self.production_folder, folder_name, asset_name, department_name, task_name)
            mod_time = self.get_file_modification_time(task_path)
            result['status'] = 'synced'
            result['tooltip'] = f"🟠 Task synchronisé ({mod_time.strftime('%H:%M') if mod_time else 'N/A'})"
                
        elif local_has:
            task_path = os.path.join(self.production_folder, folder_name, asset_name, department_name, task_name)
            mod_time = self.get_file_modification_time(task_path)
            result['status'] = 'local_only'
            result['tooltip'] = f"⚪ Task local uniquement (créé: {mod_time.strftime('%H:%M') if mod_time else 'N/A'})"
            
        elif server_has:
            result['status'] = 'server_only'
            result['tooltip'] = "⚫ Task serveur uniquement"
            
        return result
    
    def get_advanced_file_status(self, folder_name, asset_name, department_name, task_name, file_name):
        """
        Determine advanced sync status for file with conflict detection.
        
        Args:
            folder_name (str): Asset type folder name
            asset_name (str): Asset name
            department_name (str): Department name
            task_name (str): Task name
            file_name (str): File name
            
        Returns:
            dict: Status info with 'status', 'tooltip'
        """
        config = configSparkle()
        current_config = config.load_config()
        folder_path = current_config.get("project_active_folder", "")
        project_name = os.path.basename(folder_path)
        
        local_files = self.get_local_files(folder_name, asset_name, department_name, task_name)
        server_files = self.get_server_files(project_name, folder_name, asset_name, department_name, task_name)
        
        local_has = file_name in local_files
        server_has = file_name in server_files
        
        result = {'status': 'unknown', 'tooltip': ''}
        
        if local_has and server_has:
            file_path = os.path.join(self.production_folder, folder_name, asset_name, department_name, task_name, file_name)
            mod_time = self.get_file_modification_time(file_path)
            
            # Advanced conflict detection
            if mod_time:
                time_diff = (datetime.now() - mod_time).seconds
                file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
                
                if time_diff < 300:  # Modified in last 5 minutes
                    result['status'] = 'conflict'
                    result['tooltip'] = f"🔴 Conflit détecté! Modifié à {mod_time.strftime('%H:%M')}, vérifier le serveur"
                elif time_diff < 3600:  # Modified in last hour
                    result['status'] = 'needs_sync'
                    result['tooltip'] = f"🟡 Fichier modifié ({mod_time.strftime('%H:%M')}, {file_size} bytes), sync requise"
                else:
                    result['status'] = 'synced'
                    result['tooltip'] = f"🟠 Fichier synchronisé ({mod_time.strftime('%H:%M')}, {file_size} bytes)"
            else:
                result['status'] = 'synced'
                result['tooltip'] = "🟠 Fichier synchronisé"
                
        elif local_has:
            file_path = os.path.join(self.production_folder, folder_name, asset_name, department_name, task_name, file_name)
            mod_time = self.get_file_modification_time(file_path)
            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            result['status'] = 'local_only'
            result['tooltip'] = f"⚪ Fichier local uniquement ({mod_time.strftime('%H:%M') if mod_time else 'N/A'}, {file_size} bytes)"
            
        elif server_has:
            result['status'] = 'server_only'
            result['tooltip'] = "⚫ Fichier serveur uniquement"
            
        return result
    
    def clear_all_caches(self):
        """
        When call clear all the asset_manager Cache
        """
        self.asset_cache = None
        self.department_cache = None
        self.task_cache = None
        self.file_cache = None
        print("Asset_Manger cache cleared")