# 📜 Scripts - 5GH'z Cleaner

Ce dossier contient les scripts utilitaires pour la signature de code et la génération de checksums.

## 📋 Scripts Disponibles

### 🔐 Certificat Code Signing

#### `create_self_signed_cert.ps1`
Crée un certificat auto-signé pour le développement.

**Usage:**
```powershell
.\create_self_signed_cert.ps1
```

**Ce script:**
- ✅ Crée un certificat auto-signé valide 5 ans
- ✅ Exporte le certificat (.cer) et la clé privée (.pfx)
- ✅ Installe automatiquement dans Trusted Root
- ✅ Génère un mot de passe: `5GHzCleaner2024!`

**Fichiers créés:**
- `cert/5GHz_Cleaner_Dev.cer` - Certificat public
- `cert/5GHz_Cleaner_Dev.pfx` - Certificat avec clé privée

#### `sign_executable.ps1`
Signe un exécutable avec le certificat auto-signé.

**Usage:**
```powershell
.\sign_executable.ps1 -FilePath "dist\5Ghz_Cleaner.exe"
```

**Options:**
- `-FilePath` (requis) - Chemin de l'exécutable à signer
- `-CertPath` (optionnel) - Chemin du certificat (.pfx)
- `-Password` (optionnel) - Mot de passe du certificat

**Ce script:**
- ✅ Signe l'exécutable avec le certificat
- ✅ Ajoute un timestamp (DigiCert)
- ✅ Utilise SHA256 pour la signature
- ✅ Vérifie la signature après

### 📊 Checksums

#### `generate_checksum.py`
Génère les checksums SHA256 et SHA512 des fichiers de distribution.

**Usage:**
```bash
python generate_checksum.py
```

**Ce script:**
- ✅ Calcule SHA256 et SHA512 pour tous les .exe dans dist/
- ✅ Génère `CHECKSUMS.txt` lisible
- ✅ Génère `checksums.json` pour vérification automatique

## 🎯 Workflow Complet

### 1. Créer le Certificat (Une fois)
```powershell
# Exécuter en tant qu'administrateur
.\create_self_signed_cert.ps1
```

### 2. Compiler l'Application
```bash
# Compiler avec PyInstaller ou Flet
flet pack main.py --name "5Ghz_Cleaner"
```

### 3. Signer l'Exécutable
```powershell
.\sign_executable.ps1 -FilePath "dist\5Ghz_Cleaner.exe"
```

### 4. Générer les Checksums
```bash
python generate_checksum.py
```

### 5. Vérifier la Signature
```powershell
# Vérifier la signature
Get-AuthenticodeSignature "dist\5Ghz_Cleaner.exe"

# Afficher les détails
Get-AuthenticodeSignature "dist\5Ghz_Cleaner.exe" | Format-List *
```

## ⚠️ Important

### Certificat Auto-Signé
- ❌ **Windows SmartScreen affichera toujours un avertissement**
- ❌ **Pas de confiance automatique**
- ✅ **Bon pour le développement et les tests**
- ❌ **Pas adapté pour la distribution publique**

### Pour la Production
Pour éviter les avertissements SmartScreen, vous devez obtenir un **certificat code signing officiel**:

- **Certificat OV**: 200€/an (Sectigo, DigiCert)
- **Certificat EV**: 500€/an (recommandé pour réputation immédiate)

Voir [`Documentations/CODE_SIGNING_GUIDE.md`](../Documentations/CODE_SIGNING_GUIDE.md) pour le guide complet.

## 🔒 Sécurité

### Bonnes Pratiques

1. **Ne jamais commiter le certificat sur Git**
   ```bash
   # Déjà dans .gitignore
   cert/
   *.pfx
   *.p12
   ```

2. **Protéger la clé privée**
   - ✅ Stocker dans un coffre-fort de mots de passe
   - ✅ Sauvegarder dans un endroit sûr
   - ❌ Ne jamais partager

3. **Vérifier avant de signer**
   - ✅ Scanner l'exécutable avec un antivirus
   - ✅ Vérifier que c'est la bonne version
   - ✅ Tester l'exécutable avant signature

## 📚 Documentation

- **Guide complet**: [`Documentations/CODE_SIGNING_GUIDE.md`](../Documentations/CODE_SIGNING_GUIDE.md)
- **Sécurité**: [`SECURITY.md`](../SECURITY.md)
- **README principal**: [`README.md`](../README.md)

## 🆘 Dépannage

### Erreur: "signtool.exe non trouvé"
**Solution**: Installer le Windows SDK
- Télécharger: https://developer.microsoft.com/windows/downloads/windows-sdk/
- Ou utiliser Set-AuthenticodeSignature (automatique dans le script)

### Erreur: "Certificat non trouvé"
**Solution**: Exécuter d'abord `create_self_signed_cert.ps1`

### Erreur: "Accès refusé"
**Solution**: Exécuter PowerShell en tant qu'administrateur

### SmartScreen bloque toujours
**C'est normal** avec un certificat auto-signé. Solutions:
1. **Développement**: Installer le certificat sur chaque machine de test
2. **Production**: Obtenir un certificat officiel (500€/an)

## 📞 Support

Pour toute question:
- **Documentation**: [`Documentations/`](../Documentations/)
- **Issues**: [GitHub Issues](https://github.com/UndKiMi/5Ghz_Cleaner/issues)

---

**Auteur**: UndKiMi  
**Version**: MAJOR UPDATE
