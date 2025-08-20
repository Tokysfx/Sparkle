
# Sparkle

Sparkle is a professional project management application for audiovisual and 3D production, built with Python and PySide6. It provides a modern graphical interface to create, organize, and navigate projects, assets, and shots efficiently.

## Main Features

- **Project Creation**: Easily create new projects, set their name, path, and description. Automatically generates a complete folder structure (preproduction, production, postproduction, etc.).
- **Asset and Shot Management**: Visualize and organize assets and shots by type, with customizable folder and subfolder presets.
- **Tree Navigation**: Multiple QTreeWidget-based views to explore assets, departments, tasks, and project files.
- **Vertical Toolbar**: Quickly switch between file management, project home, and shot manager pages.
- **Contextual Actions**: Right-click menu for creating, deleting, or organizing assets and folders.
- **Real-Time Synchronization**: Monitors changes in project files and folders for instant UI updates.

## Project Structure

```
main.py
src/
    project_new.py
    project_browser.py
    QTtree_shot_asset.py
    QTtree_Departement.py
    QTtree_Task.py
    QTtree_File.py
    rightClic/
        Asset_rightClic.py
gui/
    toolbar.py
    fileManager.py
    project.py
    Shot_Asset_button.py
    shotManager.py
utils/
    file_manager_utils.py
    Path_Catcher.py
data/
    build/
        asset_build.json
        AssetType_preset.json
        New_project.json
    projects/
        LOL_project.json
        test_project.json
    active_project.json
```

## Requirements

- Python 3.11+
- PySide6

## Installation

1. Install Python and PySide6:
   ```powershell
   pip install PySide6
   ```
2. Clone the repository:
   ```powershell
   git clone https://github.com/Tokysfx/Sparkle.git
   ```
3. Launch the application:
   ```powershell
   python main.py
   ```

## Usage

- Run `main.py` to open the interface.
- Use the vertical toolbar to navigate between pages.
- Create a project using the "New Project" button.
- Organize your assets and shots with the file manager.
- Use right-click to create or delete assets/folders.

## Customization

- Asset presets and folder structures are configurable via JSON files in `data/build/`.
- Projects are stored in `data/projects/`.

## Author

Developed by [Your Name].
