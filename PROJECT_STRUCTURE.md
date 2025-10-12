# 📁 Structure du Projet - 5GH'z Cleaner

## 📋 Vue d'ensemble

Ce document décrit l'organisation complète du projet 5GH'z Cleaner.

**Version**: 1.5  
**Score**: 95/100 🟢 (Excellent)

---

## 🗂️ Arborescence Complète

```
5Ghz_Cleaner/
│
├── 📄 main.py                          # Point d'entrée principal
├── 📄 requirements.txt                 # Dépendances Python
├── 📄 README.md                        # Documentation principale
├── 📄 SECURITY.md                      # Rapport de sécurité
├── 📄 LICENSE                          # Licence du projet
├── 📄 PROJECT_STRUCTURE.md             # Ce fichier
│
├── 🔧 Scripts de build
│   ├── build.bat                       # Script de compilation Windows
│   ├── run.bat                         # Script de lancement rapide
│   ├── generate_checksum.py            # Générateur de checksums SHA256
│   └── 5Ghz_Cleaner.spec              # Configuration PyInstaller
│
├── 🧪 Tests
│   ├── test_service_dependencies.py    # Test dépendances services
│   ├── test_elevation_dryrun.py        # Test élévation
│   ├── test_dry_run_button.py          # Test bouton dry-run
│   ├── test_anti_spam.py               # Test anti-spam
│   └── test_anti_bypass.py             # Test anti-contournement
│
├── 📦 backend/                         # Logique métier
│   ├── __init__.py
│   ├── cleaner.py                      # Fonctions de nettoyage
│   ├── elevation.py                    # Gestion privilèges admin
│   ├── logger.py                       # Système de logging
│   ├── security.py                     # Vérifications sécurité
│   ├── dry_run.py                      # Mode prévisualisation
│   └── telemetry_checker.py            # Vérificateur télémétrie
│
├── 🎨 frontend/                        # Interface utilisateur
│   ├── __init__.py
│   ├── app.py                          # Application Flet
│   │
│   ├── design_system/                  # Système de design
│   │   ├── __init__.py
│   │   ├── theme.py                    # Tokens (couleurs, espacements)
│   │   ├── buttons.py                  # Composants boutons
│   │   ├── containers.py               # Composants conteneurs
│   │   ├── text.py                     # Composants texte
│   │   ├── icons.py                    # Composants icônes
│   │   └── inputs.py                   # Composants inputs
│   │
│   └── pages/                          # Pages de l'application
│       ├── __init__.py
│       ├── main_page.py                # Page principale
│       └── preview_page.py             # Page prévisualisation
│
├── 🎨 assets/                          # Ressources statiques
│   └── icons/                          # Icônes SVG
│       ├── cleaning.svg
│       ├── folder.svg
│       └── ...
│
├── 🖼️ icon's/                          # Icônes application
│   ├── icon.ico                        # Icône Windows
│   ├── icon.png                        # Icône PNG
│   └── icon.svg                        # Icône SVG
│
├── 📚 Documentations/                  # Documentation complète
│   ├── INDEX.md                        # Index navigation
│   ├── README.md                       # Doc générale
│   ├── ORGANISATION.md                 # Organisation projet
│   ├── SECURITY_TOOLS.md               # Outils de sécurité
│   ├── SANDBOX_WIN32_ISOLATION.md      # Guide sandbox
│   ├── SERVICES_DEPENDENCIES.md        # Dépendances services
│   ├── ELEVATION_DRYRUN.md             # Élévation conditionnelle
│   ├── DRY_RUN_BUTTON.md               # Bouton dry-run
│   ├── FIX_ANTI_SPAM.md                # Fix anti-spam
│   └── ANTI_BYPASS_SECURITY.md         # Anti-contournement
│
├── 🤖 .github/                         # GitHub Actions
│   └── workflows/
│       └── build-and-sign.yml          # Workflow CI/CD
│
├── 🏗️ build/                           # Dossier de build (ignoré)
├── 📦 dist/                            # Distribution (ignoré)
└── 📄 .gitignore                       # Fichiers ignorés par Git
```

---

## 📦 Modules Backend

### `cleaner.py` - Fonctions de Nettoyage
**Responsabilités**:
- Nettoyage fichiers temporaires
- Gestion cache Windows Update
- Vidage corbeille
- Arrêt services sécurisé
- Libération RAM
- Flush DNS

**Sécurité**:
- ✅ Whitelists strictes
- ✅ 7 couches de validation
- ✅ API natives Windows (pas PowerShell)
- ✅ 12 services protégés

### `elevation.py` - Gestion Privilèges
**Responsabilités**:
- Vérification droits admin
- Élévation conditionnelle
- Pas de UAC forcé

### `logger.py` - Système de Logging
**Responsabilités**:
- Logs détaillés de toutes les opérations
- Sauvegarde dans `Documents/5GH'zCleaner-logs/`
- Traçabilité complète

### `security.py` - Vérifications Sécurité
**Responsabilités**:
- Vérification intégrité système
- Validation fichiers système
- Checks de sécurité

### `dry_run.py` - Mode Prévisualisation
**Responsabilités**:
- Simulation sans suppression
- Calcul espace libéré
- Rapport détaillé

### `telemetry_checker.py` - Vérificateur Télémétrie
**Responsabilités**:
- Vérification absence connexions réseau
- Détection collecte de données
- Rapport de conformité

---

## 🎨 Modules Frontend

### `app.py` - Application Principale
**Responsabilités**:
- Initialisation Flet
- Gestion navigation
- État global

### `design_system/` - Système de Design
**Composants**:
- `theme.py` - Tokens de design (couleurs, espacements)
- `buttons.py` - Boutons réutilisables
- `containers.py` - Conteneurs
- `text.py` - Composants texte
- `icons.py` - Icônes
- `inputs.py` - Champs de saisie

**Avantages**:
- ✅ Cohérence visuelle
- ✅ Maintenance facilitée
- ✅ Réutilisabilité

### `pages/` - Pages de l'Application
- `main_page.py` - Page principale avec onglets
- `preview_page.py` - Page de prévisualisation

---

## 🧪 Tests

### Tests de Sécurité
| Test | Fichier | Description |
|------|---------|-------------|
| Services | `test_service_dependencies.py` | Vérification dépendances |
| Élévation | `test_elevation_dryrun.py` | Test élévation conditionnelle |
| Dry-Run | `test_dry_run_button.py` | Test bouton obligatoire |
| Anti-Spam | `test_anti_spam.py` | Test protection spam |
| Anti-Bypass | `test_anti_bypass.py` | Test anti-contournement |

### Exécution des Tests
```bash
# Test individuel
python test_service_dependencies.py

# Tous les tests
python -m pytest tests/
```

---

## 🔧 Scripts Utilitaires

### `build.bat` - Compilation
Compile l'application en exécutable Windows avec PyInstaller.

```bash
build.bat
```

### `run.bat` - Lancement Rapide
Lance l'application en mode développement.

```bash
run.bat
```

### `generate_checksum.py` - Checksums
Génère les checksums SHA256 pour vérification d'intégrité.

```bash
python generate_checksum.py
```

---

## 📚 Documentation

### Structure
```
Documentations/
├── INDEX.md                    # Point d'entrée
├── README.md                   # Doc générale
├── ORGANISATION.md             # Organisation
├── SECURITY_TOOLS.md           # Outils sécurité
├── SANDBOX_WIN32_ISOLATION.md  # Guide sandbox
├── SERVICES_DEPENDENCIES.md    # Services
├── ELEVATION_DRYRUN.md         # Élévation
├── DRY_RUN_BUTTON.md           # Bouton
├── FIX_ANTI_SPAM.md            # Anti-spam
└── ANTI_BYPASS_SECURITY.md     # Anti-bypass
```

### Navigation
Commencez par [`Documentations/INDEX.md`](./Documentations/INDEX.md)

---

## 🤖 CI/CD

### GitHub Actions
**Fichier**: `.github/workflows/build-and-sign.yml`

**Workflow**:
1. Build automatique sur tag `v*`
2. Vérification télémétrie
3. Compilation PyInstaller
4. Signature numérique (si certificat)
5. Génération checksums
6. Création release GitHub

**Déclenchement**:
```bash
git tag v1.5.0
git push origin v1.5.0
```

---

## 📦 Dépendances

### `requirements.txt`
```
flet==0.25.2
pywin32==306
psutil==5.9.8
```

### Installation
```bash
pip install -r requirements.txt
```

---

## 🔒 Fichiers Sensibles

### À NE JAMAIS Committer
- `*.pfx` - Certificats code-signing
- `*.p12` - Certificats
- `certificate.*` - Fichiers de certificat
- `*.log` - Logs
- `build/` - Dossier de build
- `dist/` - Distribution

### Protection
Tous ces fichiers sont dans `.gitignore`.

---

## 🗑️ Fichiers Supprimés (Obsolètes)

Les fichiers suivants ont été supprimés car obsolètes:
- ❌ `DOCUMENTATION_GUIDE.txt` - Remplacé par INDEX.md
- ❌ `Documentations/.REGLES.txt` - Obsolète
- ❌ `Documentations/FIX_IMPORT_BODY.md` - Corrigé
- ❌ `Documentations/IMPROVEMENT_SCROLL.md` - Non implémenté
- ❌ `Documentations/PREVIEW_PAGE_SELECTION.md` - Obsolète

---

## 📊 Statistiques du Projet

### Code
- **Lignes de code Python**: ~3,500 lignes
- **Modules backend**: 6 fichiers
- **Modules frontend**: 12 fichiers
- **Tests**: 5 fichiers

### Documentation
- **Pages de documentation**: ~120 pages
- **Lignes de documentation**: ~4,000 lignes
- **Fichiers markdown**: 11 fichiers

### Sécurité
- **Score de sécurité**: 95/100 🟢
- **Services protégés**: 12
- **Couches de validation**: 7
- **Tests de sécurité**: 5

---

## 🎯 Conventions

### Nommage
- **Fichiers**: `snake_case.py`
- **Classes**: `PascalCase`
- **Fonctions**: `snake_case()`
- **Constantes**: `UPPER_SNAKE_CASE`

### Documentation
- **Format**: Markdown (.md)
- **Encodage**: UTF-8
- **Emojis**: Oui (pour clarté)

### Git
- **Branches**: `feature/`, `bugfix/`, `hotfix/`
- **Commits**: Messages descriptifs
- **Tags**: `v1.5.0` pour releases

---

## 🚀 Workflow de Développement

### 1. Développement
```bash
# Créer une branche
git checkout -b feature/nouvelle-fonctionnalite

# Développer et tester
python main.py

# Commit
git commit -m "feat: ajout nouvelle fonctionnalité"
```

### 2. Tests
```bash
# Exécuter les tests
python test_service_dependencies.py
python test_anti_bypass.py

# Vérifier télémétrie
python backend/telemetry_checker.py
```

### 3. Build
```bash
# Compiler
build.bat

# Générer checksums
python generate_checksum.py
```

### 4. Release
```bash
# Créer un tag
git tag v1.5.0

# Pousser
git push origin v1.5.0

# GitHub Actions s'occupe du reste
```

---

## 📞 Support

### Documentation
- [INDEX.md](./Documentations/INDEX.md) - Point d'entrée
- [README.md](./README.md) - Documentation principale
- [SECURITY.md](./SECURITY.md) - Rapport de sécurité

### Contact
- **Repository**: https://github.com/UndKiMi/5Ghz_Cleaner
- **Auteur**: UndKiMi
- **Issues**: https://github.com/UndKiMi/5Ghz_Cleaner/issues

---

**Document créé le**: 2025-10-12  
**Dernière mise à jour**: 2025-10-12  
**Version**: 1.0
