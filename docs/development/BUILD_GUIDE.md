# 🔨 BUILD GUIDE - 5GH'z Cleaner

## 📋 Table des Matières

1. [Prérequis](#-prérequis)
2. [Build Rapide](#-build-rapide)
3. [Build Avancé](#-build-avancé)
4. [Troubleshooting](#-troubleshooting)
5. [Distribution](#-distribution)

---

## 🔧 Prérequis

### Logiciels Requis

| Logiciel | Version | Obligatoire | Notes |
|----------|---------|-------------|-------|
| **Python** | 3.11+ | ✅ Oui | Windows 64-bit |
| **PyInstaller** | 6.0+ | ✅ Oui | `pip install pyinstaller` |
| **UPX** | 4.0+ | ⚠️ Recommandé | Compression exe (optionnel) |
| **Visual Studio** | 2019+ | ⚠️ Recommandé | Build tools C++ |

### Dépendances Python

```bash
# Installer toutes les dépendances
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Ou manuellement
pip install pyinstaller==6.3.0
```

---

## 🚀 Build Rapide

### Méthode 1: Script Automatisé (Recommandé)

```powershell
# Build standard (un seul fichier .exe)
.\build.ps1

# Build propre (supprime les anciens builds)
.\build.ps1 -Clean

# Build debug (avec console)
.\build.ps1 -Debug
```

### Méthode 2: PyInstaller Direct

```powershell
# 1. Copier le template
Copy-Item 5Ghz_Cleaner.spec.template 5Ghz_Cleaner.spec

# 2. Build
pyinstaller 5Ghz_Cleaner.spec

# 3. L'exe est dans dist/5Ghz_Cleaner.exe
```

---

## 🎯 Build Avancé

### Options du Script build.ps1

| Option | Description | Exemple |
|--------|-------------|---------|
| `-Clean` | Supprime les builds précédents | `.\build.ps1 -Clean` |
| `-Debug` | Active la console (pour debug) | `.\build.ps1 -Debug` |
| `-OneDir` | Mode dossier (startup plus rapide) | `.\build.ps1 -OneDir` |
| `-NoUPX` | Désactive compression UPX | `.\build.ps1 -NoUPX` |
| `-SkipTests` | Ignore les tests pré-build | `.\build.ps1 -SkipTests` |

### Exemples Combinés

```powershell
# Build propre en mode debug
.\build.ps1 -Clean -Debug

# Build rapide sans compression
.\build.ps1 -OneDir -NoUPX

# Build de production optimisé
.\build.ps1 -Clean
```

---

## 📦 Modes de Build

### Mode One-File (Par défaut)

**Avantages:**
- ✅ Un seul fichier .exe
- ✅ Plus facile à distribuer
- ✅ Pas de dossier à gérer

**Inconvénients:**
- ❌ Démarrage plus lent (extraction temporaire)
- ❌ Fichier plus gros
- ❌ Antivirus plus suspicieux

**Utilisation:**
```powershell
.\build.ps1
# Résultat: dist/5Ghz_Cleaner.exe
```

### Mode One-Dir

**Avantages:**
- ✅ Démarrage rapide
- ✅ Fichier exe plus petit
- ✅ Moins de faux positifs antivirus

**Inconvénients:**
- ❌ Dossier avec plusieurs fichiers
- ❌ Plus complexe à distribuer

**Utilisation:**
```powershell
.\build.ps1 -OneDir
# Résultat: dist/5Ghz_Cleaner/ (dossier)
```

---

## 🔍 Configuration du .spec

### Fichiers Importants

```
5Ghz_Cleaner.spec.template  # Template de configuration
5Ghz_Cleaner.spec           # Configuration active (généré)
version_info.txt            # Informations de version Windows
```

### Personnalisation

Éditez `5Ghz_Cleaner.spec.template`:

```python
# Activer/désactiver la console
CONSOLE_ENABLED = False  # True pour debug

# Activer/désactiver UPX
UPX_ENABLED = True  # False si problèmes

# Mode de build
ONE_FILE = True  # False pour one-dir
```

### Ajouter des Fichiers

```python
datas = [
    # Ajouter vos fichiers ici
    ('mon_fichier.txt', '.'),
    ('mon_dossier/', 'mon_dossier'),
]
```

### Ajouter des Imports Cachés

```python
hiddenimports = [
    # Ajouter vos modules ici
    'mon_module',
    'mon_package.sous_module',
]
```

---

## 🐛 Troubleshooting

### Erreur: "Module not found"

**Problème:** PyInstaller ne détecte pas un module

**Solution:**
```python
# Dans 5Ghz_Cleaner.spec.template
hiddenimports = [
    'le_module_manquant',
]
```

### Erreur: "DLL not found"

**Problème:** Une DLL n'est pas incluse

**Solution:**
```python
# Dans 5Ghz_Cleaner.spec.template
binaries = [
    ('chemin/vers/ma.dll', 'dossier_destination'),
]
```

### Exe Trop Gros

**Solutions:**
1. Activer UPX: `UPX_ENABLED = True`
2. Exclure modules inutiles:
```python
excludes = [
    'matplotlib',
    'numpy',
    'pandas',
]
```
3. Utiliser mode one-dir: `.\build.ps1 -OneDir`

### Démarrage Lent

**Solutions:**
1. Utiliser mode one-dir: `.\build.ps1 -OneDir`
2. Désactiver UPX: `.\build.ps1 -NoUPX`
3. Exclure modules inutiles

### Antivirus Bloque l'Exe

**Solutions:**
1. Signer le code (certificat payant ~500€/an)
2. Utiliser mode one-dir
3. Désactiver UPX
4. Soumettre à Microsoft pour analyse

---

## 📦 Distribution

### Créer un Package de Release

```powershell
# 1. Build propre
.\build.ps1 -Clean

# 2. Tester l'exe
dist\5Ghz_Cleaner.exe

# 3. Créer l'archive
Compress-Archive -Path dist\* -DestinationPath 5Ghz_Cleaner_v1.6.0.zip

# 4. Générer checksums
Get-FileHash dist\5Ghz_Cleaner.exe -Algorithm SHA256 | Format-List
```

### Contenu du Package

```
5Ghz_Cleaner_v1.6.0.zip
├── 5Ghz_Cleaner.exe
├── README.md
├── LICENSE
├── CHECKSUMS.txt
└── CHECKSUMS_BUILD.txt
```

### Upload sur GitHub

1. **Créer une release** sur GitHub
2. **Tag:** `v1.6.0`
3. **Titre:** `5GH'z Cleaner v1.6.0 - Major Update`
4. **Fichiers:**
   - `5Ghz_Cleaner_v1.6.0.zip`
   - `CHECKSUMS_BUILD.txt`

---

## ✅ Checklist Pré-Release

### Tests

- [ ] L'exe démarre sans erreur
- [ ] Les privilèges admin sont demandés
- [ ] Toutes les fonctionnalités marchent
- [ ] Hardware monitoring fonctionne
- [ ] Dry-run fonctionne
- [ ] Nettoyage fonctionne
- [ ] Logs sont créés correctement

### Sécurité

- [ ] Signature vérifiée: `python backend/signature_manager.py --verify`
- [ ] Scan antivirus: Windows Defender
- [ ] Scan VirusTotal (optionnel)
- [ ] Test sur VM Windows 11 propre

### Documentation

- [ ] README.md à jour
- [ ] CHANGELOG.md à jour
- [ ] CHECKSUMS.txt généré
- [ ] Version dans version_info.txt correcte

---

## 📊 Métriques de Build

### Tailles Typiques

| Mode | Taille | Démarrage | Distribution |
|------|--------|-----------|--------------|
| **One-File + UPX** | ~50 MB | Lent (3-5s) | ⭐⭐⭐⭐⭐ |
| **One-File sans UPX** | ~80 MB | Lent (3-5s) | ⭐⭐⭐⭐ |
| **One-Dir + UPX** | ~60 MB | Rapide (<1s) | ⭐⭐⭐ |
| **One-Dir sans UPX** | ~90 MB | Rapide (<1s) | ⭐⭐ |

### Temps de Build

- **Clean build:** 2-5 minutes
- **Incremental:** 1-2 minutes
- **Tests:** 30 secondes

---

## 🔗 Ressources

### Documentation

- [PyInstaller Docs](https://pyinstaller.org/en/stable/)
- [UPX](https://upx.github.io/)
- [Flet Packaging](https://flet.dev/docs/guides/python/packaging-desktop-app)

### Outils

- [Resource Hacker](http://www.angusj.com/resourcehacker/) - Éditer icône/version
- [Dependency Walker](https://www.dependencywalker.com/) - Analyser DLLs
- [Process Monitor](https://docs.microsoft.com/en-us/sysinternals/downloads/procmon) - Debug runtime

---

## 🆘 Support

### Problèmes de Build

1. Consultez [Troubleshooting](#-troubleshooting)
2. Vérifiez les logs dans `build/`
3. Ouvrez une issue sur GitHub

### Contact

- **GitHub Issues:** [5Ghz_Cleaner/issues](https://github.com/UndKiMi/5Ghz_Cleaner/issues)
- **Discussions:** [5Ghz_Cleaner/discussions](https://github.com/UndKiMi/5Ghz_Cleaner/discussions)

---

**Version:** MAJOR UPDATE  
**Dernière mise à jour:** 2025-10-15  
**Auteur:** UndKiMi
