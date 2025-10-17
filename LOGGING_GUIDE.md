# 📝 Guide du Système de Logging

**5GH'z Cleaner** - Système de logging professionnel

---

## 🎯 Vue d'ensemble

Le projet utilise un système de logging avancé avec:
- ✅ **Rotation automatique** des logs (10 MB max, 5 fichiers)
- ✅ **Console colorée** (si colorama installé)
- ✅ **Stacktraces détaillés** avec contexte complet
- ✅ **Mode debug** verbeux
- ✅ **Format différent** console/fichier
- ✅ **Pas de pollution** console en production

---

## 🚀 Utilisation

### Import du logger

```python
from backend.advanced_logger import logger

# Ou utiliser les fonctions raccourcies
from backend.advanced_logger import log_info, log_error, log_exception
```

### Niveaux de log

```python
# INFO - Informations générales
logger.info("Application démarrée")

# DEBUG - Détails techniques (seulement si DEBUG=true)
logger.debug(f"Variable x = {x}, état = {state}")

# WARNING - Avertissements
logger.warning("Espace disque faible: 5 GB restants")

# ERROR - Erreurs (sans stacktrace)
logger.error("Impossible de lire le fichier config.json")

# ERROR avec stacktrace
logger.error("Erreur lors du nettoyage", exc_info=True)

# EXCEPTION - Dans un bloc except (stacktrace automatique)
try:
    result = operation_risquee()
except Exception as e:
    logger.exception("Opération risquée a échoué")

# SUCCESS - Succès d'opération
logger.success("Nettoyage terminé: 500 MB libérés")

# SECURITY - Événements de sécurité
logger.security("Tentative d'accès à un fichier système bloquée")
```

---

## ⚙️ Configuration

### Variables d'environnement

Créer un fichier `.env` à la racine du projet:

```bash
# Mode debug (affiche tous les logs dans la console)
DEBUG=false

# Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO
```

### Activer le mode debug

```bash
# Windows
set DEBUG=true
python main.py

# Ou dans .env
DEBUG=true
```

**En mode debug**:
- ✅ Tous les logs s'affichent dans la console
- ✅ Messages très détaillés
- ✅ Contexte complet des erreurs
- ✅ Couleurs activées (si colorama installé)

**En mode production** (DEBUG=false):
- ✅ Console sobre et épurée
- ✅ Seulement WARNING, ERROR, CRITICAL dans la console
- ✅ Tous les logs dans le fichier
- ✅ Pas de pollution

---

## 📂 Emplacement des logs

### Répertoire

```
C:\Users\[USERNAME]\Documents\5GH'zCleaner-logs\
```

### Fichiers

```
5ghz_cleaner.log        # Fichier actif
5ghz_cleaner.log.1      # Backup 1
5ghz_cleaner.log.2      # Backup 2
5ghz_cleaner.log.3      # Backup 3
5ghz_cleaner.log.4      # Backup 4
5ghz_cleaner.log.5      # Backup 5
```

**Rotation automatique**: Quand un fichier atteint 10 MB, il est renommé et un nouveau fichier est créé.

---

## 📊 Exemples de logs

### Console (mode production)

```
[14:23:45] WARNING  │ cleaner         │ Espace disque faible: 5 GB restants
[14:23:50] ERROR    │ disk_optimizer  │ Impossible d'optimiser le disque C:
```

### Console (mode debug avec couleurs)

```
[14:23:45] DEBUG    │ main            │ Initialisation de l'application
[14:23:45] INFO     │ main            │ Windows 11 détecté (Build 22000)
[14:23:46] WARNING  │ cleaner         │ Espace disque faible: 5 GB restants
[14:23:50] ERROR    │ disk_optimizer  │ Impossible d'optimiser le disque C:
```

### Fichier de log (détaillé)

```
2025-10-17 14:23:45,123 | INFO     | main.check_windows_11:78 | Windows 11 détecté (Build 22000)
2025-10-17 14:23:46,456 | WARNING  | cleaner.scan_disk:234 | Espace disque faible: 5 GB restants
2025-10-17 14:23:50,789 | ERROR    | disk_optimizer.optimize:156 | Impossible d'optimiser le disque C:
====================================================================================================
Traceback (most recent call last):
  File "backend\disk_optimizer.py", line 154, in optimize
    result = subprocess.run(['defrag', 'C:', '/O'], check=True)
  File "subprocess.py", line 528, in run
    raise CalledProcessError(retcode, process.args, output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '['defrag', 'C:', '/O']' returned non-zero exit status 1.
====================================================================================================
```

---

## 🔍 Diagnostic d'erreurs

### En cas de problème

1. **Activer le mode debug**
   ```bash
   set DEBUG=true
   python main.py
   ```

2. **Reproduire l'erreur**
   - L'erreur s'affichera dans la console avec tous les détails

3. **Consulter les logs**
   ```
   C:\Users\[USERNAME]\Documents\5GH'zCleaner-logs\5ghz_cleaner.log
   ```

4. **Informations à fournir** (pour une issue GitHub):
   - Message d'erreur complet
   - Stacktrace (si disponible)
   - Contexte (que faisiez-vous?)
   - Extrait du fichier de log

### Exemple d'erreur complète

```
[14:23:50] ERROR    │ disk_optimizer  │ Impossible d'optimiser le disque C:
====================================================================================================
Traceback (most recent call last):
  File "backend\disk_optimizer.py", line 154, in optimize
    result = subprocess.run(['defrag', 'C:', '/O'], check=True)
subprocess.CalledProcessError: Command '['defrag', 'C:', '/O']' returned non-zero exit status 1.

Context:
- Drive: C:
- Type: SSD
- Free space: 5.2 GB
====================================================================================================
```

---

## 💡 Bonnes pratiques

### Pour les développeurs

```python
# ✅ BON - Log avec contexte
logger.info(f"Nettoyage démarré: {file_count} fichiers à traiter")

# ✅ BON - Exception avec logger.exception()
try:
    clean_files()
except Exception as e:
    logger.exception("Erreur lors du nettoyage")
    # Le stacktrace est automatiquement inclus

# ✅ BON - Debug avec détails
logger.debug(f"État: files={files}, size={size}, mode={mode}")

# ❌ MAUVAIS - print() au lieu du logger
print("[ERROR] Erreur")  # Ne va pas dans les logs

# ❌ MAUVAIS - Pas de contexte
logger.error("Erreur")  # Trop vague

# ❌ MAUVAIS - Exception sans stacktrace
try:
    operation()
except Exception as e:
    logger.error(str(e))  # Perd le stacktrace
```

### Uniformisation

**Remplacer tous les `print()` par le logger**:

```python
# AVANT
print("[INFO] Application lancée")
print("[ERROR] Erreur")

# APRÈS
logger.info("Application lancée")
logger.error("Erreur", exc_info=True)
```

---

## 🎨 Installation de colorama (optionnel)

Pour avoir des couleurs dans la console:

```bash
pip install colorama
```

**Avec colorama**:
- ✅ Console colorée (vert, jaune, rouge selon le niveau)
- ✅ Meilleure lisibilité
- ✅ Distinction visuelle immédiate

**Sans colorama**:
- ✅ Fonctionne quand même
- ⚠️ Pas de couleurs (texte brut)

---

## 📋 Checklist de migration

Pour migrer vers le nouveau système de logging:

- [ ] Installer colorama: `pip install colorama`
- [ ] Créer `.env` avec `DEBUG=false`
- [ ] Remplacer les imports:
  ```python
  # AVANT
  from backend.production_logger import logger
  
  # APRÈS
  from backend.advanced_logger import logger
  ```
- [ ] Remplacer tous les `print()` par `logger.info()` ou équivalent
- [ ] Utiliser `logger.exception()` dans les blocs `except`
- [ ] Tester en mode debug: `set DEBUG=true`
- [ ] Vérifier les logs dans `Documents/5GH'zCleaner-logs/`

---

## ✅ Avantages

### Pour l'utilisateur

- ✅ Console propre et non polluée
- ✅ Erreurs claires et compréhensibles
- ✅ Facile de fournir des logs pour le support

### Pour le développeur

- ✅ Diagnostic rapide des erreurs
- ✅ Stacktraces complets avec contexte
- ✅ Mode debug très verbeux
- ✅ Logs rotatifs (pas de saturation disque)
- ✅ Format structuré et professionnel

### Pour le support

- ✅ Logs détaillés disponibles
- ✅ Contexte complet des erreurs
- ✅ Facile à analyser
- ✅ Horodatage précis

---

## 🔗 Liens utiles

- **Dépôt GitHub**: [5GH'z Cleaner](https://github.com/UndKiMi/5Ghz_Cleaner)
- **Issues**: [Signaler un bug](https://github.com/UndKiMi/5Ghz_Cleaner/issues)
- **Documentation Python logging**: [docs.python.org](https://docs.python.org/3/library/logging.html)

---

**5GH'z Cleaner** - Système de logging professionnel pour un diagnostic optimal.
