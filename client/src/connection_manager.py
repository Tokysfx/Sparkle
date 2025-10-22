"""
Connection Manager Module

Intelligent server connection management system for Sparkle 3D Pipeline.
Provides automatic server detection, fallback to local mode, and connection monitoring.

Features:
- Automatic server availability detection
- Graceful fallback to local mode when server unavailable
- Periodic connection health checks
- Signal-based connection state notifications
- Request management with timeout handling
"""

import requests
import os
from PySide6.QtCore import QObject, Signal, QTimer


class ConnectionManager(QObject):
    """
    Intelligent server connection manager.
    
    Manages server connectivity with automatic detection and fallback capabilities.
    Provides a singleton pattern for application-wide connection management.
    """
    
    # Signals for connection state notifications
    connection_changed = Signal(bool)  # True = connected, False = disconnected
    
    def __init__(self):
        """
        Initialize the connection manager.
        
        Sets up connection state tracking and periodic health check timer.
        """
        super().__init__()
        self.server_url = ""
        self.is_connected = False
        self.last_check_failed = False
        
        # Timer for periodic connection health checks
        self.connection_timer = QTimer()
        self.connection_timer.timeout.connect(self.check_connection)
        
    def set_server_url(self, url):
        """
        Set the server URL and initiate connection check.
        
        Args:
            url (str): Server URL to connect to
        """
        self.server_url = url
        self.check_connection()
        
    def check_connection(self):
        """
        Check if the server is accessible.
        
        Performs a health check request to the server and updates connection state.
        Falls back to local mode if server is not reachable.
        
        Returns:
            bool: True if server is accessible, False otherwise
        """
        if not self.server_url:
            print("WARNING: No server URL configured")
            self._set_connection_state(False)
            return False
            
        print(f"INFO: Testing connection to: {self.server_url}/health")
        try:
            response = requests.get(f"{self.server_url}/health", timeout=2)
            print(f"INFO: Server response: status={response.status_code}")
            
            if response.status_code == 200:
                self._set_connection_state(True)
                return True
            else:
                self._set_connection_state(False)
                return False
                
        except Exception as e:
            print(f"WARNING: Connection failed: {e}")
            self._set_connection_state(False)
            return False
    
    def _set_connection_state(self, connected):
        """
        Update connection state and emit signal if state changed.
        
        Args:
            connected (bool): New connection state
        """
        if self.is_connected != connected:
            self.is_connected = connected
            self.connection_changed.emit(connected)
            
            if connected:
                print("SUCCESS: Server connected - Collaborative mode activated")
            else:
                print("INFO: Server disconnected - Local mode activated")
    
    def make_request(self, endpoint, timeout=3):
        """
        Make a server request only if connected.
        
        Performs HTTP GET request to the specified endpoint with automatic
        connection state management and fallback handling.
        
        Args:
            endpoint (str): API endpoint to request (e.g., "/projects")
            timeout (int): Request timeout in seconds
            
        Returns:
            dict or None: JSON response data if successful, None if failed
        """
        if not self.is_connected:
            return None
            
        try:
            response = requests.get(f"{self.server_url}{endpoint}", timeout=timeout)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"ERROR: Request failed for {endpoint}: {e}")
            # Re-check connection on request failure
            self.check_connection()
            return None
    
    def make_post_request(self, endpoint, data=None, timeout=3):
        """
        Make a POST request to the server only if connected.
        
        Performs HTTP POST request to the specified endpoint with data payload.
        
        Args:
            endpoint (str): API endpoint to request (e.g., "/create_folder")
            data (dict): Data to send in POST request
            timeout (int): Request timeout in seconds
            
        Returns:
            dict or None: JSON response data if successful, None if failed
        """
        if not self.is_connected:
            return None
            
        try:
            response = requests.post(f"{self.server_url}{endpoint}", json=data, timeout=timeout)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"WARNING: POST request failed with status {response.status_code}")
                return None
        except Exception as e:
            print(f"ERROR: POST request failed for {endpoint}: {e}")
            # Re-check connection on request failure
            self.check_connection()
            return None
    
    def start_auto_check(self, interval_seconds=30):
        """
        Start automatic connection health checks.
        
        Args:
            interval_seconds (int): Check interval in seconds
        """
        self.connection_timer.setInterval(interval_seconds * 1000)
        self.connection_timer.start()
        print(f"INFO: Auto connection check started (interval: {interval_seconds}s)")
        
    def stop_auto_check(self):
        """Stop automatic connection health checks."""
        self.connection_timer.stop()
        print("INFO: Auto connection check stopped")
    
    def download_file_from_server(self, endpoint, local_path):
        """
        Download a file from server and save it locally.
        
        Args:
            endpoint (str): Download endpoint (e.g., "/download/project/path/file.blend")
            local_file_path (str): Where to save the file locally
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_connected:
            return False
            
        try:
            response = requests.get(f"{self.server_url}{endpoint}", timeout=30)
            if response.status_code == 200:
                # Create parent directories if needed
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                
                # Write binary content to file
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"INFO: Downloaded file to {local_path}")
                return True
            else:
                print(f"ERROR: Download failed, status: {response.status_code}")
                return False
        except Exception as e:
            print(f"ERROR: Download failed for {endpoint}: {e}")
            return False
    
    def upload_file_to_server(self, endpoint, local_file_path):
        """
        Upload a file from local to server.
        
        Args:
            endpoint (str): Upload endpoint (e.g., "/upload/project/path/file.blend")
            local_file_path (str): Path to the local file to upload
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_connected:
            return False
        
        if not os.path.exists(local_file_path):
            print(f"ERROR: Local file not found: {local_file_path}")
            return False
            
        try:
            # Open and send the file
            with open(local_file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{self.server_url}{endpoint}", files=files, timeout=60)
            
            if response.status_code == 200:
                print(f"INFO: Uploaded file from {local_file_path}")
                return True
            else:
                print(f"ERROR: Upload failed, status: {response.status_code}")
                return False
        except Exception as e:
            print(f"ERROR: Upload failed for {endpoint}: {e}")
            return False


# Global singleton instance
connection_manager = ConnectionManager()