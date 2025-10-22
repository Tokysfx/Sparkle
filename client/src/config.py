import json
import os
from pathlib import Path


class configSparkle():
    def __init__(self):
                
        self.sparkle_folder = Path.home() / "Documents" / "Sparkle"
        self.sparkle_folder.mkdir(parents=True, exist_ok=True)

        self.config_path = self.sparkle_folder / "config.json"

        self.default_config = {
            "projects_folder": str(Path.home() / "Documents" / "Sparkle"),
            "version": "1.0.0"
        }

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as file:
                config = json.load(file)
                return config
        else:
            config = self.default_config
            return config
        
    def update_active_project(self, project_path):
        
        current_config = self.load_config()
        
        current_config["project_active_folder"] = project_path
        
        self.save_config(current_config)

    def uptdate_url(self, server_url):

        current_config = self.load_config()

        current_config["url"] = server_url

        self.save_config(current_config)

    def update_project_folder(self, file):

        current_config = self.load_config()

        current_config["projects_folder"] = file

        self.save_config(current_config)

    def save_config(self, config_data):
        json_str = json.dumps(config_data, indent=4)
        with open (self.config_path, "w") as file:
            file.write(json_str)
