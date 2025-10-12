# 📋 PLAN DE RESTRUCTURATION - 5GHz Cleaner

## 🎯 Objectif
Restructurer le projet selon les meilleures pratiques Python/Windows pour un projet de sécurité système.

---

## 📁 Structure Actuelle (Analyse)

```
5Ghz_Cleaner/
├── backend/              ✅ BIEN - Modules Python
├── frontend/             ✅ BIEN - Interface Flet
├── tests/                ✅ BIEN - Tests unitaires
├── assets/               ✅ BIEN - Ressources
├── Documentations/       ⚠️  À renommer en docs/
├── icon's/               ⚠️  À renommer en icons/
├── build/                ⚠️  À ignorer (gitignore)
├── dist/                 ⚠️  À ignorer (gitignore)
├── __pycache__/          ⚠️  À ignorer (gitignore)
├── *.md (multiples)      ⚠️  À organiser
├── main.py               ✅ BIEN - Point d'entrée
├── requirements.txt      ✅ BIEN
└── ...                   ⚠️  Fichiers à trier
```

### Problèmes Identifiés
1. **Documentation dispersée**: 10+ fichiers .md à la racine
2. **Noms non-standards**: `icon's/`, `Documentations/`
3. **Fichiers de build**: Non ignorés dans git
4. **Pas de structure src/**: Code directement à la racine
5. **Scripts utilitaires**: Mélangés avec le code principal

---

## 📁 Structure Proposée (Best Practices)

```
5Ghz_Cleaner/
├── src/                          # Code source principal
│   ├── __init__.py
│   ├── main.py                   # Point d'entrée
│   ├── backend/                  # Logique métier
│   │   ├── __init__.py
│   │   ├── core/                 # Modules core
│   │   │   ├── __init__.py
│   │   │   ├── cleaner.py
│   │   │   ├── security_core.py
│   │   │   └── signature_manager.py
│   │   ├── utils/                # Utilitaires
│   │   │   ├── __init__.py
│   │   │   ├── elevation.py
│   │   │   ├── logger.py
│   │   │   └── telemetry_checker.py
│   │   ├── security/             # Sécurité
│   │   │   ├── __init__.py
│   │   │   ├── security.py
│   │   │   └── dry_run.py
│   │   └── config/               # Configuration
│   │       ├── __init__.py
│   │       ├── blocklist.py
│   │       └── settings.py
│   └── frontend/                 # Interface utilisateur
│       ├── __init__.py
│       ├── app.py
│       ├── design_system/
│       └── pages/
│
├── tests/                        # Tests unitaires et d'intégration
│   ├── __init__.py
│   ├── unit/                     # Tests unitaires
│   │   ├── __init__.py
│   │   ├── test_security_core.py
│   │   ├── test_confirmations.py
│   │   └── test_restore_point.py
│   ├── integration/              # Tests d'intégration
│   │   ├── __init__.py
│   │   └── test_full_workflow.py
│   ├── fixtures/                 # Données de test
│   │   └── __init__.py
│   └── run_all_tests.py
│
├── docs/                         # Documentation complète
│   ├── README.md                 # Documentation principale
│   ├── INSTALLATION.md           # Guide d'installation
│   ├── USAGE.md                  # Guide d'utilisation
│   ├── SECURITY.md               # Politique de sécurité
│   ├── CONTRIBUTING.md           # Guide de contribution
│   ├── CHANGELOG.md              # Historique des versions
│   ├── API.md                    # Documentation API
│   ├── ARCHITECTURE.md           # Architecture du projet
│   ├── guides/                   # Guides détaillés
│   │   ├── dry-run.md
│   │   ├── elevation.md
│   │   └── services.md
│   └── reports/                  # Rapports d'audit
│       ├── security-audit.md
│       ├── improvements.md
│       └── restructuration.md
│
├── scripts/                      # Scripts utilitaires
│   ├── build.bat
│   ├── run.bat
│   ├── generate_checksum.py
│   └── setup_dev.py
│
├── assets/                       # Ressources statiques
│   ├── icons/                    # Icônes
│   │   ├── app.ico
│   │   └── ...
│   └── images/                   # Images
│       └── ...
│
├── config/                       # Fichiers de configuration
│   ├── blocklist.json
│   ├── settings.json
│   └── logging.json
│
├── .github/                      # GitHub Actions
│   ├── workflows/
│   │   ├── tests.yml
│   │   ├── security-scan.yml
│   │   └── build.yml
│   └── ISSUE_TEMPLATE/
│
├── .vscode/                      # Configuration VS Code
│   ├── settings.json
│   └── launch.json
│
├── build/                        # Build artifacts (gitignored)
├── dist/                         # Distribution (gitignored)
│
├── .gitignore                    # Git ignore
├── .gitattributes                # Git attributes
├── README.md                     # README principal
├── LICENSE                       # Licence
├── requirements.txt              # Dépendances production
├── requirements-dev.txt          # Dépendances développement
├── setup.py                      # Setup Python
├── pyproject.toml                # Configuration projet
├── MANIFEST.in                   # Manifest
└── 5Ghz_Cleaner.spec            # PyInstaller spec
```

---

## 🔄 Plan de Migration

### Phase 1: Préparation
1. ✅ Créer la nouvelle structure de dossiers
2. ✅ Backup du projet actuel
3. ✅ Créer les fichiers __init__.py nécessaires

### Phase 2: Migration du Code
1. ✅ Déplacer `backend/` → `src/backend/`
2. ✅ Déplacer `frontend/` → `src/frontend/`
3. ✅ Déplacer `main.py` → `src/main.py`
4. ✅ Réorganiser les modules backend en sous-dossiers

### Phase 3: Migration de la Documentation
1. ✅ Créer `docs/`
2. ✅ Déplacer `Documentations/` → `docs/guides/`
3. ✅ Organiser les fichiers .md dans `docs/`
4. ✅ Créer `docs/reports/` pour les rapports

### Phase 4: Migration des Tests
1. ✅ Organiser `tests/` en `unit/` et `integration/`
2. ✅ Créer `tests/fixtures/`
3. ✅ Ajouter `__init__.py` partout

### Phase 5: Migration des Assets
1. ✅ Renommer `icon's/` → `assets/icons/`
2. ✅ Organiser les ressources

### Phase 6: Scripts et Configuration
1. ✅ Créer `scripts/` pour les utilitaires
2. ✅ Créer `config/` pour les configurations
3. ✅ Déplacer les scripts de build

### Phase 7: Fichiers de Configuration
1. ✅ Créer `setup.py`
2. ✅ Créer `pyproject.toml`
3. ✅ Créer `requirements-dev.txt`
4. ✅ Mettre à jour `.gitignore`

### Phase 8: Documentation
1. ✅ Créer `CONTRIBUTING.md`
2. ✅ Améliorer `SECURITY.md`
3. ✅ Créer `INSTALLATION.md`
4. ✅ Créer `USAGE.md`

---

## 📝 Fichiers à Créer

### Configuration
- [ ] `setup.py` - Installation Python
- [ ] `pyproject.toml` - Configuration moderne
- [ ] `requirements-dev.txt` - Dépendances dev
- [ ] `MANIFEST.in` - Fichiers à inclure
- [ ] `.gitattributes` - Attributs Git

### Documentation
- [ ] `docs/INSTALLATION.md` - Guide installation
- [ ] `docs/USAGE.md` - Guide utilisation
- [ ] `docs/CONTRIBUTING.md` - Guide contribution
- [ ] `docs/API.md` - Documentation API
- [ ] `docs/ARCHITECTURE.md` - Architecture

### Tests
- [ ] `tests/integration/test_full_workflow.py`
- [ ] `tests/fixtures/__init__.py`
- [ ] `tests/conftest.py` - Configuration pytest

### CI/CD
- [ ] `.github/workflows/tests.yml`
- [ ] `.github/workflows/security-scan.yml`
- [ ] `.github/workflows/build.yml`

---

## 🔒 Améliorations de Sécurité

### Blocklist Centralisée
```python
# config/blocklist.json
{
  "forbidden_paths": [
    "C:\\Windows\\System32",
    "C:\\Windows\\SysWOW64",
    ...
  ],
  "forbidden_extensions": [
    ".sys", ".dll", ".exe", ...
  ],
  "forbidden_patterns": [
    "ntoskrnl.*", "hal.*", ...
  ]
}
```

### Configuration Sécurisée
```python
# config/settings.json
{
  "security": {
    "require_admin": true,
    "create_restore_point": true,
    "confirm_critical_operations": true,
    "max_file_size": 10737418240,
    "allowed_temp_dirs": [...]
  },
  "logging": {
    "level": "INFO",
    "file": "logs/cleaner.log",
    "max_size": 10485760
  }
}
```

---

## 🧪 Tests Améliorés

### Structure de Tests
```
tests/
├── unit/                 # Tests unitaires
│   ├── test_security_core.py
│   ├── test_cleaner.py
│   ├── test_elevation.py
│   └── ...
├── integration/          # Tests d'intégration
│   ├── test_full_workflow.py
│   ├── test_dry_run_to_clean.py
│   └── ...
├── fixtures/             # Données de test
│   ├── test_files/
│   └── mock_data/
└── conftest.py           # Configuration pytest
```

### Couverture de Code
- Objectif: 90%+ de couverture
- Outil: pytest-cov
- Badge dans README

---

## 📊 Métriques de Qualité

### Outils à Intégrer
- **pytest**: Tests unitaires
- **pytest-cov**: Couverture de code
- **black**: Formatage automatique
- **flake8**: Linting
- **mypy**: Type checking
- **bandit**: Analyse de sécurité
- **safety**: Vérification dépendances

### GitHub Actions
- Tests automatiques sur chaque PR
- Scan de sécurité quotidien
- Build automatique des releases

---

## 🎯 Priorités

### Haute Priorité
1. ✅ Restructuration des dossiers
2. ✅ Migration du code source
3. ✅ Organisation de la documentation
4. ✅ Amélioration .gitignore

### Priorité Moyenne
1. ⏳ Création setup.py et pyproject.toml
2. ⏳ Tests d'intégration
3. ⏳ GitHub Actions
4. ⏳ Documentation API

### Basse Priorité
1. ⏳ VS Code configuration
2. ⏳ Docker support
3. ⏳ Internationalisation

---

## 📅 Timeline

- **Jour 1**: Phases 1-3 (Structure + Code)
- **Jour 2**: Phases 4-6 (Tests + Assets + Scripts)
- **Jour 3**: Phases 7-8 (Config + Documentation)
- **Jour 4**: Tests et validation
- **Jour 5**: CI/CD et finalisation

---

**Auteur**: UndKiMi  
**Date**: 12 Octobre 2025  
**Version**: 1.6.0 → 2.0.0  
**Status**: 📋 PLAN APPROUVÉ
