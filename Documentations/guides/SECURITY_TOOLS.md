# 🔐 Guide des Outils de Sécurité

## 📋 Vue d'ensemble

Ce guide explique comment utiliser tous les outils de sécurité intégrés dans **5GH'z Cleaner**.

---

## 🛠️ Outils Disponibles

### 1. Vérificateur de Télémétrie

**Fichier**: `backend/telemetry_checker.py`

#### Description
Vérifie qu'aucune donnée utilisateur n'est envoyée sans consentement explicite.

#### Utilisation

```bash
# Exécuter la vérification
python backend/telemetry_checker.py
```

#### Résultat Attendu

```
================================================================================
RAPPORT DE CONFORMITÉ TÉLÉMÉTRIE
================================================================================

[1/3] Vérification de l'activité réseau...
      ✓ No network connections detected

[2/3] Vérification des requêtes externes...
      ✓ No suspicious domain resolution detected

[3/3] Vérification de la collecte de données...
      ✓ No data collection files detected

================================================================================
RÉSUMÉ DE CONFORMITÉ
================================================================================
Activité réseau       : ✓ CONFORME
Requêtes externes     : ✓ CONFORME
Collecte de données   : ✓ CONFORME

✓ STATUT GLOBAL: CONFORME - Aucune télémétrie détectée
✓ Aucune donnée utilisateur n'est envoyée sans consentement
================================================================================
```

#### Que Vérifie-t-il?

1. **Activité réseau**: Aucune connexion réseau active
2. **Requêtes externes**: Aucun domaine suspect résolu
3. **Collecte de données**: Aucun fichier de tracking créé

---

### 2. Générateur de Checksums

**Fichier**: `generate_checksum.py`

#### Description
Génère les checksums SHA256 et MD5 pour vérifier l'intégrité des fichiers de distribution.

#### Utilisation

```bash
# Générer les checksums (après build)
python generate_checksum.py
```

#### Fichiers Générés

- `dist/CHECKSUMS.txt` - Format lisible
- `dist/CHECKSUMS.json` - Format machine

#### Exemple de Sortie

```
================================================================================
GÉNÉRATEUR DE CHECKSUM SHA256
================================================================================

[INFO] Found 1 file(s) to process

[INFO] Processing: 5Ghz_Cleaner.exe
      Calculating SHA256... ✓
      Calculating MD5... ✓

[SUCCESS] Checksums saved to: dist\CHECKSUMS.json
[SUCCESS] Readable checksums saved to: dist\CHECKSUMS.txt

================================================================================
RÉSUMÉ
================================================================================

5Ghz_Cleaner.exe:
  SHA256: a1b2c3d4e5f6...
  Taille: 15.42 MB

================================================================================
```

#### Vérifier l'Intégrité d'un Fichier

**Windows PowerShell**:
```powershell
Get-FileHash -Algorithm SHA256 5Ghz_Cleaner.exe
```

**Linux/Mac**:
```bash
shasum -a 256 5Ghz_Cleaner.exe
```

**Avec l'outil**:
```bash
python generate_checksum.py verify 5Ghz_Cleaner.exe <hash_attendu>
```

---

### 3. Point de Restauration Automatique

**Fichier**: `main.py` (fonction `create_restore_point()`)

#### Description
Crée automatiquement un point de restauration système avant chaque nettoyage.

#### Activation

✅ **Activé par défaut** dans la version 1.5

#### Fonctionnement

1. Au démarrage de l'application
2. Avant le premier nettoyage
3. Via API WMI native (pas PowerShell)

#### Sortie Console

```
[INFO] System restore point creation...
[INFO] Creating system restore point...
[INFO] System restore point created successfully
[SUCCESS] ✓ Restore point created - System protected
```

#### Restauration Manuelle

Si problème après nettoyage:

1. **Ouvrir**: `Créer un point de restauration`
2. **Cliquer**: `Restauration du système`
3. **Sélectionner**: `5GHz Cleaner - Before Cleaning`
4. **Suivre**: L'assistant de restauration

#### Désactiver (Non Recommandé)

Commenter dans `main.py`:
```python
# restore_created = create_restore_point()
```

---

### 4. Workflow GitHub Actions

**Fichier**: `.github/workflows/build-and-sign.yml`

#### Description
Automatise la compilation, signature et publication des releases.

#### Déclenchement

1. **Automatique**: Sur push de tag `v*` (ex: `v1.5.0`)
2. **Manuel**: Via l'onglet Actions sur GitHub

#### Étapes du Workflow

1. ✅ Checkout du code
2. ✅ Installation Python + dépendances
3. ✅ Vérification télémétrie
4. ✅ Build avec PyInstaller
5. ✅ Signature numérique (si certificat configuré)
6. ✅ Génération checksums
7. ✅ Création release GitHub
8. ✅ Upload des artifacts

#### Configuration Requise

**Secrets GitHub** (Settings > Secrets):
- `CERTIFICATE_BASE64`: Certificat PFX encodé en base64
- `CERTIFICATE_PASSWORD`: Mot de passe du certificat

#### Créer une Release

```bash
# Créer un tag
git tag v1.5.0

# Pousser le tag
git push origin v1.5.0

# Le workflow se déclenche automatiquement
```

#### Vérifier la Signature

```powershell
# Vérifier la signature numérique
Get-AuthenticodeSignature 5Ghz_Cleaner.exe

# Afficher les détails
Get-AuthenticodeSignature 5Ghz_Cleaner.exe | Format-List *
```

---

### 5. API Natives Windows (Anti-Injection)

**Fichiers**: `backend/cleaner.py`, `main.py`

#### Description
Remplacement de toutes les commandes PowerShell par des API natives Windows.

#### Changements Implémentés

| Fonction | Avant (PowerShell) | Après (API Native) |
|----------|-------------------|-------------------|
| Compter corbeille | `PowerShell Get-ChildItem` | `win32com.client` (COM) |
| Vider corbeille | `PowerShell Clear-RecycleBin` | `SHEmptyRecycleBinW` (ctypes) |
| Libérer RAM | `PowerShell Clear-PhysicalMemory` | `EmptyWorkingSet` (psutil) |
| Point restauration | `PowerShell Checkpoint-Computer` | WMI API (win32com) |

#### Vérification

Rechercher PowerShell dans le code:
```bash
grep -r "powershell" --include="*.py" .
```

**Résultat attendu**: Aucune occurrence dangereuse (seulement commentaires).

#### Avantages

- ✅ **Sécurité**: Pas d'injection de commandes
- ✅ **Performance**: Appels directs plus rapides
- ✅ **Fiabilité**: Moins de dépendances externes
- ✅ **Compatibilité**: Fonctionne même si PowerShell désactivé

---

## 📊 Tableau Récapitulatif

| Outil | Fichier | Commande | Fréquence |
|-------|---------|----------|-----------|
| Vérificateur télémétrie | `backend/telemetry_checker.py` | `python backend/telemetry_checker.py` | À chaque release |
| Générateur checksums | `generate_checksum.py` | `python generate_checksum.py` | Après chaque build |
| Point restauration | `main.py` | Automatique | À chaque démarrage |
| Workflow CI/CD | `.github/workflows/build-and-sign.yml` | Automatique | Sur tag `v*` |
| API natives | `backend/cleaner.py` | Automatique | Toujours actif |

---

## 🧪 Tests de Sécurité

### Test Complet

Exécuter tous les tests de sécurité:

```bash
# 1. Vérifier télémétrie
python backend/telemetry_checker.py

# 2. Tester dépendances services
python test_service_dependencies.py

# 3. Tester élévation
python test_elevation_dryrun.py

# 4. Tester dry-run
python test_dry_run_button.py

# 5. Tester anti-spam
python test_anti_spam.py

# 6. Tester anti-contournement
python test_anti_bypass.py
```

### Résultat Attendu

```
✓ Tous les tests passés (6/6)
✓ Aucune vulnérabilité détectée
✓ Score de sécurité: 95/100
```

---

## 🔍 Audit de Sécurité

### Commandes d'Audit

```bash
# Rechercher PowerShell dangereux
grep -r "powershell.*-Command" --include="*.py" .

# Rechercher subprocess avec shell=True
grep -r "shell=True" --include="*.py" .

# Rechercher connexions réseau
grep -r "urllib\|requests\|socket" --include="*.py" .

# Rechercher eval/exec dangereux
grep -r "eval\|exec" --include="*.py" .
```

### Résultats Attendus

Toutes les commandes doivent retourner **aucun résultat** (ou seulement des commentaires).

---

## 📚 Documentation Supplémentaire

- [SECURITY.md](../SECURITY.md) - Rapport de sécurité complet
- [SANDBOX_WIN32_ISOLATION.md](./SANDBOX_WIN32_ISOLATION.md) - Guide sandbox
- [ANTI_BYPASS_SECURITY.md](./ANTI_BYPASS_SECURITY.md) - Protection anti-contournement

---

## 🐛 Signaler un Problème de Sécurité

Si vous découvrez une vulnérabilité:

1. **NE PAS** créer d'issue publique
2. Contacter: security@github.com/UndKiMi
3. Inclure:
   - Description détaillée
   - Étapes de reproduction
   - Impact potentiel
   - Suggestions de correction

**Délai de réponse**: 48 heures maximum

---

**Version**: 1.0  
**Dernière mise à jour**: 2025-10-12  
**Auteur**: UndKiMi
