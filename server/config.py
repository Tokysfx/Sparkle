import json
import os
from pathlib import Path

class ServerConfig:
    def __init__(self):
        if os.name == 'nt':
            documents_path = Path(os.environ.get('USERPROFILE', Path.home())) / 'Documents'
        else:
            documents_path = Path.home() / 'Documents'
            
        self.config_folder = documents_path / "Sparkle"
        self.config_file = self.config_folder / "server_config.json"
        self.default_config = {
            "projects_folder": str(documents_path / "Sparkle")
        }
    
    def load_config(self):
        """Load server config"""
        if not self.config_file.exists():
            self.save_config(self.default_config)
            return self.default_config
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except:
            return self.default_config
    
    def save_config(self, config):
        """Sauvegarder la configuration"""
        self.config_folder.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get_projects_folder(self):
        """Récupérer le dossier des projets"""
        config = self.load_config()
        return Path(config["projects_folder"])