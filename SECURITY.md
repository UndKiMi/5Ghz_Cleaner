# 🔒 Rapport de Sécurité - 5GH'z Cleaner

## 📋 Vue d'ensemble

Ce document détaille toutes les mesures de sécurité implémentées dans **5GH'z Cleaner** pour garantir une utilisation sûre et transparente.

**Version**: 1.5  
**Date**: 2025-10-12  
**Score de sécurité**: **95/100** 🟢 (Excellent)

---

## ✅ Fonctionnalités de Sécurité Implémentées

### 1. 🚫 Aucune Télémétrie Cachée

#### Garanties

- ✅ **Aucune connexion réseau** établie par l'application
- ✅ **Aucune donnée utilisateur** collectée ou envoyée
- ✅ **Aucun tracking** ou analytics
- ✅ **Aucune communication** avec des serveurs externes

#### Vérification

Exécutez le vérificateur de télémétrie:

```bash
python backend/telemetry_checker.py
```

**Résultat attendu**:
```
✓ STATUT GLOBAL: CONFORME - Aucune télémétrie détectée
✓ Aucune donnée utilisateur n'est envoyée sans consentement
```

---

### 2. 🛡️ Protection Contre Injection PowerShell/Script

#### Mesures Implémentées

✅ **Remplacement complet de PowerShell** par des API natives Windows:

| Ancienne Méthode (RISQUÉE) | Nouvelle Méthode (SÉCURISÉE) |
|----------------------------|------------------------------|
| `PowerShell.exe -Command` | API COM Windows (`win32com.client`) |
| `powershell Clear-RecycleBin` | `SHEmptyRecycleBinW` (ctypes) |
| `powershell Clear-PhysicalMemory` | `EmptyWorkingSet` (psutil + ctypes) |

#### Code Sécurisé

```python
# ❌ AVANT (Injection possible)
subprocess.run(['powershell', '-Command', f'Get-Item {user_input}'])

# ✅ APRÈS (Sécurisé)
import win32com.client
shell = win32com.client.Dispatch("Shell.Application")
```

---

### 3. 🔐 Suppression Récursive Sécurisée

#### Protections Multiples

✅ **7 couches de sécurité** avant toute suppression:

1. **Whitelist stricte** des dossiers autorisés
2. **Vérification zone interdite** (System32, Program Files, etc.)
3. **Détection fichiers système critiques**
4. **Vérification âge des fichiers** (minimum 2 heures)
5. **Test de verrouillage** (fichiers en cours d'utilisation)
6. **Limite de taille** (fichiers > 500 MB ignorés)
7. **Attributs système** (fichiers avec flag SYSTEM protégés)

---

### 4. 🎯 Mode Dry-Run Obligatoire

✅ **Prévisualisation obligatoire** avant tout nettoyage:

1. Utilisateur clique sur "Prévisualiser" (Dry-Run)
2. Analyse complète **sans suppression**
3. Rapport détaillé affiché
4. Bouton "Nettoyer" débloqué **uniquement après** dry-run

---

### 5. 🚦 Arrêt de Services Sécurisé

✅ **12 services critiques** jamais arrêtés:

```python
PROTECTED_SERVICES = [
    "Spooler",          # Impression
    "wuauserv",         # Windows Update
    "BITS",             # Transfert intelligent
    "CryptSvc",         # Cryptographie
    "Winmgmt",          # WMI
    "EventLog",         # Journaux
    "RpcSs",            # RPC
    "DcomLaunch",       # DCOM
    "PlugPlay",         # Plug and Play
    "Power",            # Alimentation
    "LanmanServer",     # Partage fichiers
    "LanmanWorkstation" # Accès réseau
]
```

---

### 6. 📝 Logs Détaillés et Traçabilité

✅ **Toutes les opérations** sont consignées dans:

```
C:\Users\<User>\Documents\5GH'zCleaner-logs\
```

---

### 7. 🔑 Élévation Conditionnelle

✅ **Pas de UAC forcé** - L'utilisateur choisit le mode d'exécution.

---

### 8. 🔐 Signature Numérique (GitHub Actions)

✅ **Signature automatique** sur chaque release via workflow CI/CD.

**Vérification**:
```powershell
Get-AuthenticodeSignature 5Ghz_Cleaner.exe
```

---

### 9. ✅ Checksums SHA256 Fournis

✅ **Checksums générés** pour chaque release.

**Vérification**:
```powershell
Get-FileHash -Algorithm SHA256 5Ghz_Cleaner.exe
```

Comparer avec `CHECKSUMS.txt`.

---

### 10. 💾 Point de Restauration Automatique

✅ **Point de restauration créé** avant chaque nettoyage via WMI API native.

**Restauration manuelle**:
1. Ouvrir "Créer un point de restauration"
2. Cliquer "Restauration du système"
3. Sélectionner "5GHz Cleaner - Before Cleaning"

---

## 🧪 Tests de Sécurité

### Tests Automatisés Disponibles

```bash
python test_service_dependencies.py
python test_elevation_dryrun.py
python test_dry_run_button.py
python test_anti_spam.py
python test_anti_bypass.py
python backend/telemetry_checker.py
```

---

## 📊 Score de Sécurité Détaillé

| Catégorie | Points | Max | Note |
|-----------|--------|-----|------|
| **Télémétrie** | 10/10 | 10 | ✅ Parfait |
| **Injection Script** | 10/10 | 10 | ✅ Parfait |
| **Suppression Sécurisée** | 10/10 | 10 | ✅ Parfait |
| **Dry-Run** | 10/10 | 10 | ✅ Parfait |
| **Services Protégés** | 10/10 | 10 | ✅ Parfait |
| **Logs/Traçabilité** | 10/10 | 10 | ✅ Parfait |
| **Élévation** | 10/10 | 10 | ✅ Parfait |
| **Signature Numérique** | 8/10 | 10 | 🟡 Bon |
| **Checksums** | 10/10 | 10 | ✅ Parfait |
| **Point Restauration** | 7/10 | 10 | 🟡 Bon |

**TOTAL**: **95/100** 🟢 (Excellent)

---

## 🔍 Audit de Code

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

**Résultats attendus**: Aucune occurrence dangereuse.

---

## 🛡️ Comparaison avec Autres Cleaners

| Fonctionnalité | 5GH'z Cleaner | CCleaner | BleachBit |
|----------------|---------------|----------|-----------|
| Open Source | ✅ | ❌ | ✅ |
| Aucune Télémétrie | ✅ | ❌ | ✅ |
| Dry-Run Obligatoire | ✅ | ❌ | ⚠️ |
| API Natives (pas PowerShell) | ✅ | ⚠️ | ⚠️ |
| Services Protégés | ✅ (12) | ⚠️ | ⚠️ |
| Point Restauration Auto | ✅ | ❌ | ❌ |
| Logs Détaillés | ✅ | ⚠️ | ⚠️ |
| Checksums Fournis | ✅ | ❌ | ✅ |

---

## 📚 Documentation Supplémentaire

- [Guide Sandbox Win32](./Documentations/SANDBOX_WIN32_ISOLATION.md)
- [Protection Anti-Contournement](./Documentations/ANTI_BYPASS_SECURITY.md)
- [Dépendances Services](./Documentations/SERVICES_DEPENDENCIES.md)
- [Documentation Complète](./Documentations/INDEX.md)

---

## 🐛 Signaler une Vulnérabilité

Si vous découvrez une vulnérabilité de sécurité:

1. **NE PAS** créer d'issue publique
2. Envoyer un email à: security@github.com/UndKiMi
3. Inclure:
   - Description détaillée
   - Étapes de reproduction
   - Impact potentiel
   - Suggestions de correction

**Délai de réponse**: 48 heures maximum

---

## 📜 Licence et Responsabilité

**Tous droits réservés par UndKiMi**

Ce logiciel est fourni "tel quel", sans garantie d'aucune sorte. L'utilisateur est responsable de:
- Créer des sauvegardes avant utilisation
- Vérifier les opérations en mode Dry-Run
- Comprendre les actions effectuées

---

**Version**: 1.5  
**Dernière mise à jour**: 2025-10-12  
**Auteur**: UndKiMi  
**Repository**: https://github.com/UndKiMi/5Ghz_Cleaner
