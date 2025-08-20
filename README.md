# Sparkle

Sparkle est une application de gestion de projets pour la production audiovisuelle ou 3D, développée avec Python et PySide6. Elle permet de créer, organiser et naviguer dans des projets, assets et shots, avec une interface graphique moderne.

## Fonctionnalités principales

- **Création de projets** : Interface pour créer un nouveau projet, définir son nom, son chemin et sa description. Génération automatique de la structure de dossiers (préproduction, production, postproduction, etc.).
- **Gestion des assets et shots** : Visualisation et organisation des assets et shots par type, avec création de dossiers et sous-dossiers selon des presets configurables.
- **Navigation par arborescence** : Plusieurs arbres (QTreeWidget) pour explorer les assets, départements, tâches et fichiers du projet.
- **Barre d’outils verticale** : Navigation rapide entre la gestion de fichiers, la page d’accueil projet et le gestionnaire de shots.
- **Actions contextuelles** : Menu clic droit pour créer, supprimer ou organiser des assets et dossiers.
- **Synchronisation automatique** : Surveillance des changements dans les fichiers et dossiers du projet pour mise à jour en temps réel de l’interface.

## Structure du projet

```
main.py
script/
    project_new.py
    project_browser.py
    QTtree_shot_asset.py
    QTtree_Departement.py
    QTtree_Task.py
    QTtree_File.py
    build/
        Asset_build.py
        AssetFolder_build.py
    rightClic/
        Asset_rightClic.py
ui/
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

## Dépendances

- Python 3.11+
- PySide6

## Installation

1. Installe Python et PySide6 :
   ```powershell
   pip install PySide6
   ```
2. Clone le projet :
   ```powershell
   git clone https://github.com/ton-utilisateur/sparkle.git
   ```
3. Lance l’application :
   ```powershell
   python main.py
   ```

## Utilisation

- Lance `main.py` pour ouvrir l’interface.
- Utilise la barre d’outils pour naviguer entre les pages.
- Crée un projet via le bouton "New Project".
- Organise tes assets et shots via le gestionnaire de fichiers.
- Utilise le clic droit pour créer ou supprimer des assets/dossiers.

## Personnalisation

- Les presets d’assets et la structure des dossiers sont configurables via les fichiers JSON dans `data/build/`.
- Les projets sont stockés dans `data/projects/`.

## Auteur

Projet développé par [Ton Nom].
