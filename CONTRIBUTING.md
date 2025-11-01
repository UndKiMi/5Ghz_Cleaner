# Guide de Contribution - 5GH'z Cleaner

## 🎯 Bonnes Pratiques pour les Audits GitHub

### ✅ Avant de Commit

1. **Vérifier la syntaxe Python**
   ```bash
   python -m py_compile main.py
   find src -name "*.py" -exec python -m py_compile {} \;
   ```

2. **Formater le code**
   ```bash
   black src/ --line-length 120
   isort src/ --profile black
   ```

3. **Linter**
   ```bash
   pylint src/ --exit-zero
   flake8 src/
   ```

4. **Tests de sécurité**
   ```bash
   bandit -r src/ -ll
   safety check
   ```

5. **Tests unitaires**
   ```bash
   pytest tests/ -v
   ```

### 📋 Checklist Pre-Commit

- [ ] Code formaté avec Black
- [ ] Imports organisés avec isort
- [ ] Pas d'erreurs Pylint critiques
- [ ] Pas de secrets dans le code
- [ ] Tests unitaires passent
- [ ] Documentation à jour

### 🔒 Sécurité

**À NE JAMAIS commit:**
- Clés API, tokens, passwords
- Fichiers `.env` avec secrets
- Credentials dans le code
- Données sensibles

**Utiliser:**
- Variables d'environnement
- GitHub Secrets
- Fichiers `.env.example` (sans valeurs réelles)

### 🚀 Workflow GitHub Actions

Tous les workflows sont configurés pour être **non-bloquants** :
- `continue-on-error: true` sur les checks non-critiques
- Warnings ne bloquent pas les PRs
- Seules les erreurs critiques bloquent

### 📊 Outils Configurés

| Outil | Fichier Config | But |
|-------|---------------|-----|
| Black | `pyproject.toml` | Formatage code |
| isort | `pyproject.toml` | Organisation imports |
| Pylint | `.pylintrc` | Qualité code |
| Flake8 | `.flake8` | Style code |
| Bandit | `.bandit` | Sécurité |
| Pytest | `pyproject.toml` | Tests unitaires |

### 🔧 Commandes Utiles

```bash
# Installer les outils de dev
pip install black isort pylint flake8 bandit safety pytest

# Formater tout le projet
black . && isort .

# Vérifier la qualité
pylint src/ && flake8 src/

# Tests de sécurité
bandit -r src/ && safety check

# Tests unitaires
pytest tests/ -v --cov=src
```

### 📝 Structure des Commits

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatage
- `refactor`: Refactoring
- `test`: Tests
- `chore`: Maintenance

**Exemples:**
```
feat(security): Add SHA256 integrity checker
fix(cleaner): Resolve cooldown timer bug
docs(readme): Update security audit section
```

### 🎯 Pull Requests

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing`)
3. Commit les changements (`git commit -m 'feat: Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing`)
5. Ouvrir une Pull Request

**La PR sera automatiquement testée par:**
- CI (validation structure)
- Security Audit (CodeQL, Bandit, Safety, Trivy)
- Code Quality (Pylint, Black, isort, Flake8)
- Secret Scanning (Gitleaks, TruffleHog)

### ⚡ Performance

- Utiliser `cache: 'pip'` dans les workflows
- Minimiser les dépendances
- Tests rapides (<5 min)
- Workflows parallèles

### 🐛 Debugging Workflows

Si un workflow échoue :

1. **Consulter les logs** dans Actions tab
2. **Reproduire localement** avec les mêmes commandes
3. **Vérifier les dépendances** dans requirements.txt
4. **Tester avec Docker** (même environnement)

```bash
# Tester dans un container Ubuntu
docker run -it -v $(pwd):/app python:3.11 bash
cd /app
pip install -r requirements.txt
# Exécuter les commandes du workflow
```

### 📚 Ressources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Python Best Practices](https://docs.python-guide.org/)
- [Security Best Practices](https://owasp.org/www-project-top-ten/)

---

**Merci de contribuer à 5GH'z Cleaner ! 🎉**
