"""
Version manager module

Handle versionning files in the diferent software
"""

import re
import os

class VersionManager:
    def __init__(self):
        self.pattern = r"^([A-Za-z0-9]+)_([A-Za-z0-9]+)_v(\d{3})\.([A-Za-z0-9]+)$"
        self.master_pattern = r"^([A-Za-z0-9]+)_([A-Za-z0-9]+)_master\.([A-Za-z0-9]+)$"

    def clean_name(self, name):
        """
        Clean the name

        Args:
            name : Name of the asset

        Returns:
            Clean name without space or spécial character
        """
        return re.sub(r'[^A-Za-z0-9]', '', name)
    
    def is_versioned_file(self, directory_path):
        """
        Verify if a verion file already exist
        """

        is_version_file = False
        for file in os.listdir(directory_path):
            if re.fullmatch(self.pattern, file):
                is_version_file = True
        return is_version_file
    
    def is_master_file(self, directory_path):
        """
        Verify if the a master file already exist
        """

        is_master_file = False
        for file in os.listdir(directory_path):
            if re.fullmatch(self.master_pattern, file):
                is_master_file = True
        return is_master_file

    
    def parse_filename(self, filename):
        """
        Cute the filename in four piece

        Args:
            Filename
        Returns:
            Dic: with the four part of the filename

        """
        match = re.match(self.pattern, filename)
        if match:
            return {
                "asset_name": match.group(1),
                "task_name": match.group(2),
                "version": int(match.group(3)),
                "extension": match.group(4)  
            }
    
    def get_next_version_number(self, directory_path, asset, task, extension):
        """
        Change the version of the filename

        Args:
            directory_path: Local Path of the file
            asset: asset_name
            task: task_name
            extension: .blend, .mb, .hipnic
        Returns:
            New filename
        """
        max_version = 0

        files = os.listdir(directory_path)
        for file in files:
            if file.startswith(f"{asset}_{task}_v"):
                name = self.parse_filename(file)
                version = name.get("version", "")
                if max_version < version:
                    max_version = version
        if max_version > 0:
            new_version = max_version + 1
            new_name = f"{asset}_{task}_v{new_version:03d}.{extension}"
        else:
            new_name =f"{asset}_{task}_v001.{extension}"
        return new_name     

    def creat_version_save_as(self, directory_path, asset, task, extension):

        version = self.get_next_version_number(directory_path, asset, task, extension)
        version_path = os.path.join(directory_path, version)
        master = f"{asset}_{task}_master.{extension}"
        master_path = os.path.join(directory_path, master)

        return version_path, master_path