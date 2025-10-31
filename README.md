# 5GHz Cleaner

> Optimiseur système Windows moderne et intuitif avec monitoring temps réel

## 📋 À propos

5GHz Cleaner est un outil d'optimisation système complet pour Windows, offrant une interface moderne et intuitive pour nettoyer, optimiser et surveiller votre PC en temps réel.

## ✨ Fonctionnalités

### 🧹 Nettoyage Intelligent
- Suppression des fichiers temporaires Windows
- Nettoyage du cache système et applications
- Vidage de la corbeille et fichiers inutiles
- Prévisualisation détaillée avant nettoyage
- Opérations sécurisées et avancées

### 💾 Optimisation Disque
- Défragmentation intelligente
- Nettoyage des secteurs défectueux
- Optimisation SSD (TRIM)
- Analyse de l'espace disque
- Gestion de la mémoire standby

### 📊 Monitoring Temps Réel
- **CPU** - Utilisation, température, fréquence
- **RAM** - Mémoire utilisée/disponible, cache
- **GPU** - Charge, température, VRAM
- **Disques** - Lecture/écriture, espace disponible
- Graphiques en temps réel et historique

### 🎨 Interface Moderne
- Design dark élégant et responsive
- Animations fluides
- Thème personnalisable
- Navigation intuitive
- Feedback visuel en temps réel

## 📦 Installation

### Prérequis
- Windows 10/11
- Python 3.11 ou supérieur
- Droits administrateur (pour certaines fonctionnalités)

### Installation Standard

```bash
# Cloner le projet
git clone https://github.com/votre-repo/5Ghz_Cleaner.git
cd 5Ghz_Cleaner

# Installer les dépendances
pip install -r requirements.txt

# Télécharger LibreHardwareMonitor
python download_librehardwaremonitor.py

# Lancer l'application
python main.py
```

### Installation Développeur

```bash
# Installer les dépendances de développement
pip install -r requirements-dev.txt

# Construire l'exécutable
python build.py
```

## ⚙️ Configuration

Créez un fichier `.env` à partir de `.env.example` :

```bash
cp .env.example .env
```

Variables disponibles :
- `DEBUG_MODE` - Active le mode debug
- `LOG_LEVEL` - Niveau de logging (INFO, DEBUG, ERROR)
- `THEME` - Thème de l'interface (dark, light)
- `AUTO_UPDATE` - Mise à jour automatique des données

## 🚀 Utilisation

1. **Lancer l'application** en mode administrateur pour accéder à toutes les fonctionnalités
2. **Analyser** votre système depuis l'onglet principal
3. **Prévisualiser** les opérations de nettoyage
4. **Nettoyer** en un clic les fichiers inutiles
5. **Surveiller** les performances en temps réel

## 🛠️ Technologies

- **Python 3.11+** - Langage principal
- **Flet** - Framework UI moderne
- **LibreHardwareMonitor** - Monitoring matériel
- **WMI** - Interface de gestion Windows
- **psutil** - Informations système
- **Threading** - Opérations asynchrones

## 📁 Structure du Projet

```
5Ghz_Cleaner/
├── backend/          # Logique métier
│   ├── cleaner.py    # Nettoyage système
│   ├── optimizer.py  # Optimisation disque
│   └── monitor.py    # Monitoring matériel
├── frontend/         # Interface utilisateur
│   ├── pages/        # Pages de l'application
│   └── components/   # Composants réutilisables
├── config/           # Configuration
├── assets/           # Ressources (icônes, images)
└── main.py           # Point d'entrée
```

## 🔒 Sécurité

- Écritures atomiques pour éviter la corruption de données
- Validation stricte des chemins de fichiers
- Protection contre les injections de commandes
- Logs sécurisés sans fuites d'informations sensibles
- Backup automatique avant modifications critiques

## 🐛 Dépannage

### L'application ne démarre pas
- Vérifiez que Python 3.11+ est installé
- Installez les dépendances : `pip install -r requirements.txt`
- Lancez en mode administrateur

### Le monitoring ne fonctionne pas
- Téléchargez LibreHardwareMonitor : `python download_librehardwaremonitor.py`
- Vérifiez les droits administrateur

### Erreur de privilèges
- Lancez l'application en tant qu'administrateur
- Utilisez `diagnostic_privileges.py` pour diagnostiquer

## 📝 Licence

**Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International**

Ce projet est sous licence CC BY-NC-SA 4.0. Voir [LICENSE](LICENSE) pour plus de détails.

- ✅ Usage personnel autorisé
- ✅ Modifications autorisées
- ✅ Partage autorisé (même licence)
- ❌ Usage commercial interdit

## 💬 Support & Communauté

- 💭 **Discord** - [Rejoindre le serveur](https://discord.gg/votre-lien)
- 🐛 **Issues** - [Signaler un bug](https://github.com/votre-repo/5Ghz_Cleaner/issues)
- 📖 **Wiki** - [Documentation complète](https://github.com/votre-repo/5Ghz_Cleaner/wiki)

## 🤝 Contribution

Les contributions sont les bienvenues ! Consultez notre guide de contribution pour commencer.

## 📊 Roadmap

- [ ] Support multi-langues
- [ ] Planification automatique de nettoyage
- [ ] Profils d'optimisation personnalisés
- [ ] Export des rapports en PDF
- [ ] Mode portable

---

**Développé avec ❤️ pour Windows** | Version 1.0.0
