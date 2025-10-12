# 🚀 Démarrage Rapide - 5GH'z Cleaner

Guide ultra-rapide pour commencer à utiliser 5GH'z Cleaner en 5 minutes.

---

## ⚡ Installation Express (2 minutes)

### Option 1: Exécutable Précompilé (Recommandé)

```powershell
# 1. Télécharger la dernière release
# https://github.com/UndKiMi/5Ghz_Cleaner/releases

# 2. Vérifier les checksums (optionnel mais recommandé)
Get-FileHash "5Ghz_Cleaner.exe" -Algorithm SHA256

# 3. Lancer l'application
.\5Ghz_Cleaner.exe
```

### Option 2: Depuis les Sources

```bash
# 1. Cloner le repository
git clone https://github.com/UndKiMi/5Ghz_Cleaner.git
cd 5Ghz_Cleaner

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
python main.py
```

---

## 🎯 Première Utilisation (3 minutes)

### Étape 1: Lancer l'Application

```bash
python main.py
# ou
.\5Ghz_Cleaner.exe
```

### Étape 2: Dry-Run OBLIGATOIRE

1. **Sélectionner** les options de nettoyage
2. **Cliquer** sur "🔍 Dry-Run" (OBLIGATOIRE)
3. **Vérifier** la prévisualisation
4. **Valider** les fichiers à supprimer

### Étape 3: Nettoyage

1. **Cliquer** sur "🧹 Nettoyer"
2. **Confirmer** l'action
3. **Attendre** la fin du nettoyage
4. **Vérifier** les logs

---

## 📋 Checklist Rapide

### Avant le Premier Nettoyage

- [ ] ✅ **Point de restauration créé** (automatique)
- [ ] ✅ **Dry-run exécuté** (obligatoire)
- [ ] ✅ **Prévisualisation vérifiée**
- [ ] ✅ **Sauvegarde importante faite** (recommandé)

### Pendant le Nettoyage

- [ ] ✅ **Ne pas fermer l'application**
- [ ] ✅ **Ne pas éteindre l'ordinateur**
- [ ] ✅ **Attendre la fin complète**

### Après le Nettoyage

- [ ] ✅ **Vérifier les logs** (`Documents/5GH'zCleaner-logs/`)
- [ ] ✅ **Redémarrer si nécessaire**
- [ ] ✅ **Vérifier que tout fonctionne**

---

## 🔒 Sécurité en 30 Secondes

### Ce qui est PROTÉGÉ (Impossible à supprimer)

- ❌ **Fichiers système Windows** (226 chemins protégés)
- ❌ **Applications Microsoft** (Office, Edge, OneDrive, Teams)
- ❌ **Navigateurs** (Chrome, Firefox, Brave)
- ❌ **Antivirus** (7 marques protégées)
- ❌ **Drivers GPU** (NVIDIA, AMD, Intel)

### Ce qui est AUTORISÉ

- ✅ **Fichiers temporaires** (`%TEMP%`)
- ✅ **Cache navigateurs** (si sélectionné)
- ✅ **Corbeille** (avec confirmation)
- ✅ **Windows.old** (avec confirmation)

---

## 🧪 Tester la Sécurité (1 minute)

```bash
# Test complet de sécurité
python tests/test_all_security.py

# Résultat attendu: 7/7 tests réussis ✅
```

---

## 📊 Monitoring Matériel

### Onglet Configuration

1. **Cliquer** sur l'onglet "⚙️ Configuration"
2. **Voir** CPU, RAM, GPU, Disques en temps réel
3. **Code couleur**:
   - 🟢 Vert: Normal
   - 🟡 Jaune: Attention
   - 🔴 Rouge: Critique

---

## 🆘 Problèmes Courants

### "Windows a protégé votre PC"

**Cause:** Certificat auto-signé (pas officiel)

**Solution:**
```
1. Cliquer "Plus d'infos"
2. Cliquer "Exécuter quand même"
```

**Note:** C'est normal avec un certificat auto-signé. Pour éviter cela en production, un certificat officiel est nécessaire (500€/an).

### "Accès refusé"

**Cause:** Droits administrateur requis pour certaines opérations

**Solution:**
```powershell
# Lancer en tant qu'administrateur
Right-click > "Exécuter en tant qu'administrateur"
```

### "Module non trouvé"

**Cause:** Dépendances manquantes

**Solution:**
```bash
pip install -r requirements.txt
```

---

## 📚 Documentation Complète

| Document | Utilité | Temps de lecture |
|----------|---------|------------------|
| **README.md** | Vue d'ensemble | 10 min |
| **SECURITY.md** | Sécurité détaillée | 15 min |
| **INSTALLATION.md** | Installation complète | 5 min |
| **CONTRIBUTING.md** | Contribuer | 10 min |

---

## 🎯 Commandes Utiles

### Vérifier l'Intégrité

```bash
# Vérifier les checksums
python scripts/verify_checksum.py

# Vérifier l'absence de télémétrie
python backend/telemetry_checker.py
```

### Tests

```bash
# Tests de sécurité (7 tests)
python tests/test_all_security.py

# Tests unitaires (31 tests)
python tests/test_coverage_complete.py

# Tous les tests
python tests/run_all_tests.py
```

### Build

```bash
# Compiler l'exécutable
flet pack main.py --name "5Ghz_Cleaner"

# Signer (certificat auto-signé)
.\scripts\sign_executable.ps1 -FilePath "dist\5Ghz_Cleaner.exe"

# Générer les checksums
python scripts/generate_checksum.py
```

---

## 💡 Conseils Pro

### 1. Toujours Faire un Dry-Run

```
❌ JAMAIS nettoyer sans dry-run
✅ TOUJOURS vérifier la prévisualisation
```

### 2. Vérifier les Logs

```
Emplacement: Documents/5GH'zCleaner-logs/
Format: cleaner_YYYYMMDD_HHMMSS.log
```

### 3. Point de Restauration

```
✅ Créé automatiquement avant chaque nettoyage
✅ Permet de revenir en arrière si problème
✅ Vérification espace disque (1 GB minimum)
```

---

## 🔗 Liens Rapides

- **GitHub**: https://github.com/UndKiMi/5Ghz_Cleaner
- **Issues**: https://github.com/UndKiMi/5Ghz_Cleaner/issues
- **Releases**: https://github.com/UndKiMi/5Ghz_Cleaner/releases
- **Documentation**: [Documentations/INDEX.md](Documentations/INDEX.md)

---

## ⏱️ Résumé 1 Minute

```bash
# 1. Installer
pip install -r requirements.txt

# 2. Lancer
python main.py

# 3. Dry-Run (OBLIGATOIRE)
Cliquer "🔍 Dry-Run"

# 4. Vérifier
Vérifier la prévisualisation

# 5. Nettoyer
Cliquer "🧹 Nettoyer"

# 6. Confirmer
Confirmer l'action

# ✅ Terminé!
```

---

**Temps total:** ~5 minutes  
**Difficulté:** Facile  
**Prérequis:** Python 3.8+ (ou exécutable précompilé)

**Besoin d'aide?** Consultez [README.md](README.md) ou ouvrez une [issue](https://github.com/UndKiMi/5Ghz_Cleaner/issues).

---

**Auteur**: UndKiMi  
**Version**: MAJOR UPDATE  
