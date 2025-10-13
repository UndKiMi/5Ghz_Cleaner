# 📁 Structure du Projet - 5GH'z Cleaner

## 📋 Vue d'ensemble

Ce document décrit l'organisation complète du projet 5GH'z Cleaner.

**Version**: MAJOR UPDATE  
**Auteur**: UndKiMi

---

## 🗂️ Structure des Dossiers

```
5Ghz_Cleaner/
│
├── 📄 Fichiers Racine (Configuration et Documentation Principale)
│   ├── README.md                    # Documentation principale du projet
│   ├── SECURITY.md                  # Rapport de sécurité complet (85/100)
│   ├── CONTRIBUTING.md              # Guide de contribution
│   ├── LICENSE                      # Licence CC BY-NC-SA 4.0
│   ├── CHANGELOG.md                 # Historique des versions
│   ├── PRIVACY.md                   # Politique de confidentialité
│   ├── INSTALLATION.md              # Guide d'installation
│   ├── PROJECT_STRUCTURE.md         # Ce fichier
│   ├── requirements.txt             # Dépendances Python
│   ├── requirements-dev.txt         # Dépendances développement
│   ├── setup.py                     # Configuration installation
│   ├── .gitignore                   # Fichiers ignorés par Git
│   └── main.py                      # Point d'entrée de l'application
│
├── 📂 .github/ (Configuration GitHub)
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md            # Template rapport de bug
│   │   └── feature_request.md       # Template demande de fonctionnalité
│   ├── PULL_REQUEST_TEMPLATE.md     # Template pull request
│   └── workflows/
│       └── security-audit.yml       # CI/CD audit de sécurité
│
├── 📂 backend/ (Logique Métier)
│   ├── cleaner.py                   # Fonctions de nettoyage
│   ├── security.py                  # Gestionnaire de sécurité
│   ├── security_core.py             # Protection système (226 chemins)
│   ├── hardware_monitor.py          # Monitoring matériel
│   ├── telemetry_checker.py         # Vérification télémétrie
│   ├── signature_manager.py         # Gestion signatures
│   └── __init__.py
│
├── 📂 frontend/ (Interface Utilisateur)
│   ├── pages/
│   │   ├── main_page.py             # Page principale
│   │   ├── preview_page.py          # Page prévisualisation
│   │   ├── settings_page.py         # Page paramètres
│   │   └── __init__.py
│   ├── components/
│   │   ├── header.py                # En-tête
│   │   ├── footer.py                # Pied de page
│   │   └── __init__.py
│   └── __init__.py
│
├── 📂 tests/ (Tests Automatisés)
│   ├── test_all_security.py         # Tests sécurité (7/7 ✓)
│   ├── test_coverage_complete.py    # Tests unitaires (31/31 ✓)
│   ├── test_security_core.py        # Tests security_core
│   ├── test_confirmations.py        # Tests confirmations
│   ├── test_restore_point.py        # Tests point restauration
│   ├── test_anti_bypass.py          # Tests anti-contournement
│   ├── test_anti_spam.py            # Tests anti-spam
│   ├── test_dry_run_button.py       # Tests dry-run
│   ├── test_elevation_dryrun.py     # Tests élévation
│   ├── test_service_dependencies.py # Tests services
│   ├── run_all_tests.py             # Lanceur de tests
│   └── __init__.py
│
├── 📂 scripts/ (Scripts Utilitaires)
│   ├── README.md                    # Documentation scripts
│   ├── create_self_signed_cert.ps1  # Création certificat auto-signé
│   ├── sign_executable.ps1          # Signature exécutable
│   ├── generate_checksum.py         # Génération checksums
│   ├── verify_checksum.py           # Vérification checksums
│   └── cert/                        # Certificats (ignoré par Git)
│
├── 📂 Documentations/ (Documentation Technique)
│   ├── INDEX.md                     # Index de la documentation
│   ├── CODE_SIGNING_GUIDE.md        # Guide certificat code signing
│   ├── ANTI_BYPASS_SECURITY.md      # Protection anti-contournement
│   ├── SERVICES_DEPENDENCIES.md     # Dépendances services
│   ├── SANDBOX_WIN32_ISOLATION.md   # Guide sandboxing
│   ├── SECURITY_TOOLS.md            # Outils de sécurité
│   └── reports/                     # Rapports d'audit
│       ├── SECURITY_AUDIT_2025.md
│       ├── SIGNATURE_UPGRADE.md
│       └── ...
│
├── 📂 assets/ (Ressources)
│   ├── icons/                       # Icônes
│   ├── images/                      # Images
│   └── fonts/                       # Polices
│
├── 📂 config/ (Configuration)
│   └── (fichiers de configuration)
│
├── 📂 dist/ (Distribution - Ignoré par Git)
│   └── 5Ghz_Cleaner.exe            # Exécutable compilé
│
└── 📂 build/ (Build - Ignoré par Git)
    └── (fichiers de build temporaires)
```

---

## 📄 Fichiers Principaux

### Documentation Utilisateur

| Fichier | Description | Lignes |
|---------|-------------|--------|
| **README.md** | Documentation principale, démarrage rapide | ~420 |
| **INSTALLATION.md** | Guide d'installation détaillé | ~290 |
| **PRIVACY.md** | Politique de confidentialité | ~95 |
| **CHANGELOG.md** | Historique des versions | ~120 |

### Documentation Sécurité

| Fichier | Description | Score |
|---------|-------------|-------|
| **SECURITY.md** | Rapport sécurité complet | 85/100 |
| **CODE_SIGNING_GUIDE.md** | Guide certificat officiel | 300+ lignes |
| **ANTI_BYPASS_SECURITY.md** | Protection anti-contournement | Complet |

### Documentation Développeur

| Fichier | Description | Utilité |
|---------|-------------|---------|
| **CONTRIBUTING.md** | Guide de contribution | Templates inclus |
| **PROJECT_STRUCTURE.md** | Structure du projet | Ce fichier |
| **setup.py** | Configuration installation | PyPI ready |

---

## 🔧 Modules Backend

### Module de Sécurité (Critique)

```python
backend/
├── security_core.py         # 226 chemins protégés, 184 fichiers critiques
├── security.py              # WinVerifyTrust API, validation
└── telemetry_checker.py     # Vérification aucune télémétrie
```

**Fonctionnalités:**
- ✅ Protection système maximale
- ✅ 100% API natives Windows
- ✅ Validation triple couche
- ✅ Tests: 31/31 passent

### Module de Nettoyage

```python
backend/
└── cleaner.py               # Fonctions de nettoyage sécurisées
```

**Fonctionnalités:**
- ✅ Dry-run obligatoire
- ✅ Point de restauration auto
- ✅ Logs détaillés
- ✅ Gestion d'erreurs robuste

### Module de Monitoring

```python
backend/
└── hardware_monitor.py      # Monitoring CPU, RAM, GPU, Disques
```

**Fonctionnalités:**
- ✅ Mise à jour temps réel
- ✅ Code couleur température
- ✅ Thread daemon léger
- ✅ < 1% CPU overhead

---

## 🎨 Modules Frontend

### Pages

```python
frontend/pages/
├── main_page.py             # Page principale avec onglets
├── preview_page.py          # Prévisualisation dry-run
└── settings_page.py         # Configuration et monitoring
```

### Composants

```python
frontend/components/
├── header.py                # En-tête avec logo
└── footer.py                # Pied de page avec infos
```

**Framework:** Flet (Flutter for Python)  
**Design:** Material Design 3  
**Thème:** Sombre par défaut

---

## 🧪 Tests

### Tests de Sécurité

| Test | Tests | Statut |
|------|-------|--------|
| **test_all_security.py** | 7/7 | ✅ 100% |
| **test_coverage_complete.py** | 31/31 | ✅ 100% |

**Couverture estimée:** ~92%

### Suites de Tests

1. ✅ `test_security_core.py` - Protection système
2. ✅ `test_confirmations.py` - Confirmations utilisateur
3. ✅ `test_restore_point.py` - Points de restauration
4. ✅ `test_anti_bypass.py` - Anti-contournement
5. ✅ `test_anti_spam.py` - Anti-spam
6. ✅ `test_dry_run_button.py` - Dry-run obligatoire
7. ✅ `test_elevation_dryrun.py` - Élévation conditionnelle
8. ✅ `test_service_dependencies.py` - Services Windows

---

## 📜 Scripts

### Certificat Code Signing

```powershell
scripts/
├── create_self_signed_cert.ps1    # Création certificat auto-signé
└── sign_executable.ps1            # Signature exécutable
```

**Usage:**
```powershell
# 1. Créer le certificat (une fois)
.\create_self_signed_cert.ps1

# 2. Signer l'exécutable
.\sign_executable.ps1 -FilePath "dist\5Ghz_Cleaner.exe"
```

### Checksums

```python
scripts/
├── generate_checksum.py           # Génération SHA256+SHA512
└── verify_checksum.py             # Vérification intégrité
```

---

## 🔒 Fichiers de Sécurité

### Signatures et Checksums

```
CHECKSUMS.txt                      # Checksums lisibles
SIGNATURE.json                     # Signatures numériques
checksums.json                     # Format JSON pour automatisation
```

### Certificats (Non commités)

```
scripts/cert/
├── 5GHz_Cleaner_Dev.cer          # Certificat public
└── 5GHz_Cleaner_Dev.pfx          # Certificat + clé privée
```

**⚠️ IMPORTANT:** Les certificats sont dans `.gitignore` et ne doivent JAMAIS être commités!

---

## 📊 Métriques du Projet

### Code

| Métrique | Valeur |
|----------|--------|
| **Lignes de code** | ~5000+ |
| **Modules backend** | 7 |
| **Modules frontend** | 5 |
| **Tests** | 31 unitaires + 7 sécurité |
| **Couverture** | ~92% |

### Documentation

| Type | Fichiers | Lignes |
|------|----------|--------|
| **Markdown** | 20+ | 3000+ |
| **Docstrings** | 100+ | 500+ |
| **Commentaires** | 200+ | 300+ |

### Sécurité

| Aspect | Valeur |
|--------|--------|
| **Score global** | 85/100 |
| **Chemins protégés** | 226 |
| **Fichiers critiques** | 184 |
| **Tests sécurité** | 38/38 ✓ |

---

## 🚀 Workflow de Développement

### 1. Développement Local

```bash
# Cloner le repo
git clone https://github.com/UndKiMi/5Ghz_Cleaner.git
cd 5Ghz_Cleaner

# Installer les dépendances
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Lancer l'application
python main.py
```

### 2. Tests

```bash
# Tests de sécurité
python tests/test_all_security.py

# Tests unitaires
python tests/test_coverage_complete.py

# Tous les tests
python tests/run_all_tests.py
```

### 3. Build

```bash
# Compiler l'exécutable
flet pack main.py --name "5Ghz_Cleaner"

# Signer l'exécutable
.\scripts\sign_executable.ps1 -FilePath "dist\5Ghz_Cleaner.exe"

# Générer les checksums
python scripts/generate_checksum.py
```

### 4. Release

```bash
# 1. Mettre à jour CHANGELOG.md
# 2. Créer un tag Git
git tag -a vMAJOR_UPDATE -m "MAJOR UPDATE"
git push origin vMAJOR_UPDATE

# 3. Créer une release GitHub avec:
#    - Exécutable signé
#    - CHECKSUMS.txt
#    - SIGNATURE.json
```

---

## 📚 Documentation Complète

### Pour les Utilisateurs

1. **README.md** - Démarrage rapide
2. **INSTALLATION.md** - Installation détaillée
3. **PRIVACY.md** - Confidentialité
4. **SECURITY.md** - Sécurité (lecture recommandée)

### Pour les Développeurs

1. **CONTRIBUTING.md** - Comment contribuer
2. **PROJECT_STRUCTURE.md** - Structure du projet
3. **Documentations/INDEX.md** - Index technique
4. **CODE_SIGNING_GUIDE.md** - Certificat officiel

### Pour les Auditeurs

1. **SECURITY.md** - Rapport sécurité complet
2. **tests/** - 38 tests automatisés
3. **backend/security_core.py** - Code de protection
4. **Documentations/reports/** - Rapports d'audit

---

## 🔄 Maintenance

### Fichiers à Mettre à Jour Régulièrement

| Fichier | Fréquence | Raison |
|---------|-----------|--------|
| **CHANGELOG.md** | Chaque release | Historique |
| **README.md** | Changements majeurs | Documentation |
| **SECURITY.md** | Audit sécurité | Score et analyse |
| **requirements.txt** | Nouvelles dépendances | Installation |

### Fichiers Générés Automatiquement

| Fichier | Générateur | Quand |
|---------|------------|-------|
| **CHECKSUMS.txt** | `generate_checksum.py` | Chaque build |
| **SIGNATURE.json** | `signature_manager.py` | Chaque build |
| **bandit-report.json** | GitHub Actions | Chaque commit |

---

## 🆘 Support

### Documentation

- **README.md** - Vue d'ensemble
- **Documentations/INDEX.md** - Index complet
- **GitHub Issues** - Questions et bugs

### Contact

- **GitHub**: https://github.com/UndKiMi/5Ghz_Cleaner
- **Issues**: https://github.com/UndKiMi/5Ghz_Cleaner/issues
- **Discussions**: https://github.com/UndKiMi/5Ghz_Cleaner/discussions

---

**Auteur**: UndKiMi  
**Version**: MAJOR UPDATE  
**Licence**: CC BY-NC-SA 4.0
