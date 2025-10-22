from fastapi import FastAPI, File, UploadFile
from pathlib import Path
from config import ServerConfig 
from pydantic import BaseModel
import shutil
import os
from fastapi.responses import FileResponse

app = FastAPI(title="Sparkle Server")
server_config = ServerConfig()

class ProjectCreate(BaseModel):
    name: str

config_project = {
    "01_PreProduction" : [
        "concept_art",
        "references",
        "storyboard"
    ],
    "02_Production" : [
        "Chara",
        "Env",
        "Props",
        "Items",
        "Modules",
        "FX",
        "00_Shot"
    ],
    "03_PostProduction" : [
        "Grading",
        "Editing",
        "DCP"
    ]            
}

@app.get("/health")
def health_check():
    return {"status": "OK"}

@app.get("/projects")
def get_projects():
    projects_folder = server_config.get_projects_folder()

    if not projects_folder.exists():
        return {"projects": []}
    
    projects = []
    for folder in projects_folder.iterdir():
        if folder.is_dir():
            projects.append({
                "name": folder.name,
                "path": str(folder)
            })
    return {"projects": projects}

@app.post("/projects/{project_name}")
def create_project(project: ProjectCreate, project_name = str):

    projects_folder = server_config.get_projects_folder()
    project_path = projects_folder / project_name
    
    if project_path.exists():
        return {"error": f"Project '{project_name}' already exists"}
    
    for main_folder, subfolders in config_project.items():
        for subfolder in subfolders:
            full_path = project_path / main_folder / subfolder
            full_path.mkdir(parents=True, exist_ok=True)
    
    return {"message": f"Project '{project_name}' created successfully"}

""" 


Use for Filemanager


"""
@app.get("/projects/{project_name}/assets")
def get_assets(project_name = str):

    server_assets = {}

    projects_folder = server_config.get_projects_folder()
    project_path = projects_folder / project_name
    production_folder = project_path / "02_Production"
    if not production_folder.exists():
        return {"assets": []}

    for asset_type_folder in production_folder.iterdir():
        if asset_type_folder.is_dir() and asset_type_folder.name != "00_Shot":
            asset_type = asset_type_folder.name
            assets = []
            for asset in asset_type_folder.iterdir():
                if asset.is_dir():
                    assets.append(asset.name)
            server_assets[asset_type] = assets
    return server_assets

@app.get("/projects/{project_name}/{folder_name}/{asset_name}/department")
def get_department(project_name = str, folder_name = str, asset_name = str):

    server_department = []

    projects_folder = server_config.get_projects_folder()
    project_path = projects_folder / project_name
    asset_folder = project_path / "02_Production" / folder_name / asset_name
    if not asset_folder.exists():
        return {"departments": []}

    for department in asset_folder.iterdir():
        if department.is_dir():
            server_department.append(department.name)
    return {"departments": server_department}

@app.get("/projects/{project_name}/{folder_name}/{asset_name}/{department_name}/task")
def get_department(project_name = str, folder_name = str, asset_name = str, department_name = str):

    server_task = []

    projects_folder = server_config.get_projects_folder()
    project_path = projects_folder / project_name
    department_folder = project_path / "02_Production" / folder_name / asset_name / department_name
    if not department_folder.exists():
        return {"departments": []}

    for task in department_folder.iterdir():
        if task.is_dir():
            server_task.append(task.name)
    return {"task": server_task}

@app.get("/projects/{project_name}/{folder_name}/{asset_name}/{department_name}/{task_name}/file")
def get_department(project_name = str, folder_name = str, asset_name = str, department_name = str, task_name = str):

    server_file = []

    projects_folder = server_config.get_projects_folder()
    project_path = projects_folder / project_name
    task_folder = project_path / "02_Production" / folder_name / asset_name / department_name /task_name
    if not task_folder.exists():
        return {"file": []}

    for file in task_folder.iterdir():
        if file.is_file():  # ✅ CORRECTION : Vérifier les fichiers, pas les dossiers !
            server_file.append(file.name)
    return {"file": server_file}

@app.get("/status/{project_name}")
def get_status(project_name: str):
    tree = []
    projects_folder = server_config.get_projects_folder()
    project_path = projects_folder / project_name
    production_folder = project_path / "02_Production"

    for root, dirs, files in os.walk(production_folder):
        for d in dirs:
            tree.append({
                "type": "dir",
                "name": d,
                "path": os.path.relpath(os.path.join(root, d), str(production_folder))
            })
        for f in files:
            tree.append({
                "type": "file",
                "name": f,
                "path": os.path.relpath(os.path.join(root, f), str(production_folder))
            })
    return {"tree": tree}

@app.post("/upload/{project_name}/{path:path}")
def upload_file(project_name: str, path: str, file: UploadFile = File(...)):
    projects_folder = server_config.get_projects_folder()
    target_path = projects_folder / project_name / "02_Production" / Path(path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with open(target_path, "wb") as buffer:
        buffer.write(file.file.read())
    return {"message": f"Fichier {file.filename} uploadé dans {target_path}"}

@app.post("/create_folder/{project_name}/{path:path}")
def create_folder(project_name: str, path: str):
    """Create a folder structure on the server."""
    projects_folder = server_config.get_projects_folder()
    target_path = projects_folder / project_name / "02_Production" / Path(path)
    target_path.mkdir(parents=True, exist_ok=True)
    return {"message": f"Folder created: {target_path}"}

@app.get("/download/{project_name}/{path:path}")
def download_file(project_name: str, path: str):
    """Download a file from the server."""
    projects_folder = server_config.get_projects_folder()
    file_path = projects_folder / project_name / "02_Production" / Path(path)
    
    if not file_path.exists():
        return {"error": f"File not found: {path}"}
    
    return FileResponse(
        path=str(file_path),
        filename=file_path.name,
        media_type='application/octet-stream'
    )

@app.delete("/projects/{name}")
def delete_project(name: str):
    projects_folder = server_config.get_projects_folder()
    project_path = projects_folder / name
    
    if not project_path.exists():
        return {"error": f"Project '{name}' not found"}
    shutil.rmtree(project_path)
    return {"message": f"Project '{name}' deleted successfully"}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)