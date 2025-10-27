# Sparkle 3D Pipeline

**Sparkle** est un système de gestion de pipeline 3D professionnel conçu pour les studios de production travaillant avec Blender, Nuke, Houdini, ZBrush, Substance Painter et autres logiciels 3D.

## Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#️-architecture)
- [Installation](#️-installation)
- [Démarrage rapide](#-démarrage-rapide)
- [Utilisation du serveur](#️-utilisation-du-serveur)
- [Utilisation du client](#-utilisation-du-client)
- [Configuration](#-configuration)
- [Structure des projets](#-structure-des-projets)
- [Workflow typique](#-workflow-typique)
- [Dépannage](#-dépannage)

## Fonctionnalités

### Fonctionnalités implémentées
- **Système client-serveur** : Architecture distribuée pour collaboration d'équipe
- **Gestionnaire de fichiers 4 colonnes** : Navigation Asset → Department → Task → File
- **Gestion de projets** : Création/gestion avec structure standardisée
- **Synchronisation local/serveur** : Visual feedback du statut de sync
- **Publish/Download** : Transfert bidirectionnel de fichiers
- **CRUD complet** : Création/suppression assets, départements, tâches, fichiers
- **Configuration flexible** : Choix du répertoire de stockage serveur
- **Architecture modulaire** : Code organisé et maintenable

### En développement
- **Versioning automatique** : Gestion des versions lors des sauvegardes
- **Intégration logiciels 3D** : Plugins Blender/Maya/etc.

## Architecture

```
Sparkle/
├── server/                     # Serveur FastAPI
│   ├── main.py                # Point d'entrée serveur
│   ├── api/                   # Routes API REST
│   ├── models/                # Modèles SQLAlchemy
│   ├── database/              # Configuration base de données
│   └── config/                # Configuration serveur
├── client/                     # Client PySide6
│   ├── main.py                # Point d'entrée client
│   ├── ui/                    # Interface utilisateur
│   └── src/                   # Logique métier
└── venv/                      # Environnement virtuel Python
```

**Communication** : Client HTTP ↔ FastAPI REST API ↔ SQLite Database + Système de fichiers

## Installation

### Prérequis
- **Python 3.8+** (testé avec Python 3.10)
- **Git** (pour cloner le projet)

### 1. Cloner le projet
```bash
git clone [URL_DU_PROJET]
cd Sparkle
```

### 2. Créer l'environnement virtuel
```bash
python -m venv venv
```

### 3. Activer l'environnement
**Windows :**
```bash
venv\\Scripts\\activate
```

**Linux/Mac :**
```bash
source venv/bin/activate
```

### 4. Installer les dépendances
```bash
pip install fastapi uvicorn sqlalchemy pyside6 requests
```

## Démarrage rapide

### Démarrer le serveur (Local)
```bash
# Depuis le répertoire racine Sparkle/
cd server
python main.py
```

Le serveur sera accessible sur : `http://localhost:8000`

### Démarrer le serveur (Accès distant)
```bash
# Pour permettre l'accès depuis d'autres machines
cd server
python start_remote_server.py
```

Le script vous donnera l'IP à communiquer à vos collaborateurs.

### Lancer le client
```bash
# Depuis le répertoire racine Sparkle/
cd client
python main.py
```

### Connecter un client distant

#### Méthode 1 : Clé de connexion (RECOMMANDÉE) 🔑
1. **L'administrateur serveur** démarre avec `python start_remote_server.py`
2. **Copier la clé** affichée (ex: `SPARKLE_KEY_eyJpZCI6...`)
3. **Donner la clé** aux collaborateurs
4. **Client** : Menu **Tools → Connect with Key**
5. **Coller la clé** et cliquer **Connect**

#### Méthode 2 : Configuration manuelle
1. **Menu Tools → Network Configuration**
2. Entrer l'IP du serveur (ex: `192.168.1.100`)
3. Port : `8000`
4. **Test Connection** puis **Apply & Connect**

## 🖥️ Utilisation du serveur

### Démarrage manuel
```bash
cd server
python main.py
```

### Démarrage avec Uvicorn (production)
```bash
cd server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Configuration du stockage
Le serveur créé automatiquement un fichier `server/config/server_config.json` :

```json
{
    "projects_root_path": "./server_projects",
    "server_host": "localhost",
    "server_port": 8000,
    "database_url": "sqlite:///./sparkle.db",
    "max_file_size_mb": 500,
    "allowed_extensions": [".blend", ".ma", ".mb", ".hip", ".nk", ".psd", ".exr", ".png", ".jpg"]
}
```

### API Endpoints disponibles

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Status serveur + configuration |
| GET | `/api/projects/` | Liste tous les projets |
| POST | `/api/projects/` | Créer un nouveau projet |
| DELETE | `/api/projects/{id}` | Supprimer un projet |
| GET | `/api/config/` | Configuration serveur |
| POST | `/api/config/projects-root` | Modifier chemin stockage |
| GET | `/api/config/validate-path` | Valider un chemin |

## Utilisation du client

### Interface principale
L'interface client offre :

1. **Menu Project** : Nouveau projet, charger projet existant
2. **Menu Tools** : Configuration serveur, test de connexion
3. **Gestionnaire 4 colonnes** :
   - **Asset** : Types d'assets (chara, props, env, fx, etc.)
   - **Department** : Départements (modeling, texturing, rigging, etc.)
   - **Task** : Tâches (work, publish, reference)
   - **File** : Fichiers de travail

### Visual feedback des fichiers
- **Blanc** : Fichier local uniquement
- **Gris** : Fichier serveur uniquement  
- **Vert** : Fichier synchronisé (local + serveur)

### Menus contextuels (clic droit)

#### Colonne Asset
- **New Asset** : Créer un nouvel asset
- **Delete Local/Server** : Supprimer asset en local ou serveur

#### Colonne Department
- **New Department** : Créer un département
- **Delete Local/Server** : Supprimer département

#### Colonne Task
- **New Task** : Créer une tâche
- **Delete Local/Server** : Supprimer tâche

#### Colonne File
- **New File** : Créer un nouveau fichier
- **Publish** : Envoyer fichier vers serveur
- **Download** : Télécharger fichier depuis serveur
- **Delete Local/Server** : Supprimer fichier
- **Create Scene** : Ouvrir dans logiciel 3D (futur)

## Configuration Réseau pour Collaboration Distante

### Pour l'hôte du serveur (vous)

#### 1. Démarrage serveur distant
```bash
cd server
python start_remote_server.py
```

Le script vous affichera :
- Votre IP locale (ex: `192.168.1.100`)
- Instructions pour vos collaborateurs
- Vérifications réseau nécessaires

#### 2. Configuration réseau requise
- **Firewall** : Ouvrir le port 8000
- **Réseau local** : Tous sur le même Wi-Fi/réseau
- **Internet** : Port forwarding sur votre routeur (si accès internet)

### Pour les collaborateurs distants

#### 1. Connexion via clé (SIMPLE)
1. **Recevoir la clé** de l'administrateur serveur
2. **Menu Tools → Connect with Key**
3. **Coller la clé** dans le champ texte
4. **Validate Key** pour vérifier
5. **Connect to Server**

#### 2. Configuration manuelle (AVANCÉE)
**Via interface :**
1. **Menu Tools → Network Configuration**
2. **Host** : IP fournie par l'hôte (ex: `192.168.1.100`)
3. **Port** : `8000`
4. **Test Connection** pour valider
5. **Apply & Connect**

#### 2. Vérification connexion
- **Menu Tools → Test Server Connection**
- Doit afficher "Server is online!"

### Dépannage réseau

#### Connexion impossible
1. **Ping test** : `ping [IP_DU_SERVEUR]`
2. **Port ouvert** : `telnet [IP_DU_SERVEUR] 8000`
3. **Firewall** : Vérifier les règles des deux côtés
4. **Réseau** : Même sous-réseau ou port forwarding

#### Performance lente
- **Bandwidth** : Éviter le transfert de gros fichiers
- **Wi-Fi** : Privilégier câble Ethernet
- **Compression** : Activée automatiquement

#### Sécurité
- **Réseau privé** : Utiliser VPN si possible
- **Firewall strict** : Limiter l'accès au port 8000
- **Mot de passe** : À implémenter (future version)

## Configuration

### Configuration serveur
**Via interface client :**
1. Menu **Tools → Server Settings**
2. Modifier le chemin de stockage
3. Cliquer **Browse** pour naviguer
4. **Validate** pour vérifier
5. **Apply** pour confirmer

**Via fichier config :**
Éditer `server/config/server_config.json`

### Test de connexion
**Via interface client :**
Menu **Tools → Test Server Connection**

**Via curl :**
```bash
curl -X GET "http://localhost:8000/"
```

## Structure des projets

Chaque projet créé suit cette structure standardisée :

```
MonProjet/
├── 00_data/              # Données sources, références
├── 01_Preprod/           # Pré-production, concepts
├── 02_Prod/              # Production principale
│   ├── chara/            # Personnages
│   │   └── hero/         # Asset exemple
│   │       ├── modeling/ # Département
│   │       │   ├── work/     # Fichiers de travail
│   │       │   ├── publish/  # Versions publiées
│   │       │   └── reference/ # Références
│   │       ├── texturing/
│   │       ├── rigging/
│   │       └── animation/
│   ├── props/            # Objets/accessoires
│   ├── env/              # Environnements
│   ├── fx/               # Effets spéciaux
│   ├── item/             # Items spéciaux
│   └── assemble/         # Assemblages/rigs
└── 03_Postprod/          # Post-production
```

## Workflow typique

### 1. Configuration initiale
1. **Démarrer le serveur** : `cd server && python main.py`
2. **Configurer stockage** : Menu Tools → Server Settings
3. **Tester connexion** : Menu Tools → Test Server Connection

### 2. Création de projet
1. **Menu Project → New Project**
2. Saisir nom, chemin local, description
3. Le projet est créé sur serveur ET local

### 3. Travail sur assets
1. **Navigation** : Asset → Department → Task
2. **Création fichiers** : Clic droit → New File
3. **Travail local** : Fichiers visibles en blanc
4. **Publication** : Clic droit → Publish (fichier devient vert)

### 4. Collaboration
1. **Téléchargement** : Clic droit → Download (fichiers gris → verts)
2. **Modification locale** : Travail sur copies locales
3. **Re-publication** : Publish des modifications

### 5. Gestion d'équipe
- **Chaque artiste** : Client connecté au même serveur
- **Serveur centralisé** : Stockage partagé configurable
- **Sync intelligent** : Visual feedback du statut

## Dépannage

### Serveur ne démarre pas
```bash
# Vérifier l'environnement Python
cd server
python -c "import fastapi, uvicorn; print('Dependencies OK')"

# Tester la configuration
python -c "from config.settings import get_server_config; print('Config OK')"
```

### Client ne se connecte pas
1. **Vérifier serveur** : `curl http://localhost:8000/`
2. **Test interface** : Menu Tools → Test Server Connection
3. **Vérifier firewall** : Port 8000 ouvert

### Erreurs de permissions
1. **Côté serveur** : Vérifier droits écriture répertoire projets
2. **Validation** : Menu Tools → Server Settings → Validate

### Fichiers non synchronisés
1. **Vérifier connexion** : Status bar client
2. **Forcer refresh** : F5 ou clic sur asset
3. **Vérifier chemins** : Cohérence local/serveur

### Base de données corrompue
```bash
# Supprimer et recréer (ATTENTION : perte de données)
cd server
rm sparkle.db
python main.py  # Recrée automatiquement
```

---

## Support

Pour questions ou problèmes :
1. Vérifier ce README
2. Consulter `project_memory.md` pour l'historique du développement
3. Tester avec configuration par défaut

**Version actuelle : 1.0.0** - Architecture refactorisée et configuration flexible  
**Dernière mise à jour : Octobre 2025**