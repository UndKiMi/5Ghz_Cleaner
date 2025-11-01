# 5GH'z Cleaner

<div align="center">

![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%2011-0078D6.svg)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB.svg)
![Version](https://img.shields.io/badge/Version-1.7.0-green.svg)
![Security](https://img.shields.io/badge/Security-Hardened-brightgreen.svg)

[![Security Audit](https://github.com/UndKiMi/5Ghz_Cleaner/actions/workflows/security-audit.yml/badge.svg)](https://github.com/UndKiMi/5Ghz_Cleaner/actions/workflows/security-audit.yml)
[![Code Quality](https://github.com/UndKiMi/5Ghz_Cleaner/actions/workflows/code-quality.yml/badge.svg)](https://github.com/UndKiMi/5Ghz_Cleaner/actions/workflows/code-quality.yml)
[![Trivy](https://github.com/UndKiMi/5Ghz_Cleaner/actions/workflows/trivy-security.yml/badge.svg)](https://github.com/UndKiMi/5Ghz_Cleaner/actions/workflows/trivy-security.yml)
[![OpenSSF Scorecard](https://github.com/UndKiMi/5Ghz_Cleaner/actions/workflows/scorecard.yml/badge.svg)](https://github.com/UndKiMi/5Ghz_Cleaner/actions/workflows/scorecard.yml)
[![Secret Scanning](https://github.com/UndKiMi/5Ghz_Cleaner/actions/workflows/secret-scan.yml/badge.svg)](https://github.com/UndKiMi/5Ghz_Cleaner/actions/workflows/secret-scan.yml)

**Outil professionnel de nettoyage et d'optimisation pour Windows 11**

[Installation](#-installation) • [Fonctionnalités](#-fonctionnalités) • [Utilisation](#-utilisation) • [Licence](#-licence)

</div>

---

## 📋 Description

**5GH'z Cleaner** est un outil de maintenance système moderne pour Windows 11, offrant nettoyage, optimisation et monitoring matériel en temps réel. Interface élégante, opérations sécurisées, performances optimales.

### Pourquoi 5GH'z Cleaner ?

- ✅ **Interface moderne** - Design épuré avec Flet
- ✅ **Ultra-rapide** - Optimisations parallèles (5-7x plus rapide)
- ✅ **Sécurité renforcée** - Validation quadruple couche, vérification d'intégrité
- ✅ **Complet** - Nettoyage + Optimisation + Monitoring
- ✅ **Transparent** - Logs sécurisés, code open-source
- ✅ **Protection maximale** - Backup automatique, cooldown 10 minutes

---

## ✨ Fonctionnalités

### 🧹 Nettoyage Système

- **Fichiers temporaires** - Suppression sécurisée avec backup automatique
- **Cache Windows Update** - Nettoyage optimisé (scan limité 2 niveaux)
- **WinSxS** - Nettoyage ultra-rapide (1-3 min au lieu de 10-20 min)
- **Prefetch & Miniatures** - Suppression rapide
- **Corbeille** - Vidage complet avec confirmation
- **Logs volumineux** - Suppression fichiers > 100 MB

### ⚡ Optimisations

- **RAM Standby** - Libération mémoire (jusqu'à 20%)
- **DNS Flush** - Vidage cache DNS
- **Optimisation disque automatique** - Détection HDD/SSD/NVMe + optimisations spécifiques
  - HDD: Défragmentation + Indexation optimisée
  - SSD: TRIM + Désactivation défrag + Désactivation indexation
  - NVMe: TRIM + Désactivation indexation + Mode Hautes performances
- **Cooldown intelligent** - Protection anti-spam de 10 minutes sur actions critiques

### 📊 Monitoring Temps Réel

- **Température CPU/GPU** - Surveillance avec LibreHardwareMonitor
- **Utilisation RAM** - Détails complets (utilisée, disponible, standby)
- **Espace disque** - Analyse tous les lecteurs
- **Performances** - Vue d'ensemble système

### 🔒 Sécurité Renforcée

- **Validation quadruple couche** - Liens symboliques, hard links, junction points
- **Vérification d'intégrité** - Hash SHA256 des DLLs critiques
- **Backup automatique** - Sauvegarde avant toute suppression
- **Mode Dry-Run** - Prévisualisation ultra-rapide (5-10s)
- **Point de restauration** - Création automatique au démarrage
- **Logs sécurisés** - Thread-safe, chemins masqués
- **Cooldown 10 minutes** - Protection anti-spam renforcée
- **Élévation contrôlée** - Validation post-élévation des privilèges

---

## 🚀 Installation

### Prérequis

- **Windows 11** (64-bit) - OBLIGATOIRE
- **Python 3.11+** - [Télécharger](https://www.python.org/downloads/)
- **Droits administrateur** - Requis

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

---

## 🎯 Utilisation

### Démarrage

```bash
python main.py
```

L'application démarre **directement** (pas de page de conditions).

### Mode Prévisualisation (Recommandé)

1. Cliquer sur **"Prévisualiser le nettoyage"**
2. Attendre l'analyse parallèle (5-10s)
3. Consulter le rapport détaillé
4. Cocher/décocher les opérations
5. Lancer le nettoyage

### Actions Rapides

| Bouton | Action | Cooldown |
|--------|--------|----------|
| 🧹 **Nettoyer** | Fichiers temporaires + backup | 10 min |
| 💾 **Libérer RAM** | Vide RAM Standby | 10 min |
| 🗑️ **Vider corbeille** | Suppression définitive | 10 min |
| 🌐 **Flush DNS** | Vide cache DNS | 10 min |

### Optimisation Disque (Nouveau)

**Onglet Configuration → Disque C:\ → Bouton "Optimiser"**

- Détection automatique du type (HDD/SSD/NVMe)
- Optimisations spécifiques appliquées
- Barre de progression intégrée (pas de pop-up)
- Résultat affiché dans le bouton
- Cooldown visible de 3 minutes

---

## 🆕 Nouveautés v1.7.0 - Sécurité Renforcée

### 🔒 Correctifs de Sécurité Majeurs

#### Validation Avancée des Chemins
- **Détection liens symboliques** - Résolution et validation des cibles
- **Détection hard links** - Blocage des fichiers avec nlink > 1
- **Détection junction points** - Protection contre suppressions récursives hors scope
- **Validation quadruple couche** - Sécurité maximale

#### Vérification d'Intégrité
- **Hash SHA256 des DLLs** - Vérification LibreHardwareMonitor et dépendances
- **Base de données de hash** - Détection de fichiers corrompus ou modifiés
- **Validation au démarrage** - Contrôle automatique avant utilisation

#### Backup Automatique
- **Sauvegarde avant suppression** - Tous les fichiers backupés
- **Restauration complète** - Rollback en cas d'erreur
- **Manifeste détaillé** - Traçabilité complète
- **Nettoyage automatique** - Backups > 7 jours supprimés

#### Protection Renforcée
- **Cooldown 10 minutes** - Protection anti-spam maximale
- **Logs sécurisés** - Chemins utilisateurs masqués (C:\Users\***)
- **Élévation validée** - Re-vérification post-élévation
- **SSL strict** - Vérification certificats pour téléchargements

### ⚡ Performances (v1.6.1)

- **Dry-run 5-7x plus rapide** - Parallélisation 8 threads
- **Nettoyage 3-4x plus rapide** - os.scandir() + cache
- **WinSxS 5-10x plus rapide** - Analyse préalable

### 🎨 Interface (v1.6.1)

- **Démarrage direct** - Pas de page conditions
- **Bouton optimisation disque** - Feedback visuel intégré
- **Cooldown visible** - Timer dégressif
- **Expérience fluide** - Aucun pop-up
- **Logs thread-safe** - Écritures atomiques
- **Protection anti-spam** - Timer visible

---

## 📁 Structure

```
5Ghz_Cleaner/
├── main.py                    # Point d'entrée
├── README.md                  # Documentation
├── requirements.txt           # Dépendances
│
├── src/
│   ├── core/                  # Logique métier
│   │   ├── cleaner.py        # Nettoyage (optimisé, quadruple validation)
│   │   ├── dry_run.py        # Dry-run (parallèle, 8 threads)
│   │   ├── disk_auto_optimizer.py  # Optimisation disque auto
│   │   └── advanced_optimizations.py
│   │
│   ├── services/              # Services
│   │   ├── hardware_monitor.py
│   │   └── security_core.py  # Validation chemins
│   │
│   ├── ui/                    # Interface
│   │   ├── app.py            # Application Flet
│   │   ├── design_system/    # Composants UI
│   │   └── pages/            # Pages (main, preview)
│   │
│   └── utils/                 # Utilitaires
│       ├── logger_safe.py    # Logs thread-safe
│       ├── integrity_checker.py  # Vérification SHA256
│       ├── path_validator.py # Validation avancée
│       ├── backup_manager.py # Backup automatique
│       └── elevation.py      # Privilèges
│
├── config/                    # Configuration
├── assets/                    # Ressources
├── libs/                      # Bibliothèques
└── scripts/                   # Scripts
```

---

## 🔧 Développement

### Conventions

- **Style**: PEP 8
- **Type Hints**: Obligatoires
- **Docstrings**: Google Style
- **Logging**: `CleaningLogger`

### Tests

```bash
# Vérifier imports
python -c "from src.core import cleaner; print('✓ OK')"

# Tester dry-run
python -c "from src.core.dry_run import dry_run_manager; print('✓ OK')"
```

---

## 🛡️ Audits de Sécurité

Ce projet intègre une suite complète d'outils d'audit automatisés via GitHub Actions :

### 🔒 Security Audit (Workflow Consolidé)
- **CodeQL** - Analyse statique avancée (Microsoft)
- **Bandit** - Linter de sécurité Python
- **Safety** - Vérification vulnérabilités CVE
- **Trivy** - Scanner multi-format
- **Gitleaks** - Détection secrets exposés

### 📊 Code Quality
- **Pylint** - Analyse qualité code
- **Black** - Formatage automatique
- **isort** - Organisation imports
- **Flake8** - Vérification style
- **Pytest** - Tests unitaires

### 🎯 Autres Audits
- **Dependabot** - Mises à jour automatiques
- **OpenSSF Scorecard** - Score sécurité global
- **Secret Scanning** - TruffleHog + Gitleaks

### ⏰ Fréquence
- **Push/PR** : Security Audit, Code Quality
- **Hebdomadaire** : Scorecard (lundi 2h), Dependabot (lundi 9h)

Tous les résultats sont disponibles dans l'onglet **Actions** du dépôt GitHub.

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. **Fork** le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit les changements (`git commit -m 'Ajout fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une **Pull Request**

### Guidelines

- Respecter PEP 8
- Ajouter des tests pour les nouvelles fonctionnalités
- Mettre à jour la documentation
- Suivre les conventions de sécurité existantes

---

## 📄 Licence

**CC BY-NC-SA 4.0** - Creative Commons Attribution-NonCommercial-ShareAlike 4.0

### Vous êtes libre de :

- ✅ **Partager** - Copier et redistribuer
- ✅ **Adapter** - Modifier et créer des dérivés
- 📝 **Attribution** - Créditer l'auteur original
- 🚫 **Non-commercial** - Pas d'utilisation commerciale
- 🔄 **Partage identique** - Même licence pour les dérivés

---

## ⚠️ Avertissement

Cet outil effectue des opérations système sensibles :

- ⚠️ Utilisez à vos propres risques
- ⚠️ Point de restauration créé automatiquement
- ⚠️ Backup automatique avant toute suppression
- ⚠️ Testez en mode prévisualisation d'abord
- ⚠️ Lisez les avertissements avant toute action

**L'auteur ne peut être tenu responsable des dommages causés par une mauvaise utilisation.**

---

<div align="center">

**Version 1.7.0 - Security Hardened** • **Novembre 2025**

Made with ❤️ for Windows 11 users

[![Star on GitHub](https://img.shields.io/github/stars/UndKiMi/5Ghz_Cleaner?style=social)](https://github.com/UndKiMi/5Ghz_Cleaner)
[![Issues](https://img.shields.io/github/issues/UndKiMi/5Ghz_Cleaner)](https://github.com/UndKiMi/5Ghz_Cleaner/issues)
[![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-blue.svg)](LICENSE)

</div>
