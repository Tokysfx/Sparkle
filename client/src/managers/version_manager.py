"""
Version manager module

Handle versionning files in the diferent software
"""

import re
import os

class VersionManager:
    def __init__(self):
        self.pattern = r"^([A-Za-z0-9]+)_([A-Za-z0-9]+)_v(\d{3})\.([A-Za-z0-9]+)$"

    def clean_name(self, name):
        """
        Clean the name

        Args:
            name : Name of the asset

        Returns:
            Clean name without space or spécial character
        """
        return re.sub(r'[^A-Za-z0-9]', '', name)
    
    def is_versioned_file(self, filename):
        """
        Verify if the file have the same parterne

        Args:
            Filename

        Returns:
            Bool: True or false
        """
        return bool(re.fullmatch(self.pattern, filename))
        
    
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
    
    def get_next_version_number(self, directory_path, asset, task, version, extension):
        """
        Change the version of the filename

        Args:
            directory_path: Local Path of the file
            asset: asset_name
            task: task_name
            version: old version of the filename
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