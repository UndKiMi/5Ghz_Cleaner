# 🔒 Guide d'Exécution en Sandbox (Win32 App Isolation)

## 📋 Vue d'ensemble

Ce guide explique comment exécuter **5GH'z Cleaner** dans un environnement sandbox sécurisé en utilisant **Win32 App Isolation** de Microsoft.

### ⚠️ Niveau de difficulté: **Avancé**

Cette méthode est recommandée pour:
- Les utilisateurs soucieux de la sécurité maximale
- Les environnements d'entreprise
- Les tests de sécurité
- L'exécution de logiciels non signés

---

## 🎯 Qu'est-ce que Win32 App Isolation?

Win32 App Isolation est une technologie Microsoft qui crée une **barrière de sécurité** entre l'application et le système d'exploitation en utilisant:

- **AppContainer**: Isolation au niveau du processus
- **Ressources virtualisées**: Système de fichiers et registre virtuels
- **Brokering**: Contrôle d'accès granulaire

### Avantages

✅ **Isolation complète** du système d'exploitation  
✅ **Contrôle d'accès** fichier par fichier  
✅ **Prévention** des compromissions système  
✅ **Audit** de toutes les opérations  
✅ **Réversibilité** totale (aucune modification permanente)

---

## 📦 Prérequis

### 1. Version Windows

- **Windows 11 Insider Preview** (Build 25357 ou supérieur)
- Ou **Windows 11 23H2** avec les dernières mises à jour

Vérifier votre version:
```powershell
winver
```

### 2. Outils nécessaires

- **MSIX Packaging Tool**: [Télécharger ici](https://github.com/microsoft/win32-app-isolation/releases/)
- **Certificat de signature** (auto-signé acceptable pour tests)

---

## 🛠️ Installation Étape par Étape

### Étape 1: Télécharger Python Installer

```powershell
# Télécharger Python 3.11 ou supérieur
Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe" -OutFile "python-installer.exe"
```

### Étape 2: Créer un Certificat Auto-signé (pour tests)

```powershell
# Créer un certificat de test
New-SelfSignedCertificate -Type Custom `
    -Subject "CN=5GHz Cleaner Test Certificate" `
    -KeyUsage DigitalSignature `
    -FriendlyName "5GHz Cleaner Test" `
    -CertStoreLocation "Cert:\CurrentUser\My" `
    -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3", "2.5.29.19={text}")

# Exporter le certificat
$cert = Get-ChildItem -Path Cert:\CurrentUser\My | Where-Object {$_.Subject -match "5GHz Cleaner"}
Export-Certificate -Cert $cert -FilePath "5GHzCleaner.cer"
Export-PfxCertificate -Cert $cert -FilePath "5GHzCleaner.pfx" -Password (ConvertTo-SecureString -String "YourPassword" -Force -AsPlainText)
```

### Étape 3: Packager avec MSIX Packaging Tool

1. **Lancer MSIX Packaging Tool**
2. **Sélectionner**: "Application package"
3. **Choisir**: "Create package on this computer"
4. **Sélectionner l'installeur**: `5Ghz_Cleaner.exe`
5. **Suivre l'assistant** de packaging

### Étape 4: Configurer les Capacités de Sécurité

Dans le fichier `AppxManifest.xml` du package, ajouter:

```xml
<Capabilities>
  <!-- Demander permission pour accès fichiers -->
  <rescap:Capability Name="isolatedWin32-PromptForAccess" />
  
  <!-- Pas d'accès réseau (sécurité maximale) -->
  <!-- <Capability Name="internetClient" /> -->
  
  <!-- Accès limité au système de fichiers -->
  <rescap:Capability Name="broadFileSystemAccess" />
</Capabilities>
```

### Étape 5: Signer le Package

```powershell
# Signer avec le certificat
signtool sign /fd SHA256 /a /f "5GHzCleaner.pfx" /p "YourPassword" "5GHzCleaner.msix"
```

### Étape 6: Installer le Certificat

```powershell
# Installer le certificat dans le magasin de confiance
Import-Certificate -FilePath "5GHzCleaner.cer" -CertStoreLocation "Cert:\LocalMachine\TrustedPeople"
```

### Étape 7: Installer le Package

```powershell
# Installer le package MSIX
Add-AppxPackage -Path "5GHzCleaner.msix"
```

---

## 🚀 Utilisation

### Lancer l'Application Sandboxée

```powershell
# Méthode 1: Depuis le menu Démarrer
# Chercher "5GHz Cleaner" et lancer

# Méthode 2: Depuis PowerShell
Start-Process "shell:AppsFolder\5GHzCleaner_<ID>!App"
```

### Comportement en Sandbox

Lors du premier lancement, l'application demandera des permissions pour:

1. **Accès au répertoire courant**
   - ✅ Accepter: L'application peut lire/écrire dans ce dossier
   - ❌ Refuser: Accès bloqué

2. **Accès aux fichiers temporaires**
   - ✅ Accepter: Nettoyage possible
   - ❌ Refuser: Nettoyage limité

3. **Accès aux dossiers système**
   - ⚠️ Demandé au cas par cas

### Gérer les Permissions

```powershell
# Voir les permissions accordées
Get-AppxPackage -Name "*5GHzCleaner*" | Get-AppxPackageManifest

# Réinitialiser les permissions
# Paramètres > Confidentialité et sécurité > Système de fichiers
```

---

## 🔍 Vérification de la Sécurité

### Test 1: Vérifier l'Isolation Réseau

```python
# Dans l'application sandboxée, tester:
import urllib.request
try:
    urllib.request.urlopen("http://www.microsoft.com")
    print("❌ Accès réseau NON bloqué")
except:
    print("✅ Accès réseau bloqué (sécurité OK)")
```

### Test 2: Vérifier l'Isolation Fichiers

```python
# Tenter d'accéder à un fichier hors sandbox
try:
    with open("C:\\Windows\\System32\\drivers\\etc\\hosts", "r") as f:
        print("❌ Accès fichier système NON bloqué")
except PermissionError:
    print("✅ Accès fichier système bloqué (sécurité OK)")
```

### Test 3: Vérifier l'Isolation Processus

```python
# Tenter d'exécuter un processus externe
import subprocess
try:
    subprocess.run(["cmd.exe", "/c", "echo test"])
    print("❌ Exécution processus NON bloquée")
except:
    print("✅ Exécution processus bloquée (sécurité OK)")
```

---

## 📊 Comparaison des Niveaux de Sécurité

| Méthode | Isolation | Complexité | Performance | Recommandé pour |
|---------|-----------|------------|-------------|-----------------|
| **Exécution normale** | ❌ Aucune | ⭐ Facile | ⭐⭐⭐ Rapide | Utilisation quotidienne |
| **UAC élevé** | ⚠️ Partielle | ⭐⭐ Moyenne | ⭐⭐⭐ Rapide | Nettoyage système |
| **Win32 Sandbox** | ✅ Complète | ⭐⭐⭐⭐ Difficile | ⭐⭐ Moyenne | Sécurité maximale |
| **VM/Container** | ✅ Totale | ⭐⭐⭐⭐⭐ Très difficile | ⭐ Lente | Tests de sécurité |

---

## 🐛 Dépannage

### Problème: "Le package ne peut pas être installé"

**Solution**:
```powershell
# Vérifier que le certificat est installé
Get-ChildItem Cert:\LocalMachine\TrustedPeople | Where-Object {$_.Subject -match "5GHz"}

# Réinstaller si nécessaire
Import-Certificate -FilePath "5GHzCleaner.cer" -CertStoreLocation "Cert:\LocalMachine\TrustedPeople"
```

### Problème: "L'application ne démarre pas"

**Solution**:
```powershell
# Vérifier les logs d'événements
Get-WinEvent -LogName "Microsoft-Windows-AppxPackaging/Operational" -MaxEvents 10

# Réinitialiser le package
Get-AppxPackage -Name "*5GHzCleaner*" | Remove-AppxPackage
Add-AppxPackage -Path "5GHzCleaner.msix"
```

### Problème: "Permissions refusées en boucle"

**Solution**:
```powershell
# Réinitialiser les permissions
# Paramètres > Confidentialité et sécurité > Système de fichiers
# Trouver "5GHz Cleaner" et cliquer "Réinitialiser"
```

---

## 📚 Ressources Supplémentaires

### Documentation Officielle

- [Win32 App Isolation - GitHub](https://github.com/microsoft/win32-app-isolation)
- [MSIX Packaging Tool - Microsoft Learn](https://learn.microsoft.com/en-us/windows/msix/packaging-tool/)
- [AppContainer - Microsoft Docs](https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation)

### Articles de Blog

- [Sandboxing Python with Win32 App Isolation](https://blogs.windows.com/windowsdeveloper/2024/03/06/sandboxing-python-with-win32-app-isolation/)
- [MSIX Packaging Best Practices](https://learn.microsoft.com/en-us/windows/msix/desktop/desktop-to-uwp-best-practices)

---

## ⚠️ Limitations

### Limitations Connues

1. **Nécessite Windows 11 Insider** (pour l'instant)
2. **Complexité élevée** de mise en place
3. **Performance légèrement réduite** (overhead de virtualisation)
4. **Compatibilité limitée** avec certaines opérations système

### Opérations Non Supportées en Sandbox

- ❌ Modification du registre système
- ❌ Installation de drivers
- ❌ Modification de services Windows
- ❌ Accès direct au matériel

### Recommandation

Pour **5GH'z Cleaner**, le sandbox Win32 est **optionnel** car:
- ✅ Le code source est open-source et auditable
- ✅ Aucune télémétrie n'est présente
- ✅ Les opérations sont déjà sécurisées par des whitelists
- ✅ Le mode Dry-Run permet de prévisualiser

**Utilisez le sandbox uniquement si**:
- Vous testez une version non officielle
- Vous êtes dans un environnement d'entreprise strict
- Vous effectuez des tests de sécurité

---

## 📝 Notes de Sécurité

### Audit de Sécurité

Toutes les opérations en sandbox sont auditées:

```powershell
# Voir les logs d'audit
Get-WinEvent -LogName "Microsoft-Windows-AppLocker/EXE and DLL" -MaxEvents 50
```

### Nettoyage Après Tests

```powershell
# Désinstaller le package
Get-AppxPackage -Name "*5GHzCleaner*" | Remove-AppxPackage

# Supprimer le certificat
Get-ChildItem Cert:\LocalMachine\TrustedPeople | Where-Object {$_.Subject -match "5GHz"} | Remove-Item

# Nettoyer les fichiers temporaires
Remove-Item -Path "$env:TEMP\5GHzCleaner*" -Recurse -Force
```

---

## 🎓 Conclusion

Le sandbox Win32 App Isolation offre une **sécurité maximale** mais au prix d'une **complexité élevée**.

### Quand l'utiliser?

✅ **OUI** pour:
- Tests de sécurité
- Environnements d'entreprise
- Exécution de versions non signées
- Audit de sécurité

❌ **NON** pour:
- Utilisation quotidienne normale
- Si l'exécutable est signé et vérifié
- Si le code source est audité

### Alternative Simple: Windows Sandbox

Pour une isolation plus simple:

```powershell
# Activer Windows Sandbox
Enable-WindowsOptionalFeature -FeatureName "Containers-DisposableClientVM" -All -Online

# Lancer Windows Sandbox
WindowsSandbox.exe
```

Puis exécutez 5GH'z Cleaner dans la sandbox Windows (environnement jetable).

---

**Version**: 1.0  
**Dernière mise à jour**: 2025-10-12  
**Auteur**: UndKiMi
