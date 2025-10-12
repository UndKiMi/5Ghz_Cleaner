# 5GH'z Cleaner - Structure du Projet

## 📁 Architecture

```
5Ghz_Cleaner/
├── assets/                      # Ressources statiques
│   ├── icons/                   # Icônes SVG personnalisées
│   │   ├── cleaning.svg         # Icône de nettoyage
│   │   ├── folder.svg           # Icône de dossier
│   │   └── shield_check.svg     # Icône de bouclier
│   └── images/                  # Images (si nécessaire)
│
├── backend/                     # Logique métier
│   ├── __init__.py
│   └── cleaner.py              # Fonctions de nettoyage Windows
│
├── frontend/                    # Interface utilisateur
│   ├── __init__.py
│   ├── app.py                  # Application principale Flet
│   ├── constants.py            # Constantes UI (deprecated, voir design_system)
│   ├── ui_components.py        # Composants UI (deprecated, voir design_system)
│   │
│   ├── design_system/          # Système de design
│   │   ├── __init__.py         # Exports centralisés
│   │   ├── theme.py            # Tokens (couleurs, espacements, typo)
│   │   ├── buttons.py          # Composants boutons
│   │   ├── containers.py       # Composants conteneurs
│   │   ├── text.py             # Composants texte
│   │   ├── icons.py            # Composants icônes
│   │   └── inputs.py           # Composants inputs
│   │
│   └── pages/                  # Pages de l'application
│       ├── __init__.py
│       └── main_page.py        # Page principale
│
├── main.py                     # Point d'entrée de l'application
├── requirements.txt            # Dépendances Python
├── DESIGN_SYSTEM.md           # Documentation du design system
├── PROJECT_STRUCTURE.md       # Ce fichier
└── README.md                  # Documentation principale

```

## 🎨 Design System

Le design system est organisé en modules thématiques :

- **theme.py** : Tokens de design (Colors, Spacing, Typography, etc.)
- **buttons.py** : PrimaryButton, SecondaryButton, IconButton, TextButton
- **containers.py** : Card, Panel, WarningBox, Divider, Spacer
- **text.py** : Heading, BodyText, Caption, Link
- **icons.py** : ShieldIcon, WarningIcon, InfoIcon, etc.
- **inputs.py** : Checkbox, Slider, Switch, TextField

## 🔧 Backend

Le module backend contient toutes les fonctions de nettoyage :

### Fonctions principales
- `clean_temp_files()` - Nettoyage complet des fichiers temporaires
- `run_full_cleanup(options)` - Nettoyage complet avec options

### Fonctions individuelles
- `clear_temp()` - Fichiers temporaires
- `clear_windows_update_cache()` - Cache Windows Update
- `empty_recycle_bin()` - Corbeille
- `clear_prefetch()` - Prefetch
- `clear_recent()` - Fichiers récents
- `clear_thumbnail_cache()` - Cache miniatures
- `clear_crash_dumps()` - Dumps de crash
- `clear_standby_memory()` - RAM Standby
- `flush_dns()` - Cache DNS
- `disable_telemetry()` - Télémétrie Windows
- `clear_large_logs()` - Logs volumineux

## 📄 Pages

### MainPage (`frontend/pages/main_page.py`)

Page principale avec deux onglets :
1. **Nettoyage rapide** : 3 actions principales (Fichiers temp, RAM, DNS)
2. **Options avancées** : 4 options configurables avec switches

## 🚀 Flux d'exécution

1. `main.py` → Vérifie les droits admin et lance l'app
2. `frontend/app.py` → Initialise Flet et affiche le disclaimer
3. `frontend/pages/main_page.py` → Affiche la page principale
4. `backend/cleaner.py` → Exécute les opérations de nettoyage

## 📦 Dépendances

- **flet** : Framework UI
- **ctypes** : Interactions système Windows
- **subprocess** : Exécution de commandes
- **shutil** : Opérations fichiers

## 🎯 Bonnes pratiques

1. Utiliser le design system pour tous les composants UI
2. Séparer la logique métier (backend) de l'UI (frontend)
3. Utiliser les tokens du thème pour la cohérence visuelle
4. Documenter les nouvelles fonctionnalités
5. Tester sur Windows avec droits administrateur
