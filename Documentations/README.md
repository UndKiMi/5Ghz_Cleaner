# 5GH'z Cleaner

Application de nettoyage et d'optimisation Windows avec interface moderne.

## 📁 Structure du Projet

```
5Ghz_Cleaner/
├── assets/                      # Ressources statiques
│   └── icons/                   # Icônes SVG
├── backend/                     # Logique métier
│   ├── __init__.py
│   ├── cleaner.py              # Fonctions de nettoyage
│   └── elevation.py            # Gestion des privilèges admin
├── frontend/                    # Interface utilisateur
│   ├── design_system/          # Système de design
│   │   ├── theme.py            # Tokens (couleurs, espacements)
│   │   ├── buttons.py          # Composants boutons
│   │   ├── containers.py       # Composants conteneurs
│   │   ├── text.py             # Composants texte
│   │   ├── icons.py            # Composants icônes
│   │   └── inputs.py           # Composants inputs
│   ├── pages/                  # Pages de l'application
│   │   └── main_page.py        # Page principale
│   └── app.py                  # Application Flet
├── main.py                     # Point d'entrée
├── requirements.txt            # Dépendances
├── DESIGN_SYSTEM.md           # Documentation design system
└── PROJECT_STRUCTURE.md       # Architecture détaillée
```

## Installation

1. Installer les dépendances:
```bash
pip install -r requirements.txt
```

## Utilisation

Lancer l'application:
```bash
python main.py
```

L'application demandera automatiquement les privilèges administrateur (UAC).

## Compilation en Exécutable

Pour compiler l'application en un exécutable Windows:

```bash
# Installer flet
pip install flet

# Compiler l'application
flet pack main.py --name "5Ghz_Cleaner" --icon image.jpg
```

## ✨ Fonctionnalités

### 🧹 Nettoyage Rapide
- **Fichiers temporaires** : Supprime les fichiers temporaires et cache système
- **RAM Standby** : Libère la mémoire en attente
- **Cache DNS** : Vide le cache réseau

### ⚙️ Options Avancées
- **Libérer RAM Standby** (Recommandé) : Vide la mémoire en attente pour libérer de la RAM
- **Flush DNS** (Recommandé) : Vide le cache DNS pour améliorer les performances réseau
- **Désactiver télémétrie** : Désactive les services de collecte de données de Windows
- **Nettoyer logs volumineux** (Recommandé) : Supprime les fichiers journaux volumineux

### 🔧 Opérations incluses
- Nettoyage des fichiers temporaires (User & System)
- Cache Windows Update
- Prefetch
- Fichiers récents
- Cache des miniatures
- Dumps de crash
- Windows.old
- Corbeille

## 🎨 Interface

- **Design System** : Composants réutilisables et cohérents
- **Thème sombre** : Interface moderne et élégante
- **Onglets** : Navigation entre nettoyage rapide et options avancées
- **Barre de progression** : Suivi en temps réel du nettoyage
- **Switches** : Configuration intuitive des options
- **Résumé** : Dialogue avec statistiques de nettoyage

## 🏗️ Architecture

### Backend
Logique métier pure sans dépendances UI :
- Fonctions de nettoyage Windows
- Gestion des privilèges administrateur
- Opérations système sécurisées

### Frontend
Interface Flet avec design system :
- Composants UI modulaires
- Tokens de design centralisés
- Pages organisées
- Gestion d'état réactive

### Sécurité
- Aucune communication réseau
- Opérations locales uniquement
- Demande de privilèges administrateur
- Gestion d'erreurs robuste

## Auteur

**UndKiMi**
- GitHub: https://github.com/UndKiMi
- Repository: https://github.com/UndKiMi/5Ghz_Cleaner

## Licence

Tous droits réservés par UndKiMi
