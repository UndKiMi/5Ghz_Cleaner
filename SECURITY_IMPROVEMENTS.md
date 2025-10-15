# Améliorations de Sécurité - 5GHz Cleaner

## Date: 2025-01-XX

## Résumé des Corrections Appliquées

Ce document détaille toutes les améliorations de sécurité apportées au projet pour passer l'audit de sécurité GitHub.

---

## 1. Validation SSL et Sécurité des Téléchargements

### Fichier: `download_librehardwaremonitor.py`

**Problème identifié:**
- Téléchargement sans validation SSL stricte
- Pas de vérification de l'origine de l'URL

**Corrections appliquées:**
- ✅ Ajout de validation SSL stricte avec `ssl.create_default_context()`
- ✅ Vérification que l'URL provient uniquement de `github.com` via HTTPS
- ✅ Validation du schéma et du domaine avant téléchargement
- ✅ Configuration de `ssl.CERT_REQUIRED` et `check_hostname=True`

**Code ajouté:**
```python
# Validation de l'URL
parsed_url = urlparse(download_url)
if parsed_url.scheme != 'https':
    raise SecurityError("Only HTTPS URLs are allowed")
if parsed_url.netloc != 'github.com':
    raise SecurityError("Only github.com domain is allowed")

# Contexte SSL strict
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED
```

---

## 2. Sécurisation des Appels Subprocess

### Fichier: `backend/cleaner.py`

**Problème identifié:**
- Fonction `run_hidden()` sans validation stricte des commandes
- Risque d'injection de commandes

**Corrections appliquées:**
- ✅ Liste blanche des commandes autorisées (whitelist)
- ✅ Utilisation de chemins absolus pour toutes les commandes système
- ✅ Validation que `shell=False` est toujours utilisé
- ✅ Ajout de timeout de 30 secondes
- ✅ Validation du type et du contenu des arguments

**Code ajouté:**
```python
ALLOWED_COMMANDS = {
    'sc', 'sc.exe',
    'ipconfig', 'ipconfig.exe',
    'tasklist', 'tasklist.exe'
}

# Validation stricte
if cmd_name not in ALLOWED_COMMANDS:
    raise ValueError(f"Command not allowed: {cmd_name}")

# Chemins absolus
system32 = os.path.join(os.getenv('WINDIR', 'C:\\Windows'), 'System32')
cmd[0] = os.path.join(system32, 'sc.exe')
```

---

## 3. Sécurisation du Workflow GitHub Actions

### Fichier: `.github/workflows/security.yml`

**Problèmes identifiés:**
- Pas de pinning des versions d'actions (risque de supply chain attack)
- Permissions trop larges
- Pas de `persist-credentials: false`

**Corrections appliquées:**
- ✅ Pinning de toutes les actions avec SHA256 complet
- ✅ Ajout de `permissions: contents: read` par défaut
- ✅ Permissions minimales pour chaque job
- ✅ `persist-credentials: false` sur tous les checkouts
- ✅ Versions fixes pour les dépendances Python (bandit, safety, pylint)
- ✅ Exclusion des dossiers tiers de l'analyse

**Versions pinnées:**
```yaml
actions/checkout@692973e3d937129bcbf40652eb9f2f61becf3332  # v4.1.7
actions/setup-python@f677139bbe7f9c59b41e40162b753c062f5d49a3  # v5.2.0
actions/upload-artifact@50769540e7f4bd5e21e526ee35c689e35e0d6874  # v4.4.0
github/codeql-action/init@4dd16135b69a43b6c8efb853346f8437d92d3c93  # v3.26.6
```

---

## 4. Configuration des Outils de Sécurité

### Fichiers créés:

#### `.bandit`
Configuration pour Bandit (analyseur de sécurité Python):
- Exclusion des dossiers tiers (`libs`, `build`, `dist`)
- Niveau de sévérité: medium
- Niveau de confiance: medium

#### `.pylintrc`
Configuration pour Pylint (qualité de code):
- Exclusion des dossiers tiers
- Utilisation de 4 processus parallèles
- Désactivation des warnings non pertinents
- Longueur de ligne: 120 caractères

---

## 5. Sécurité Existante Maintenue

Le projet possédait déjà des mécanismes de sécurité robustes qui ont été conservés:

### Module `backend/security_core.py`
- ✅ 200+ chemins système protégés
- ✅ Validation stricte des opérations sur fichiers
- ✅ Liste blanche des dossiers temporaires autorisés
- ✅ Protection contre la suppression de fichiers système

### Module `backend/system_commands.py`
- ✅ Chemins absolus pour toutes les commandes Windows
- ✅ Timeouts configurables
- ✅ `shell=False` forcé partout
- ✅ Commentaires `# nosec B603` pour Bandit (justifiés)

---

## 6. Résumé des Vulnérabilités Corrigées

| Vulnérabilité | Sévérité | Status |
|---------------|----------|--------|
| Téléchargement sans validation SSL | HIGH | ✅ CORRIGÉ |
| Subprocess sans liste blanche | HIGH | ✅ CORRIGÉ |
| Actions GitHub non pinnées | MEDIUM | ✅ CORRIGÉ |
| Permissions GitHub trop larges | MEDIUM | ✅ CORRIGÉ |
| Pas de timeout sur subprocess | LOW | ✅ CORRIGÉ |

---

## 7. Tests de Validation

Pour valider les corrections:

### Test 1: Bandit
```bash
bandit -r . -f txt --exclude ./libs,./build,./dist
```

### Test 2: Safety
```bash
safety check
```

### Test 3: Pylint
```bash
pylint backend/ frontend/ config/ --rcfile=.pylintrc
```

### Test 4: CodeQL (via GitHub Actions)
- Push sur la branche principale
- Vérifier que le workflow passe sans erreurs

---

## 8. Bonnes Pratiques Implémentées

1. **Principe du moindre privilège**: Permissions minimales partout
2. **Defense in depth**: Plusieurs couches de validation
3. **Fail secure**: En cas d'erreur, refuser l'opération
4. **Input validation**: Validation stricte de toutes les entrées
5. **Secure by default**: Configuration sécurisée par défaut
6. **Supply chain security**: Pinning des dépendances

---

## 9. Maintenance Future

### À faire régulièrement:
- [ ] Mettre à jour les SHA des actions GitHub tous les 3 mois
- [ ] Vérifier les nouvelles vulnérabilités avec `safety check`
- [ ] Revoir les permissions GitHub Actions
- [ ] Auditer les nouvelles dépendances Python

### Commandes de maintenance:
```bash
# Mettre à jour safety
pip install --upgrade safety

# Scanner les vulnérabilités
safety check --full-report

# Vérifier les dépendances obsolètes
pip list --outdated
```

---

## 10. Références

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Actions Security Best Practices](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Bandit Documentation](https://bandit.readthedocs.io/)

---

**Auteur:** UndKiMi  
**Date:** 2025-01-XX  
**Version:** 1.0
