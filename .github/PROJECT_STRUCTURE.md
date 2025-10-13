# 📁 Structure du Projet - Réorganisation Professionnelle

## 🎯 Nouvelle Structure

```
5Ghz_Cleaner/
├── .github/                    # GitHub configuration
│   ├── workflows/              # CI/CD workflows
│   │   └── security-audit.yml  # Security tests
│   ├── ISSUE_TEMPLATE/         # Issue templates
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── PROJECT_STRUCTURE.md    # This file
│
├── docs/                       # 📚 Documentation principale
│   ├── README.md               # Documentation overview
│   ├── QUICK_START.md          # Quick start guide
│   ├── INSTALLATION.md         # Installation guide
│   ├── SECURITY.md             # Security report
│   ├── PRIVACY.md              # Privacy policy
│   ├── CONTRIBUTING.md         # Contribution guide
│   ├── WINDOWS_11_ONLY.md      # Compatibility guide
│   ├── guides/                 # Detailed guides
│   │   ├── CODE_SIGNING_GUIDE.md
│   │   ├── SECURITY_TOOLS.md
│   │   └── SANDBOX_WIN32_ISOLATION.md
│   └── technical/              # Technical documentation
│       ├── ARCHITECTURE.md
│       ├── PROJECT_STRUCTURE.md
│       └── API_REFERENCE.md
│
├── src/                        # 💻 Code source
│   ├── backend/                # Backend logic
│   │   ├── __init__.py
│   │   ├── cleaner.py
│   │   ├── security_core.py
│   │   ├── security.py
│   │   ├── system_commands.py
│   │   ├── elevation.py
│   │   ├── logger.py
│   │   ├── dry_run.py
│   │   ├── hardware_monitor.py
│   │   ├── signature_manager.py
│   │   └── telemetry_checker.py
│   ├── frontend/               # Frontend UI
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── design_system/
│   │   └── pages/
│   └── config/                 # Configuration files
│       └── settings.py
│
├── tests/                      # 🧪 Tests
│   ├── __init__.py
│   ├── test_all_security.py
│   ├── test_coverage_complete.py
│   ├── test_privacy_complete.py
│   └── run_all_tests.py
│
├── scripts/                    # 🔧 Utility scripts
│   ├── build/                  # Build scripts
│   │   ├── build.bat
│   │   └── compile.ps1
│   ├── signing/                # Code signing
│   │   ├── create_self_signed_cert.ps1
│   │   └── sign_executable.ps1
│   └── verification/           # Verification scripts
│       ├── generate_checksum.py
│       ├── verify_checksum.py
│       └── verify_no_powershell.py
│
├── assets/                     # 📦 Static resources
│   ├── icons/
│   └── images/
│
├── build/                      # 🏗️ Build artifacts (gitignored)
├── dist/                       # 📦 Distribution files (gitignored)
│
├── .gitignore                  # Git ignore rules
├── .gitattributes              # Git attributes
├── LICENSE                     # CC BY-NC-SA 4.0
├── README.md                   # Main readme
├── CHANGELOG.md                # Version history
├── requirements.txt            # Python dependencies
├── requirements-dev.txt        # Dev dependencies
├── setup.py                    # Setup configuration
└── main.py                     # Entry point

```

## 📋 Fichiers à Déplacer

### Documentation → docs/
- QUICK_START.md
- INSTALLATION.md
- SECURITY.md
- PRIVACY.md
- CONTRIBUTING.md
- WINDOWS_11_ONLY.md
- Documentations/* → docs/guides/

### Code → src/
- backend/* → src/backend/
- frontend/* → src/frontend/
- config/* → src/config/

### Scripts → scripts/ (déjà organisé)
- Créer sous-dossiers: build/, signing/, verification/

### Fichiers à Supprimer (obsolètes)
- ARCHITECTURE_MAJOR_UPDATE.md (dupliquer dans docs/technical/)
- CHANGELOG_MAJOR_UPDATE.md (fusionner dans CHANGELOG.md)
- FINAL_SUMMARY.md (obsolète)
- GITHUB_READY.md (obsolète)
- GPU_TEMP_DETECTION.md (déplacer dans docs/technical/)
- RELEASE_READY.md (obsolète)
- SUMMARY_MAJOR_UPDATE.md (obsolète)
- TEST_REPORT_FINAL.md (déplacer dans docs/technical/)
- COMPATIBILITY_UPDATE.md (fusionner dans WINDOWS_11_ONLY.md)
- SECURITY_IMPROVEMENTS.md (fusionner dans SECURITY.md)
- test_hardware_monitor.py (déplacer dans tests/)
- 5Ghz_Cleaner.spec (build artifact)
- app.manifest (déplacer dans config/)
- CHECKSUMS.txt (build artifact)
- SIGNATURE.json (build artifact)

## 🎯 Avantages de la Nouvelle Structure

### 1. Clarté
- Documentation séparée du code
- Structure standard Python
- Facile à naviguer

### 2. Professionnalisme
- Structure reconnue par la communauté
- Compatible avec les outils Python
- Meilleure organisation

### 3. Maintenance
- Fichiers groupés logiquement
- Moins de clutter à la racine
- Plus facile à maintenir

### 4. Scalabilité
- Facile d'ajouter de nouveaux modules
- Structure extensible
- Séparation des responsabilités

## 📝 Notes

- Les fichiers de build (build/, dist/) restent gitignored
- La structure src/ permet l'import: `from src.backend import cleaner`
- Les tests peuvent importer: `from src.backend.cleaner import *`
- Documentation centralisée dans docs/
