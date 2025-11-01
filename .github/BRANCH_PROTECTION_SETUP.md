# 🔒 Configuration des Protections de Branche

## ⚠️ IMPORTANT
Ces configurations doivent être appliquées manuellement via l'interface GitHub.
GitHub ne permet pas (pour des raisons de sécurité) de configurer les branch protection rules via fichiers.

---

## 📋 Checklist de Configuration

### 1. Settings → General

#### Features
- [x] ✅ Issues
- [x] ✅ Projects  
- [ ] ⚪ Discussions (optionnel)
- [ ] ⚪ Wikis (optionnel)

#### Pull Requests
- [x] ✅ Allow squash merging
- [ ] ❌ Allow merge commits
- [ ] ❌ Allow rebase merging
- [x] ✅ Always suggest updating pull request branches
- [x] ✅ Automatically delete head branches

---

### 2. Settings → Security & Analysis

#### Dependency graph
- [x] ✅ Enable

#### Dependabot
- [x] ✅ Dependabot alerts
- [x] ✅ Dependabot security updates
- [x] ✅ Dependabot version updates

#### Code scanning
- [x] ✅ CodeQL analysis (via workflows)

#### Secret scanning
- [x] ✅ Secret scanning
- [x] ✅ Push protection

---

### 3. Settings → Branches → Add Rule

#### Branch name pattern
```
main
```

#### Protect matching branches

##### Require a pull request before merging
- [x] ✅ Enable
  - [x] ✅ Require approvals: **1**
  - [x] ✅ Dismiss stale pull request approvals when new commits are pushed
  - [x] ✅ Require review from Code Owners
  - [x] ✅ Require approval of the most recent reviewable push
  - [x] ✅ Require conversation resolution before merging

##### Require status checks to pass before merging
- [x] ✅ Enable
  - [x] ✅ Require branches to be up to date before merging
  
**Status checks required (cocher tous):**
```
CI / validate
CI / python-setup
CI / imports-test
Security Audit / codeql
Security Audit / bandit
Security Audit / safety
Security Audit / trivy
Security Audit / secrets
Code Quality / lint
Code Quality / test
Secret Scanning / gitleaks
Secret Scanning / trufflehog
```

##### Require signed commits
- [x] ✅ Enable

##### Require linear history
- [x] ✅ Enable

##### Do not allow bypassing the above settings
- [x] ✅ Enable (même les admins doivent suivre les règles)

##### Restrict who can push to matching branches
- [x] ✅ Enable
  - Ajouter: **UndKiMi** (ou votre username)
  - Ou laisser vide pour "Admins only"

##### Allow force pushes
- [ ] ❌ Disable (JAMAIS autoriser)

##### Allow deletions
- [ ] ❌ Disable (JAMAIS autoriser)

---

### 4. Settings → Branches → Add Rule (Develop)

#### Branch name pattern
```
develop
```

#### Protect matching branches

##### Require a pull request before merging
- [x] ✅ Enable
  - [x] ✅ Require approvals: **1**
  - [x] ✅ Dismiss stale pull request approvals when new commits are pushed
  - [x] ✅ Require conversation resolution before merging

##### Require status checks to pass before merging
- [x] ✅ Enable
  - [x] ✅ Require branches to be up to date before merging
  - Cocher les mêmes status checks que main

##### Require linear history
- [x] ✅ Enable

##### Allow force pushes
- [ ] ❌ Disable

##### Allow deletions
- [ ] ❌ Disable

---

### 5. Settings → Actions → General

#### Actions permissions
- [x] ✅ Allow all actions and reusable workflows

#### Workflow permissions
- [x] ✅ Read and write permissions
- [x] ✅ Allow GitHub Actions to create and approve pull requests

#### Fork pull request workflows
- [x] ✅ Require approval for first-time contributors

---

### 6. Settings → Secrets and variables → Actions

#### Repository secrets (à créer si nécessaire)

```
SNYK_TOKEN (optionnel)
Description: Token pour Snyk security scanning
```

```
CODECOV_TOKEN (optionnel)
Description: Token pour Codecov coverage reports
```

**Note:** `GITHUB_TOKEN` est automatiquement fourni par GitHub.

---

### 7. Settings → Collaborators and teams

#### Manage access

**Propriétaire (Owner):**
- UndKiMi - Admin

**Mainteneurs (si nécessaire):**
- Aucun par défaut
- Ajouter uniquement des personnes de confiance
- Role: Maintain

**Contributeurs externes:**
- Pas d'accès direct
- Contribution via Fork + Pull Request

---

## 🔐 Configuration GPG (Commits Signés)

### Étape 1: Générer une clé GPG

```bash
# Windows (avec Git Bash ou WSL)
gpg --full-generate-key

# Choisir:
# - Type: (1) RSA and RSA
# - Taille: 4096
# - Expiration: 1y (1 an)
# - Nom: Votre nom
# - Email: Votre email GitHub
```

### Étape 2: Lister les clés

```bash
gpg --list-secret-keys --keyid-format=long

# Résultat:
# sec   rsa4096/ABCD1234EFGH5678 2025-11-01 [SC] [expires: 2026-11-01]
#       XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# uid                 [ultimate] Your Name <your.email@example.com>
# ssb   rsa4096/IJKL9012MNOP3456 2025-11-01 [E] [expires: 2026-11-01]

# Copier l'ID: ABCD1234EFGH5678
```

### Étape 3: Exporter la clé publique

```bash
gpg --armor --export ABCD1234EFGH5678

# Copier tout le bloc (de -----BEGIN PGP PUBLIC KEY BLOCK----- à -----END PGP PUBLIC KEY BLOCK-----)
```

### Étape 4: Ajouter à GitHub

1. GitHub → Settings → SSH and GPG keys
2. New GPG key
3. Coller la clé publique
4. Add GPG key

### Étape 5: Configurer Git

```bash
# Configurer la clé
git config --global user.signingkey ABCD1234EFGH5678

# Activer la signature automatique
git config --global commit.gpgsign true

# Configurer GPG program (Windows)
git config --global gpg.program "C:/Program Files/Git/usr/bin/gpg.exe"
```

### Étape 6: Tester

```bash
# Faire un commit de test
git commit --allow-empty -m "test: GPG signature"

# Vérifier la signature
git log --show-signature -1

# Résultat attendu:
# gpg: Signature made ...
# gpg: Good signature from "Your Name <your.email@example.com>"
```

---

## 🧪 Validation de la Configuration

### Checklist de Validation

#### Branch Protection
```bash
# Tester que push direct est bloqué
git checkout main
echo "test" >> test.txt
git add test.txt
git commit -m "test"
git push origin main
# ❌ Devrait être rejeté: "protected branch hook declined"
```

#### Pull Request Required
```bash
# Créer une branche
git checkout -b feature/test
echo "test" >> test.txt
git add test.txt
git commit -S -m "test: signed commit"
git push origin feature/test

# Créer une PR sur GitHub
# ✅ Devrait nécessiter:
# - 1 review
# - Tous les checks au vert
# - Conversations résolues
```

#### Signed Commits
```bash
# Vérifier sur GitHub
# Chaque commit doit avoir un badge "Verified" vert
```

#### Secret Scanning
```bash
# Tester (NE PAS PUSH UN VRAI SECRET!)
echo "github_pat_FAKE123456789" >> test.txt
git add test.txt
git commit -m "test"
git push
# ❌ Devrait être bloqué par push protection
```

---

## 📊 Monitoring

### Vérifications Régulières

#### Hebdomadaire
- [ ] Vérifier les Dependabot PRs
- [ ] Vérifier les Security Alerts
- [ ] Vérifier les Failed Workflows

#### Mensuel
- [ ] Review des accès utilisateurs
- [ ] Audit des secrets
- [ ] Vérification OpenSSF Scorecard

#### Trimestriel
- [ ] Rotation des secrets
- [ ] Review complète de sécurité
- [ ] Mise à jour de la documentation

---

## 🆘 Troubleshooting

### Problème: Push rejeté

**Erreur:**
```
remote: error: GH006: Protected branch update failed
```

**Solution:**
1. Créer une branche
2. Faire une Pull Request
3. Attendre les reviews et checks

### Problème: Commit non signé

**Erreur:**
```
remote: error: GH007: Commits must be signed
```

**Solution:**
```bash
# Configurer GPG
git config --global commit.gpgsign true

# Re-signer le dernier commit
git commit --amend --no-edit -S

# Force push sur la branche (PAS sur main!)
git push --force-with-lease
```

### Problème: Status checks échouent

**Solution:**
1. Consulter les logs dans Actions tab
2. Corriger les erreurs
3. Push les corrections
4. Attendre que les checks repassent

---

## 📚 Ressources

- [GitHub Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [GitHub Security Features](https://docs.github.com/en/code-security)
- [GPG Signing](https://docs.github.com/en/authentication/managing-commit-signature-verification)
- [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)

---

**Configuration complétée le:** 1er novembre 2025  
**Prochaine révision:** 1er février 2026

**Le dépôt est maintenant sécurisé au niveau entreprise ! 🔒🛡️**
