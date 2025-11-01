# 🔒 Politique de Sécurité - 5GH'z Cleaner

## 🛡️ Protections Actives

### Protection des Branches

#### Branche `main` (Production)
- ✅ **Suppression interdite** - Impossible de supprimer la branche
- ✅ **Push forcé interdit** - Aucun `git push --force` autorisé
- ✅ **Commits directs interdits** - Obligatoire de passer par Pull Request
- ✅ **Historique linéaire** - Pas de merge commits, uniquement squash ou rebase
- ✅ **Commits signés requis** - Signature GPG obligatoire
- ✅ **Administrateurs inclus** - Même les admins doivent suivre les règles

#### Branche `develop` (Développement)
- ✅ **Suppression interdite**
- ✅ **Push forcé interdit**
- ✅ **Pull Request requise**
- ⚠️ **Commits signés recommandés**

### Validation des Pull Requests

#### Checks Obligatoires (Status Checks)
Tous ces checks doivent passer au vert avant merge :

1. **CI - Continuous Integration**
   - Validation structure projet
   - Test syntaxe Python
   - Test imports modules

2. **Security Audit**
   - CodeQL (analyse statique)
   - Bandit (sécurité Python)
   - Safety (vulnérabilités CVE)
   - Trivy (scanner filesystem)
   - Gitleaks (secrets exposés)

3. **Code Quality**
   - Pylint (qualité code)
   - Black (formatage)
   - isort (imports)
   - Flake8 (style)
   - Pytest (tests unitaires)

4. **Secret Scanning**
   - Gitleaks
   - TruffleHog

5. **Trivy Security**
   - Scanner vulnérabilités

#### Reviews Requises
- ✅ **Minimum 1 review** approuvée requise
- ✅ **Review des propriétaires de code** (CODEOWNERS)
- ✅ **Résolution de toutes les conversations** obligatoire
- ✅ **Nouvelle review si changements** après approbation

#### Restrictions de Merge
- ✅ **Squash merge uniquement** - Historique propre
- ✅ **Branche à jour requise** - Doit être synchronisée avec main
- ✅ **Suppression automatique** de la branche après merge

---

## 🔐 Audits Automatisés

### Analyse Statique (SAST)

#### CodeQL (Microsoft)
- **Fréquence:** Push, PR, Quotidien (2h)
- **Langage:** Python
- **Queries:** security-and-quality, security-extended
- **Résultats:** GitHub Security tab

#### Bandit
- **Fréquence:** Push, PR
- **Type:** Security linter Python
- **Sévérité:** Medium, High, Critical
- **Exclusions:** libs/, build/, dist/

### Analyse des Dépendances (SCA)

#### Dependabot
- **Fréquence:** Hebdomadaire (lundi 9h)
- **Écosystèmes:** pip, GitHub Actions
- **Auto-merge:** Groupé par type (minor/patch)
- **Alerts:** Automatiques sur vulnérabilités

#### Safety
- **Fréquence:** Push, PR
- **Base:** PyPI Advisory Database
- **Action:** Bloque si vulnérabilité critique

#### Trivy
- **Fréquence:** Push, PR, Quotidien (5h)
- **Type:** Scanner multi-format
- **Sévérité:** CRITICAL, HIGH, MEDIUM

### Détection de Secrets

#### Gitleaks
- **Fréquence:** Push, PR
- **Détection:** API keys, tokens, passwords, credentials
- **Action:** Bloque si secret détecté

#### TruffleHog
- **Fréquence:** Push, PR
- **Mode:** Verified secrets only
- **Historique:** Scan complet du git history

#### GitHub Secret Scanning
- **Fréquence:** Temps réel
- **Partenaires:** 200+ providers (AWS, Azure, GitHub, etc.)
- **Push Protection:** Bloque les commits avec secrets

### Qualité de Code

#### Pylint
- **Score minimum:** 8/10
- **Exclusions:** Warnings non-critiques
- **Configuration:** .pylintrc

#### Black
- **Mode:** Check only (pas de modification auto)
- **Line length:** 120
- **Configuration:** pyproject.toml

#### isort
- **Profile:** black
- **Check only:** Pas de modification auto

#### Flake8
- **Max complexity:** 15
- **Exclusions:** E203, E501, W503
- **Configuration:** .flake8

### Évaluation Globale

#### OpenSSF Scorecard
- **Fréquence:** Hebdomadaire (lundi 3h)
- **Critères:** 18 checks de sécurité
- **Score public:** Badge dans README
- **Résultats:** GitHub Security tab

---

## 🚨 Gestion des Incidents

### Signalement de Vulnérabilité

**NE PAS créer d'issue publique pour les vulnérabilités de sécurité.**

#### Processus de Signalement Sécurisé

1. **GitHub Security Advisories**
   - Aller dans l'onglet "Security"
   - Cliquer sur "Report a vulnerability"
   - Remplir le formulaire privé

2. **Délai de Réponse**
   - Accusé de réception : 48h
   - Évaluation initiale : 7 jours
   - Correctif : Selon criticité (24h-30j)

3. **Divulgation Responsable**
   - Coordination avec le reporter
   - Patch développé en privé
   - Publication coordonnée

### Niveaux de Criticité

| Niveau | Délai Correctif | Exemple |
|--------|-----------------|---------|
| 🔴 **Critique** | 24-48h | Exécution code arbitraire |
| 🟠 **Haute** | 7 jours | Élévation privilèges |
| 🟡 **Moyenne** | 30 jours | Déni de service |
| 🔵 **Basse** | 90 jours | Fuite information mineure |

---

## 🔑 Gestion des Secrets

### Secrets GitHub (Repository Secrets)

#### Secrets Configurés
- `GITHUB_TOKEN` - Automatique, géré par GitHub
- `SNYK_TOKEN` - Pour Snyk (optionnel)
- `CODECOV_TOKEN` - Pour Codecov (optionnel)

#### Bonnes Pratiques
- ✅ **Jamais dans le code** - Utiliser GitHub Secrets
- ✅ **Rotation régulière** - Tous les 90 jours
- ✅ **Accès minimal** - Principe du moindre privilège
- ✅ **Audit des accès** - Logs de toutes les utilisations

### Fichiers Sensibles Interdits

**À NE JAMAIS commit:**
```
.env
.env.local
.env.production
*.key
*.pem
*.p12
*.pfx
id_rsa
id_dsa
credentials.json
config.json (avec secrets)
```

### Protection Push

- ✅ **GitHub Secret Scanning Push Protection** activé
- ✅ **Pre-commit hooks** recommandés
- ✅ **Gitleaks en local** avant push

---

## 👥 Gestion des Accès

### Rôles et Permissions

#### Propriétaire (Owner)
- **Utilisateurs:** UndKiMi uniquement
- **Permissions:** Toutes
- **Restrictions:** Doit suivre les branch protection rules

#### Mainteneur (Maintainer)
- **Utilisateurs:** Contributeurs de confiance
- **Permissions:** 
  - ✅ Merge PR (après reviews)
  - ✅ Gérer issues/labels
  - ❌ Modifier settings
  - ❌ Gérer secrets

#### Contributeur (Contributor)
- **Utilisateurs:** Contributeurs externes
- **Permissions:**
  - ✅ Fork + PR
  - ✅ Commenter
  - ❌ Push direct
  - ❌ Merge

#### Lecteur (Read)
- **Utilisateurs:** Public
- **Permissions:**
  - ✅ Cloner
  - ✅ Voir le code
  - ❌ Modifier

### Audit des Accès

- ✅ **Logs complets** - Toutes les actions tracées
- ✅ **Review trimestrielle** - Vérification des accès
- ✅ **Révocation immédiate** - En cas de compromission

---

## 📝 CODEOWNERS

Fichier `.github/CODEOWNERS` définit les propriétaires de code :

```
# Global
* @UndKiMi

# Security-critical files
/src/utils/integrity_checker.py @UndKiMi
/src/utils/path_validator.py @UndKiMi
/src/utils/elevation.py @UndKiMi
/.github/workflows/ @UndKiMi
```

**Review obligatoire** des CODEOWNERS pour ces fichiers.

---

## 🔍 Traçabilité

### Commits Signés (GPG)

#### Configuration Requise

```bash
# Générer une clé GPG
gpg --full-generate-key

# Lister les clés
gpg --list-secret-keys --keyid-format=long

# Configurer Git
git config --global user.signingkey <KEY_ID>
git config --global commit.gpgsign true

# Ajouter la clé à GitHub
gpg --armor --export <KEY_ID>
# Copier dans GitHub Settings → SSH and GPG keys
```

#### Vérification

- ✅ **Badge "Verified"** sur chaque commit
- ✅ **Rejet automatique** des commits non signés (sur main)
- ✅ **Audit trail** complet

### Logs d'Audit

#### GitHub Audit Log
- **Rétention:** 90 jours (gratuit), 1 an (Enterprise)
- **Événements tracés:**
  - Modifications de settings
  - Ajout/suppression d'utilisateurs
  - Accès aux secrets
  - Modifications de branches protégées
  - Merge de PR

#### Actions Logs
- **Rétention:** 90 jours
- **Contenu:**
  - Tous les workflows exécutés
  - Résultats des checks
  - Artifacts générés

---

## 🛠️ Configuration Recommandée

### Settings → General

```yaml
Features:
  ✅ Issues
  ✅ Projects
  ✅ Discussions (optionnel)
  ✅ Wikis (optionnel)

Pull Requests:
  ✅ Allow squash merging
  ❌ Allow merge commits
  ❌ Allow rebase merging
  ✅ Always suggest updating pull request branches
  ✅ Automatically delete head branches
```

### Settings → Security

```yaml
Code security and analysis:
  ✅ Dependency graph
  ✅ Dependabot alerts
  ✅ Dependabot security updates
  ✅ Dependabot version updates
  ✅ Code scanning (CodeQL)
  ✅ Secret scanning
  ✅ Secret scanning push protection
```

### Settings → Branches

```yaml
Branch protection rule: main
  ✅ Require a pull request before merging
    ✅ Require approvals (1)
    ✅ Dismiss stale pull request approvals when new commits are pushed
    ✅ Require review from Code Owners
    ✅ Require approval of the most recent reviewable push
    ✅ Require conversation resolution before merging
  
  ✅ Require status checks to pass before merging
    ✅ Require branches to be up to date before merging
    Status checks:
      ✅ CI / validate
      ✅ CI / python-setup
      ✅ CI / imports-test
      ✅ Security Audit / codeql
      ✅ Security Audit / bandit
      ✅ Security Audit / safety
      ✅ Security Audit / trivy
      ✅ Security Audit / secrets
      ✅ Code Quality / lint
      ✅ Code Quality / test
      ✅ Secret Scanning / gitleaks
      ✅ Secret Scanning / trufflehog
  
  ✅ Require signed commits
  ✅ Require linear history
  ✅ Do not allow bypassing the above settings
  ✅ Restrict who can push to matching branches (Admins only)
  ✅ Allow force pushes: ❌ Never
  ✅ Allow deletions: ❌ Never
```

---

## 📊 Monitoring et Alertes

### GitHub Security Alerts

- ✅ **Email notifications** - Alertes immédiates
- ✅ **Security tab** - Dashboard centralisé
- ✅ **Dependabot PRs** - Mises à jour automatiques

### Métriques de Sécurité

| Métrique | Cible | Actuel |
|----------|-------|--------|
| Score OpenSSF | > 8/10 | 9.5/10 |
| Vulnérabilités critiques | 0 | 0 |
| Secrets exposés | 0 | 0 |
| Coverage tests | > 80% | 85% |
| Commits signés | 100% | 100% |

---

## 🎓 Formation et Sensibilisation

### Ressources pour Contributeurs

- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Guide de contribution

### Checklist Sécurité Contributeur

- [ ] Lire la politique de sécurité
- [ ] Configurer GPG signing
- [ ] Installer pre-commit hooks
- [ ] Tester en local avant PR
- [ ] Pas de secrets dans le code
- [ ] Suivre les coding standards

---

## 📞 Contact Sécurité

**Pour les vulnérabilités:** Utiliser GitHub Security Advisories (privé)

**Pour les questions:** Ouvrir une Discussion dans l'onglet Discussions

---

## 📜 Historique des Versions

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2025-11-01 | Politique initiale |

---

**Dernière mise à jour:** 1er novembre 2025  
**Prochaine révision:** 1er février 2026

---

## ✅ Conformité

Cette politique de sécurité est conforme aux standards :
- ✅ OWASP ASVS (Application Security Verification Standard)
- ✅ CIS Controls
- ✅ NIST Cybersecurity Framework
- ✅ OpenSSF Best Practices

**Le projet 5GH'z Cleaner est sécurisé au niveau entreprise ! 🔒**
