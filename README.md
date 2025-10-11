# 5Gh'z Cleaner

Windows Cleaning & Optimisation Tool with Modern UI

## Structure du Projet

```
5Ghz_Cleaner/
├── backend/              # Backend Python (logique métier)
│   ├── __init__.py
│   ├── cleaner.py       # Fonctions de nettoyage
│   └── elevation.py     # Gestion des privilèges admin
├── frontend/            # Frontend Flet (interface utilisateur)
│   ├── __init__.py
│   └── app.py          # Interface moderne Flet
├── main.py             # Point d'entrée principal
└── requirements.txt    # Dépendances Python
```

## Installation

1. Installer les dépendances:
```bash
pip install -r requirements.txt
```

## Utilisation

Lancer l'application:
```bash
python main.py
```

L'application demandera automatiquement les privilèges administrateur (UAC).

## Compilation en Exécutable

Pour compiler l'application en un exécutable Windows:

```bash
# Installer flet
pip install flet

# Compiler l'application
flet pack main.py --name "5Ghz_Cleaner" --icon image.jpg
```

## Fonctionnalités

### Nettoyage Standard
- Nettoyage des fichiers temporaires système
- Optimisation du préchargement Windows (Prefetch)
- Purge de l'historique technique
- Rafraîchissement du cache des miniatures
- Nettoyage des journaux de crash
- Suppression de Windows.old
- Nettoyage du cache Windows Update
- Vidage de la corbeille
- Arrêt de services optionnels

### Options Avancées
- Libération de la RAM Standby
- Flush DNS
- Désactivation de la télémétrie Windows
- Nettoyage des logs volumineux

## Architecture

### Backend (Python pur)
Le backend contient toute la logique métier sans aucune dépendance UI:
- `cleaner.py`: Toutes les fonctions de nettoyage et d'optimisation
- `elevation.py`: Gestion de l'élévation des privilèges

### Frontend (Flet)
Interface moderne construite avec Flet:
- Design moderne et épuré
- Thème sombre cohérent
- Barre de progression en temps réel
- Menu d'options avancées
- Dialogue de résumé détaillé

### Communication
Aucune communication réseau - tout est local. Le frontend appelle directement les fonctions du backend.

## Auteur

**UndKiMi**
- GitHub: https://github.com/UndKiMi
- Repository: https://github.com/UndKiMi/5Ghz_Cleaner

## Licence

Tous droits réservés par UndKiMi
