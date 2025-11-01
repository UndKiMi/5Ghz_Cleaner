# 5GH'z Cleaner

<div align="center">

![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%2011-0078D6.svg)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB.svg)
![Version](https://img.shields.io/badge/Version-1.6.0-green.svg)

**Outil professionnel de nettoyage et d'optimisation pour Windows 11**

[Fonctionnalités](#-fonctionnalités) • [Installation](#-installation) • [Utilisation](#-utilisation) • [Structure](#-structure-du-projet) • [Licence](#-licence)

</div>

---

## 📋 Description

**5GH'z Cleaner** est un outil de maintenance système complet pour Windows 11, offrant une interface moderne et intuitive pour nettoyer, optimiser et surveiller votre système. Conçu avec une architecture modulaire et sécurisée, il combine puissance et facilité d'utilisation.

### Pourquoi 5GH'z Cleaner ?

- ✅ **Interface moderne** - UI élégante avec Flet
- ✅ **Sécurisé** - Mode prévisualisation, point de restauration automatique
- ✅ **Complet** - Nettoyage, optimisation, monitoring en un seul outil
- ✅ **Performant** - Architecture optimisée, opérations thread-safe
- ✅ **Transparent** - Logs détaillés, code open-source

---

## ✨ Fonctionnalités

### 🧹 Nettoyage Système

| Fonctionnalité | Description | Espace Libéré |
|----------------|-------------|---------------|
| **Fichiers temporaires** | Suppression sécurisée des fichiers inutiles | Variable |
| **Cache Windows Update** | Nettoyage du cache de mise à jour | Jusqu'à plusieurs GB |
| **Prefetch** | Optimisation du cache de démarrage | ~100 MB |
| **Miniatures** | Suppression du cache d'images | ~500 MB |
| **Corbeille** | Vidage complet avec confirmation | Variable |
| **Logs volumineux** | Suppression des fichiers .log > 100 MB | Variable |

### ⚡ Optimisation

- **RAM Standby** - Libération de la mémoire en attente (jusqu'à 20% de RAM)
- **DNS Flush** - Vidage du cache DNS pour résoudre les problèmes réseau
- **Optimisation disque** - Défragmentation et optimisation SSD/HDD
- **Désactivation hibernation** - Récupération de l'espace disque (taille de la RAM)

### 📊 Monitoring en Temps Réel

- **Température CPU/GPU** - Surveillance avec LibreHardwareMonitor
- **Utilisation RAM** - Détails (utilisée, disponible, standby)
- **Espace disque** - Analyse de tous les lecteurs
- **Performances système** - Vue d'ensemble complète

### 🔒 Sécurité

- **Mode Dry-Run** - Prévisualisation avant toute action
- **Point de restauration** - Création automatique au démarrage
- **Validation des chemins** - Protection contre les suppressions accidentelles
- **Logs détaillés** - Traçabilité complète de toutes les opérations
- **Protection anti-spam** - Cooldown sur les actions critiques

---

## 🚀 Installation

### Prérequis

- **Windows 11** (64-bit) - **OBLIGATOIRE**
- **Python 3.11+** - [Télécharger Python](https://www.python.org/downloads/)
- **Droits administrateur** - Requis pour certaines opérations

### Installation Rapide

```bash
# 1. Cloner le dépôt
git clone https://github.com/UndKiMi/5Ghz_Cleaner.git
cd 5Ghz_Cleaner

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
python main.py
```

### Dépendances Principales

```
flet>=0.23.0              # Framework UI moderne
psutil>=5.9.0             # Informations système
pythonnet>=3.0.0          # Interopérabilité .NET (LibreHardwareMonitor)
pywin32>=306              # API Windows
requests>=2.31.0          # Téléchargement LibreHardwareMonitor
```

---

## 🎯 Utilisation

### Démarrage

L'application demande automatiquement l'élévation des privilèges administrateur au lancement :

```bash
python main.py
```

**Séquence de démarrage :**
1. ✅ Vérification Windows 11
2. ✅ Optimisation des ressources (CPU, RAM)
3. ✅ Élévation des privilèges
4. ✅ Création du point de restauration
5. ✅ Initialisation du monitoring matériel
6. ✅ Lancement de l'interface

### Mode Prévisualisation (Recommandé)

**Avant tout nettoyage, utilisez le mode dry-run :**

1. Cliquer sur **"Prévisualiser le nettoyage"**
2. Attendre l'analyse (10-15 secondes)
3. Consulter le rapport détaillé :
   - Fichiers à supprimer
   - Espace à libérer
   - Opérations sélectionnées
4. Cocher/décocher les opérations souhaitées
5. Cliquer sur **"Lancer le nettoyage"**

### Actions Rapides

**Onglet "Nettoyage rapide" :**

| Bouton | Action | Durée |
|--------|--------|-------|
| 🧹 **Nettoyer** | Supprime les fichiers temporaires | ~5s |
| 💾 **Libérer RAM** | Vide la RAM Standby | Instantané |
| 🗑️ **Vider corbeille** | Suppression définitive | ~2s |
| 🌐 **Flush DNS** | Vide le cache DNS | Instantané |

### Options Avancées

**Onglet "Options avancées" :**

- ☑️ **Vider RAM Standby** - Libère la mémoire en attente
- ☑️ **Flush DNS** - Vide le cache DNS
- ☑️ **Nettoyer logs volumineux** - Supprime les .log > 100 MB
- ⚠️ **Désactiver télémétrie** - Expérimental (Windows Update)

---

## 📁 Structure du Projet

```
5Ghz_Cleaner/
│
├── src/                          # Code source principal
│   ├── core/                     # Logique métier
│   │   ├── cleaner.py           # Moteur de nettoyage
│   │   ├── dry_run.py           # Mode prévisualisation
│   │   ├── file_scanner.py      # Scanner de fichiers
│   │   ├── disk_optimizer.py    # Optimisation disque
│   │   ├── ram_manager.py       # Gestion RAM
│   │   └── advanced_optimizations.py
│   │
│   ├── services/                 # Services système
│   │   ├── hardware_monitor.py  # Monitoring matériel
│   │   ├── hardware_sensors.py  # Capteurs température
│   │   ├── security.py          # Sécurité
│   │   ├── security_core.py     # Noyau sécurité
│   │   └── telemetry_checker.py # Télémétrie
│   │
│   ├── ui/                       # Interface utilisateur
│   │   ├── app.py               # Application Flet
│   │   ├── design_system/       # Système de design
│   │   └── pages/               # Pages (main, preview)
│   │
│   └── utils/                    # Utilitaires
│       ├── logger.py            # Système de logs
│       ├── logger_safe.py       # Logs thread-safe
│       ├── elevation.py         # Élévation privilèges
│       └── console_colors.py    # Console colorée
│
├── assets/                       # Ressources statiques
│   └── icons/                   # Icônes SVG
│
├── config/                       # Configuration
│   ├── settings.py              # Paramètres globaux
│   └── constants.py             # Constantes
│
├── libs/                         # Bibliothèques externes
│   └── LibreHardwareMonitorLib.dll
│
├── scripts/                      # Scripts utilitaires
│   ├── build.py                 # Build de l'exécutable
│   └── download_librehardwaremonitor.py
│
├── tests/                        # Tests
│
├── main.py                       # Point d'entrée
├── requirements.txt              # Dépendances
└── README.md                     # Ce fichier
```

### Architecture Logicielle

```
┌─────────────────────────────────────────────────┐
│              Interface (Flet UI)                │
│              src/ui/app.py                      │
└────────────────┬────────────────────────────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
┌───▼──────────┐    ┌────────▼─────────┐
│   Core       │    │   Services       │
│              │    │                  │
│ • cleaner    │    │ • hardware_mon   │
│ • dry_run    │    │ • security       │
│ • scanner    │    │ • telemetry      │
└───┬──────────┘    └────────┬─────────┘
    │                        │
    └────────────┬───────────┘
                 │
        ┌────────▼─────────┐
        │   Utilities      │
        │                  │
        │ • logger         │
        │ • elevation      │
        │ • system_cmds    │
        └──────────────────┘
```

---

## 🔧 Développement

### Conventions de Code

- **Style** : PEP 8
- **Type Hints** : Obligatoires pour les fonctions publiques
- **Docstrings** : Format Google Style
- **Logging** : Utiliser `CleaningLogger` pour toutes les opérations

### Ajouter une Nouvelle Fonctionnalité

1. **Logique métier** → `src/core/`
2. **Service système** → `src/services/`
3. **Composant UI** → `src/ui/`
4. **Utilitaire** → `src/utils/`

### Scripts Utiles

```bash
# Mettre à jour les imports après réorganisation
python scripts/update_imports.py

# Construire l'exécutable
python scripts/build.py

# Diagnostiquer les privilèges
python scripts/diagnostic_privileges.py
```

### Tests

```bash
# Exécuter les tests
python tests/test_privileges.py

# Vérifier les imports
python -c "from src.core import cleaner; print('✓ OK')"
```

---

## 📊 Logs

Les logs sont stockés dans :
```
C:\Users\<Username>\AppData\Local\5GHz_Cleaner\logs\
```

**Niveaux de log :**
- `DEBUG` - Informations détaillées
- `INFO` - Opérations normales
- `WARNING` - Avertissements
- `ERROR` - Erreurs
- `SUCCESS` - Opérations réussies

---

## 🛡️ Sécurité

### Protections Implémentées

- ✅ **Écritures atomiques** - Logs thread-safe
- ✅ **Validation des chemins** - Protection path traversal
- ✅ **Point de restauration** - Backup automatique
- ✅ **Mode dry-run** - Prévisualisation sécurisée
- ✅ **Protection anti-spam** - Cooldown sur les actions

### Fichiers Protégés

L'application **ne supprime JAMAIS** :
- Fichiers système Windows (`C:\Windows\System32\`)
- Fichiers en cours d'utilisation
- Fichiers dans des chemins protégés
- Fichiers sans extension connue

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. **Fork** le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une **Pull Request**

### Guidelines

- Respecter PEP 8
- Ajouter des tests pour les nouvelles fonctionnalités
- Mettre à jour la documentation
- Utiliser des commits descriptifs

---

## 📄 Licence

Ce projet est sous licence **CC BY-NC-SA 4.0** (Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International).

### Vous êtes libre de :

- ✅ **Partager** - Copier et redistribuer le matériel
- ✅ **Adapter** - Remixer, transformer et créer à partir du matériel

### Conditions :

- 📝 **Attribution** - Vous devez créditer l'auteur original
- 🚫 **Pas d'utilisation commerciale** - Vous ne pouvez pas utiliser ce projet à des fins commerciales
- 🔄 **Partage dans les mêmes conditions** - Si vous modifiez ce projet, vous devez distribuer vos contributions sous la même licence

**Voir le fichier [LICENSE](LICENSE) pour plus de détails.**

---

## 👤 Auteur

**UndKiMi**

- GitHub: [@UndKiMi](https://github.com/UndKiMi)
- Projet: [5GH'z Cleaner](https://github.com/UndKiMi/5Ghz_Cleaner)

---

## 🙏 Remerciements

- **[Flet](https://flet.dev/)** - Framework UI moderne et réactif
- **[LibreHardwareMonitor](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor)** - Monitoring matériel
- **[Python](https://www.python.org/)** - Langage de programmation
- **Communauté Open Source** - Pour l'inspiration et le support

---

## ⚠️ Avertissement

Cet outil effectue des opérations système sensibles. Bien qu'il soit conçu pour être sûr :

- ⚠️ **Utilisez à vos propres risques**
- ⚠️ Un point de restauration est créé automatiquement
- ⚠️ **Testez en mode prévisualisation d'abord**
- ⚠️ Lisez les avertissements avant de confirmer toute action

**L'auteur ne peut être tenu responsable des dommages causés par une mauvaise utilisation.**

---

## 📞 Support

### Problèmes et Questions

- 📖 Consultez d'abord ce README
- 🔍 Vérifiez les [Issues existantes](https://github.com/UndKiMi/5Ghz_Cleaner/issues)
- 🆕 Ouvrez une [Nouvelle Issue](https://github.com/UndKiMi/5Ghz_Cleaner/issues/new)

### FAQ

**Q: L'application ne démarre pas**  
R: Vérifiez que vous avez Python 3.11+ et Windows 11. Exécutez `python main.py` en tant qu'administrateur.

**Q: LibreHardwareMonitor ne fonctionne pas**  
R: L'application télécharge automatiquement la DLL au premier lancement. Vérifiez votre connexion internet.

**Q: Puis-je annuler un nettoyage ?**  
R: Non, une fois lancé, le nettoyage ne peut pas être annulé. Utilisez toujours le mode prévisualisation d'abord.

**Q: Est-ce sûr ?**  
R: Oui, l'application crée un point de restauration et valide tous les chemins avant suppression.

---

## 📈 Roadmap

### Version 1.7.0 (Prévue)

- [ ] Support multi-langues (EN, FR)
- [ ] Planification automatique du nettoyage
- [ ] Statistiques d'utilisation
- [ ] Export des rapports en PDF

### Version 2.0.0 (Future)

- [ ] Interface web (optionnelle)
- [ ] Support Windows 10 (rétrocompatibilité)
- [ ] Plugins personnalisés
- [ ] Mode silencieux (CLI)

---

<div align="center">

**Version 1.6.0** • **Dernière mise à jour : Novembre 2025**

Made with ❤️ for Windows 11 users

[![Star on GitHub](https://img.shields.io/github/stars/UndKiMi/5Ghz_Cleaner?style=social)](https://github.com/UndKiMi/5Ghz_Cleaner)

</div>
