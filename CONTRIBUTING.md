# 🤝 Guide de Contribution - 5GHz Cleaner

Merci de votre intérêt pour contribuer à 5GHz Cleaner! Ce document vous guidera à travers le processus de contribution.

---

## 📋 Table des Matières

1. [Code de Conduite](#code-de-conduite)
2. [Comment Contribuer](#comment-contribuer)
3. [Standards de Code](#standards-de-code)
4. [Processus de Pull Request](#processus-de-pull-request)
5. [Tests](#tests)
6. [Sécurité](#sécurité)
7. [Documentation](#documentation)

---

## 📜 Code de Conduite

### Notre Engagement

Nous nous engageons à faire de la participation à ce projet une expérience exempte de harcèlement pour tous, indépendamment de:
- L'âge
- La taille corporelle
- Le handicap
- L'ethnicité
- L'identité et l'expression de genre
- Le niveau d'expérience
- La nationalité
- L'apparence personnelle
- La race
- La religion
- L'identité et l'orientation sexuelles

### Comportements Attendus

- ✅ Utiliser un langage accueillant et inclusif
- ✅ Respecter les points de vue et expériences différents
- ✅ Accepter gracieusement les critiques constructives
- ✅ Se concentrer sur ce qui est le mieux pour la communauté
- ✅ Faire preuve d'empathie envers les autres membres

### Comportements Inacceptables

- ❌ Langage ou imagerie sexualisés
- ❌ Trolling, commentaires insultants/désobligeants
- ❌ Harcèlement public ou privé
- ❌ Publication d'informations privées sans permission
- ❌ Autre conduite inappropriée dans un cadre professionnel

---

## 🚀 Comment Contribuer

### Types de Contributions

#### 🐛 Signaler un Bug
1. Vérifiez que le bug n'a pas déjà été signalé
2. Utilisez le template d'issue "Bug Report"
3. Incluez:
   - Version de Windows
   - Version de l'application
   - Steps to reproduce
   - Comportement attendu vs actuel
   - Screenshots si applicable

#### 💡 Proposer une Fonctionnalité
1. Vérifiez que la fonctionnalité n'a pas déjà été proposée
2. Utilisez le template d'issue "Feature Request"
3. Expliquez:
   - Le problème que ça résout
   - La solution proposée
   - Les alternatives considérées

#### 📝 Améliorer la Documentation
1. Identifiez ce qui manque ou est confus
2. Proposez une amélioration claire
3. Suivez le style de documentation existant

#### 🔒 Signaler une Vulnérabilité
⚠️ **NE PAS créer d'issue publique!**
- Envoyez un email à: security@example.com
- Voir [SECURITY.md](SECURITY.md) pour plus de détails

---

## 💻 Standards de Code

### Style Python

Nous suivons [PEP 8](https://pep8.org/) avec quelques adaptations:

```python
# ✅ BON
def calculate_file_hash(filepath: str, algorithm: str = "sha256") -> str:
    """
    Calcule le hash d'un fichier.
    
    Args:
        filepath: Chemin du fichier
        algorithm: Algorithme de hash (sha256, sha512)
        
    Returns:
        str: Hash hexadécimal du fichier
        
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
    """
    hash_obj = hashlib.new(algorithm)
    
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hash_obj.update(chunk)
    
    return hash_obj.hexdigest()

# ❌ MAUVAIS
def calc_hash(f,a="sha256"):
    h=hashlib.new(a)
    with open(f,'rb') as file:
        while True:
            c=file.read(8192)
            if not c:break
            h.update(c)
    return h.hexdigest()
```

### Conventions de Nommage

```python
# Variables et fonctions: snake_case
user_name = "John"
def get_user_data():
    pass

# Classes: PascalCase
class SecurityManager:
    pass

# Constantes: UPPER_CASE
MAX_FILE_SIZE = 10485760
FORBIDDEN_PATHS = frozenset({...})

# Privé: _prefixe
def _internal_function():
    pass
```

### Documentation

Toutes les fonctions publiques doivent avoir une docstring:

```python
def function_name(param1: type, param2: type = default) -> return_type:
    """
    Description courte (une ligne).
    
    Description longue si nécessaire, expliquant le comportement,
    les cas particuliers, etc.
    
    Args:
        param1: Description du paramètre 1
        param2: Description du paramètre 2 (optionnel)
        
    Returns:
        Description de la valeur de retour
        
    Raises:
        ExceptionType: Quand cette exception est levée
        
    Examples:
        >>> function_name("test", 42)
        "result"
    """
    pass
```

### Gestion des Erreurs

```python
# ✅ BON: Gestion spécifique
try:
    result = risky_operation()
except FileNotFoundError as e:
    logger.error(f"File not found: {e}")
    return None
except PermissionError as e:
    logger.error(f"Permission denied: {e}")
    return None

# ❌ MAUVAIS: Catch-all silencieux
try:
    result = risky_operation()
except:
    pass
```

### Sécurité

```python
# ✅ BON: Validation avant opération
def delete_file(filepath: str) -> bool:
    # Validation du chemin
    is_safe, reason = security_core.validate_operation(filepath, "delete")
    if not is_safe:
        logger.warning(f"Operation blocked: {reason}")
        return False
    
    # Vérification supplémentaire
    if not is_in_allowed_temp_directory(filepath):
        logger.warning(f"Path not in allowed directories: {filepath}")
        return False
    
    # Opération
    try:
        os.remove(filepath)
        return True
    except Exception as e:
        logger.error(f"Failed to delete {filepath}: {e}")
        return False

# ❌ MAUVAIS: Pas de validation
def delete_file(filepath):
    os.remove(filepath)
```

---

## 🔄 Processus de Pull Request

### 1. Fork et Clone

```bash
# Fork le repository sur GitHub
# Puis clone votre fork
git clone https://github.com/VOTRE-USERNAME/5Ghz_Cleaner.git
cd 5Ghz_Cleaner
```

### 2. Créer une Branche

```bash
# Créer une branche descriptive
git checkout -b feature/add-new-cleaning-module
git checkout -b fix/security-validation-bug
git checkout -b docs/improve-installation-guide
```

### 3. Développer

```bash
# Installer les dépendances de développement
pip install -r requirements-dev.txt

# Faire vos modifications
# ...

# Tester localement
pytest tests/
```

### 4. Commit

```bash
# Commits atomiques avec messages clairs
git add .
git commit -m "feat: Add new cleaning module for browser cache

- Implement Chrome cache cleaning
- Add Firefox cache cleaning
- Add Edge cache cleaning
- Add tests for all browsers
- Update documentation

Closes #123"
```

### Format des Messages de Commit

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatage (pas de changement de code)
- `refactor`: Refactoring
- `test`: Ajout/modification de tests
- `chore`: Maintenance

**Exemples**:
```
feat(security): Add triple validation layer

Implement three-layer validation system:
1. Security core validation
2. Legacy checks
3. Final validation before execution

Closes #456

fix(cleaner): Fix Windows.old confirmation bypass

The confirmation check was not properly enforced
when called from the UI. Added explicit check
at function entry point.

Fixes #789

docs(readme): Update installation instructions

- Add Windows 11 specific notes
- Clarify admin requirements
- Add troubleshooting section
```

### 5. Push et Pull Request

```bash
# Push vers votre fork
git push origin feature/add-new-cleaning-module

# Créer une Pull Request sur GitHub
# Utilisez le template fourni
```

### 6. Review

- Répondez aux commentaires de review
- Faites les modifications demandées
- Mettez à jour votre PR

```bash
# Après modifications
git add .
git commit -m "fix: Address review comments"
git push origin feature/add-new-cleaning-module
```

---

## 🧪 Tests

### Exécuter les Tests

```bash
# Tous les tests
pytest tests/

# Tests spécifiques
pytest tests/unit/test_security_core.py

# Avec couverture
pytest --cov=src tests/

# Avec rapport HTML
pytest --cov=src --cov-report=html tests/
```

### Écrire des Tests

```python
# tests/unit/test_new_feature.py
import pytest
from src.backend.core import new_feature

class TestNewFeature:
    """Tests pour la nouvelle fonctionnalité"""
    
    def test_basic_functionality(self):
        """Test du comportement de base"""
        result = new_feature.do_something("input")
        assert result == "expected_output"
    
    def test_error_handling(self):
        """Test de la gestion d'erreur"""
        with pytest.raises(ValueError):
            new_feature.do_something(None)
    
    def test_security_validation(self):
        """Test de la validation de sécurité"""
        # Tentative d'accès à un chemin interdit
        result = new_feature.process_file("C:\\Windows\\System32\\test.dll")
        assert result is False
        
    @pytest.mark.parametrize("input,expected", [
        ("test1", "result1"),
        ("test2", "result2"),
        ("test3", "result3"),
    ])
    def test_multiple_cases(self, input, expected):
        """Test de plusieurs cas"""
        assert new_feature.do_something(input) == expected
```

### Couverture de Code

Objectif: **90%+** de couverture

```bash
# Générer le rapport de couverture
pytest --cov=src --cov-report=term-missing tests/

# Vérifier la couverture minimale
pytest --cov=src --cov-fail-under=90 tests/
```

---

## 🔒 Sécurité

### Checklist de Sécurité

Avant de soumettre une PR, vérifiez:

- [ ] Aucun `eval()` ou `exec()`
- [ ] Aucun `input()` non validé
- [ ] Tous les chemins de fichiers validés
- [ ] Toutes les commandes système sécurisées
- [ ] Gestion d'erreurs robuste
- [ ] Logs appropriés (pas de données sensibles)
- [ ] Tests de sécurité ajoutés
- [ ] Documentation de sécurité mise à jour

### Validation de Sécurité

```python
# ✅ Toujours valider avant opération
is_safe, reason = security_core.validate_operation(path, operation)
if not is_safe:
    logger.warning(f"Security check failed: {reason}")
    return False

# ✅ Toujours vérifier les permissions
if not os.access(path, os.W_OK):
    logger.warning(f"No write permission: {path}")
    return False

# ✅ Toujours gérer les erreurs
try:
    operation()
except PermissionError as e:
    logger.error(f"Permission denied: {e}")
    return False
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return False
```

---

## 📚 Documentation

### Structure de la Documentation

```
docs/
├── README.md              # Vue d'ensemble
├── INSTALLATION.md        # Guide d'installation
├── USAGE.md               # Guide d'utilisation
├── API.md                 # Documentation API
├── ARCHITECTURE.md        # Architecture du projet
├── SECURITY.md            # Politique de sécurité
├── CONTRIBUTING.md        # Ce fichier
└── guides/                # Guides détaillés
    ├── dry-run.md
    ├── elevation.md
    └── ...
```

### Style de Documentation

- Utilisez Markdown
- Incluez des exemples de code
- Ajoutez des screenshots si pertinent
- Maintenez à jour avec le code

---

## 🎯 Checklist Avant Soumission

Avant de soumettre votre PR, vérifiez:

### Code
- [ ] Le code suit PEP 8
- [ ] Toutes les fonctions ont des docstrings
- [ ] Pas de code commenté inutile
- [ ] Pas de `print()` de debug
- [ ] Variables et fonctions bien nommées

### Tests
- [ ] Tous les tests passent
- [ ] Nouveaux tests ajoutés pour nouvelles fonctionnalités
- [ ] Couverture de code ≥ 90%
- [ ] Tests de sécurité inclus

### Documentation
- [ ] README mis à jour si nécessaire
- [ ] Docstrings ajoutées/mises à jour
- [ ] CHANGELOG.md mis à jour
- [ ] Commentaires de code clairs

### Sécurité
- [ ] Checklist de sécurité complétée
- [ ] Aucune vulnérabilité introduite
- [ ] Validation appropriée
- [ ] Gestion d'erreurs robuste

### Git
- [ ] Messages de commit clairs
- [ ] Commits atomiques
- [ ] Branche à jour avec main
- [ ] Pas de conflits

---

## 📝 Templates d'Issues et PR

### 🐛 Template Bug Report

```markdown
**Description du Bug**
Description claire et concise du bug.

**Étapes pour Reproduire**
1. Aller à '...'
2. Cliquer sur '...'
3. Voir l'erreur

**Comportement Attendu**
Ce qui devrait se passer.

**Comportement Actuel**
Ce qui se passe réellement.

**Environnement**
- OS: [ex: Windows 11 23H2]
- Version: [ex: MAJOR UPDATE]
- Python: [ex: 3.11.5]
- Mode: [Admin / Standard]

**Logs**
Collez les logs pertinents ici

**Screenshots**
Si applicable
```

### 💡 Template Feature Request

```markdown
**Problème à Résoudre**
Description du problème.

**Solution Proposée**
Description de la solution.

**Alternatives**
Autres solutions envisagées.

**Impact Sécurité**
Comment cela affecte la sécurité?
```

### 🔀 Template Pull Request

```markdown
## Description
Changements apportés.

## Type
- [ ] Bug fix
- [ ] Nouvelle fonctionnalité
- [ ] Breaking change
- [ ] Documentation

## Checklist
- [ ] Code suit PEP 8
- [ ] Auto-review effectuée
- [ ] Documentation mise à jour
- [ ] Tests ajoutés
- [ ] Sécurité vérifiée
- [ ] CHANGELOG.md mis à jour

## Tests
Description des tests.

Closes #(issue)
```

---

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/UndKiMi/5Ghz_Cleaner/issues)
- **Discussions**: [GitHub Discussions](https://github.com/UndKiMi/5Ghz_Cleaner/discussions)
- **Security**: Voir [SECURITY.md](SECURITY.md) pour les vulnérabilités
- **Questions**: Ouvrez une Discussion GitHub

---

## 🙏 Remerciements

Merci à tous les contributeurs qui aident à améliorer 5GHz Cleaner!

---

**Auteur**: UndKiMi  
**Date**: Décembre 2024  
**Version**: MAJOR UPDATE  
**Dernière révision**: Décembre 2024
