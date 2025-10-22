"""
Version manager module

Handle versionning files in the diferent software
"""

import re
import os

class VersionManager:
    def __init__(self):
        # Pattern regex pour détecter nos fichiers
        self.pattern = r"^([A-Za-z0-9]+)_([A-Za-z0-9]+)_v(\d{3})\.([A-Za-z0-9]+)$"

    def clean_name(self, name):
        return re.sub(r'[A-Za-z0-9]', '', name)
    
    def is_versioned_file(self, filename):
        if re.fullmatch(self.pattern, filename):
            return True
        else:
            return False
    
    def parse_filename(self, filename):
        match = re.match(self.pattern, filename)
        if match:
            return {
                "asset_name": match.group(1),    # Premier groupe ()
                "task_name": match.group(2),     # Deuxième groupe ()
                "version": int(match.group(3)),  # Troisième groupe ()
                "extension": match.group(4)      # Quatrième groupe ()
            }
        return None
    
    def get_next_version_number(self, directory_path, asset, task, version, extension):
        if re.fullmatch('v(\d{3})', version):
            int(version) = re.sub(r'v')
            new_version = version + 1
            name = f"{asset}_{task}_v{new_version}.{extension}"
            return name
        else:
            print("Error no version found")