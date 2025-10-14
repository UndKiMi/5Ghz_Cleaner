# LibreHardwareMonitor - Installation

Pour activer le monitoring des températures (CPU AMD, GPU AMD/NVIDIA, Disques), vous devez télécharger LibreHardwareMonitor.

## 📥 Téléchargement

1. **Téléchargez LibreHardwareMonitor** depuis GitHub :
   - URL : https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases
   - Téléchargez la dernière version (fichier `.zip`)

2. **Extrayez le fichier ZIP**

3. **Copiez le fichier DLL** :
   - Trouvez le fichier `LibreHardwareMonitorLib.dll` dans le dossier extrait
   - Copiez-le dans ce dossier (`libs/`)

## 📂 Structure Attendue

```
5Ghz_Cleaner/
├── libs/
│   ├── LibreHardwareMonitorLib.dll  ← Placez le fichier ici
│   └── README_LIBREHARDWAREMONITOR.md (ce fichier)
```

## ✅ Vérification

Une fois le fichier copié, relancez l'application. Vous devriez voir dans la console :

```
[SUCCESS] LibreHardwareMonitor initialized successfully
```

Si vous voyez ce message, les températures s'afficheront correctement !

## ⚠️ Si Vous Ne Téléchargez Pas la DLL

L'application fonctionnera quand même, mais :
- Les températures afficheront "N/A"
- L'utilisation GPU AMD ne sera pas disponible
- Le monitoring sera limité aux méthodes natives Windows

## 🔒 Sécurité

LibreHardwareMonitor est :
- ✅ Open-source (code vérifié publiquement)
- ✅ Gratuit
- ✅ Sans télémétrie
- ✅ Utilisé par des millions d'utilisateurs
- ✅ Maintenu activement

GitHub : https://github.com/LibreHardwareMonitor/LibreHardwareMonitor

## 📝 Licence

LibreHardwareMonitor est sous licence MPL 2.0 (Mozilla Public License 2.0).
Compatible avec l'utilisation dans ce projet.
