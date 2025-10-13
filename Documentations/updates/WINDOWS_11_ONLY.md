# ⚠️ Windows 11 Uniquement - Compatibilité

## 🎯 Compatibilité Système

**5GH'z Cleaner** est conçu **exclusivement pour Windows 11 (64-bit)**.

### ✅ Compatible
- **Windows 11** (Build 22000 ou supérieur)
- Architecture 64-bit uniquement

### ❌ Non Compatible
- **Windows 10** - Non supporté
- **Windows 8/8.1** - Non supporté
- **Windows 7** - Non supporté
- Architecture 32-bit - Non supportée

---

## 🔍 Raisons Techniques

### APIs Spécifiques à Windows 11

Le logiciel utilise des fonctionnalités et APIs qui sont exclusives à Windows 11:

1. **APIs Système Modernes**
   - Nouvelles APIs de gestion de la mémoire
   - APIs de sécurité améliorées
   - Nouvelles structures de fichiers système

2. **Architecture Système**
   - Structure de dossiers Windows 11
   - Nouveaux emplacements de cache
   - Services système spécifiques à Windows 11

3. **Sécurité Renforcée**
   - Nouvelles protections système
   - APIs de vérification de signature
   - Mécanismes de sécurité Windows 11

4. **Optimisations**
   - Gestion mémoire Windows 11
   - Optimisations CPU spécifiques
   - Nouvelles APIs de monitoring matériel

---

## 🚨 Vérification au Démarrage

Le logiciel vérifie automatiquement la version de Windows au démarrage:

```python
# Vérification Windows 11 (Build 22000+)
if not check_windows_11():
    print("ERROR: Windows 11 Required")
    print("This application requires Windows 11 (Build 22000+)")
    sys.exit(1)
```

### Message d'Erreur

Si vous essayez d'exécuter sur Windows 10 ou antérieur:

```
============================================================
ERROR: Windows 11 Required
============================================================

This application requires Windows 11 (Build 22000+)
It is not compatible with Windows 10 or earlier versions.

Please upgrade to Windows 11 to use this software.

Press Enter to exit...
```

---

## 📋 Vérifier Votre Version de Windows

### Méthode 1: Paramètres Windows

1. Ouvrir **Paramètres** (Win + I)
2. Aller dans **Système** > **Informations système**
3. Vérifier la **Version de Windows**

### Méthode 2: Commande PowerShell

```powershell
# Afficher la version de Windows
[System.Environment]::OSVersion.Version

# Résultat attendu pour Windows 11:
# Major  Minor  Build  Revision
# -----  -----  -----  --------
# 10     0      22000  (ou supérieur)
```

### Méthode 3: winver

```
1. Appuyer sur Win + R
2. Taper: winver
3. Appuyer sur Entrée
4. Vérifier "Version 22H2" ou supérieure
```

---

## 🔄 Mise à Niveau vers Windows 11

### Prérequis Matériels

Pour installer Windows 11, votre PC doit avoir:

- **Processeur**: 1 GHz ou plus, 2 cœurs minimum, 64-bit
- **RAM**: 4 GB minimum
- **Stockage**: 64 GB minimum
- **TPM**: Version 2.0
- **Secure Boot**: Compatible UEFI
- **Carte graphique**: Compatible DirectX 12

### Vérifier la Compatibilité

Microsoft propose un outil de vérification:
- **PC Health Check**: https://aka.ms/GetPCHealthCheckApp

### Mise à Niveau

1. **Windows Update**
   - Paramètres > Windows Update
   - Vérifier les mises à jour
   - Installer Windows 11 si disponible

2. **Assistant d'Installation**
   - Télécharger: https://www.microsoft.com/software-download/windows11
   - Exécuter l'assistant
   - Suivre les instructions

---

## 🛠️ Alternatives pour Windows 10

Si vous ne pouvez pas mettre à niveau vers Windows 11, voici des alternatives:

### Logiciels Similaires (Windows 10 Compatible)

1. **CCleaner** - https://www.ccleaner.com/
2. **BleachBit** - https://www.bleachbit.org/
3. **Glary Utilities** - https://www.glarysoft.com/
4. **Wise Disk Cleaner** - https://www.wisecleaner.com/

> **Note**: Ces logiciels ne sont pas développés par nous et ont leurs propres politiques de confidentialité.

---

## 📊 Statistiques de Compatibilité

### Versions Windows Supportées

| Version | Support | Raison |
|---------|---------|--------|
| **Windows 11** | ✅ Oui | Conçu pour Windows 11 |
| **Windows 10** | ❌ Non | APIs incompatibles |
| **Windows 8.1** | ❌ Non | Trop ancien |
| **Windows 7** | ❌ Non | Fin de support Microsoft |

### Builds Windows 11

| Build | Version | Support |
|-------|---------|---------|
| **22000+** | 21H2 et supérieur | ✅ Oui |
| **< 22000** | Windows 10 | ❌ Non |

---

## 🔒 Sécurité et Compatibilité

### Pourquoi Windows 11 Uniquement?

1. **Sécurité Maximale**
   - Windows 11 a des protections système renforcées
   - Nouvelles APIs de sécurité
   - Meilleure isolation des processus

2. **Fiabilité**
   - APIs stables et modernes
   - Meilleur support des fonctionnalités
   - Moins de bugs et d'incompatibilités

3. **Performance**
   - Optimisations Windows 11
   - Meilleure gestion de la mémoire
   - APIs plus rapides

4. **Maintenance**
   - Code plus simple et maintenable
   - Moins de cas particuliers
   - Support plus facile

---

## ❓ Questions Fréquentes

### Q: Pourquoi pas Windows 10?

**R**: Windows 10 et Windows 11 ont des différences significatives dans leurs APIs système, leur structure de fichiers, et leurs mécanismes de sécurité. Supporter Windows 10 nécessiterait de maintenir deux versions différentes du code, ce qui augmenterait les risques de bugs et compliquerait la maintenance.

### Q: Puis-je forcer l'exécution sur Windows 10?

**R**: Non, et nous le déconseillons fortement. Le logiciel:
- Pourrait ne pas fonctionner correctement
- Pourrait causer des erreurs système
- N'a pas été testé sur Windows 10
- Pourrait endommager votre système

### Q: Y aura-t-il une version Windows 10?

**R**: Non, il n'est pas prévu de développer une version compatible Windows 10. Le logiciel est conçu spécifiquement pour Windows 11 et utilise des fonctionnalités qui n'existent pas sur Windows 10.

### Q: Mon PC n'est pas compatible Windows 11, que faire?

**R**: Vous avez plusieurs options:
1. Utiliser un logiciel alternatif compatible Windows 10
2. Mettre à niveau votre matériel
3. Acheter un nouveau PC compatible Windows 11

---

## 📞 Support

### Problèmes de Compatibilité

Si vous rencontrez des problèmes de compatibilité sur Windows 11:

1. **Vérifier votre version**
   ```powershell
   [System.Environment]::OSVersion.Version
   ```

2. **Mettre à jour Windows 11**
   - Paramètres > Windows Update
   - Installer toutes les mises à jour

3. **Ouvrir une Issue**
   - GitHub: https://github.com/UndKiMi/5Ghz_Cleaner/issues
   - Inclure votre version de Windows (Build)
   - Décrire le problème rencontré

---

## 📝 Résumé

### ✅ À Retenir

- **Windows 11 uniquement** - Build 22000 ou supérieur
- **Vérification automatique** au démarrage
- **Pas de support Windows 10** - Raisons techniques
- **Alternatives disponibles** pour Windows 10

### 🎯 Recommandation

Pour une expérience optimale et sécurisée:
1. ✅ Utiliser Windows 11 (Build 22000+)
2. ✅ Maintenir Windows à jour
3. ✅ Vérifier la compatibilité avant installation

---

**Version**: MAJOR UPDATE  
**Auteur**: UndKiMi  
**Licence**: CC BY-NC-SA 4.0  
**Repository**: https://github.com/UndKiMi/5Ghz_Cleaner

**COMPATIBILITÉ: WINDOWS 11 (64-BIT) UNIQUEMENT**
