import json
import os  

def get_projectPath_Active (production_path):
    """
    Creer un fichier JSON contenant le chemin du projet actif.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    production_path = os.path.normpath(production_path)
    json_path = os.path.join(data_dir, "active_project.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"active_project_path": production_path}, f, indent=4)

    print(f"Active project path saved to {json_path}")