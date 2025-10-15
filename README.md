# 5GH'z Cleaner

<div align="center">

![5GHz Cleaner Logo](https://img.shields.io/badge/5GHz-Cleaner-blue?style=for-the-badge&logo=windows&logoColor=white)

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg?style=flat-square)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%2011-0078D6.svg?style=flat-square&logo=windows11)](https://github.com/UndKiMi/5Ghz_Cleaner)
[![Open Source](https://img.shields.io/badge/Open%20Source-Yes-success.svg?style=flat-square&logo=github)](https://github.com/UndKiMi/5Ghz_Cleaner)
[![No Telemetry](https://img.shields.io/badge/Telemetry-None-success.svg?style=flat-square&logo=adguard)](https://github.com/UndKiMi/5Ghz_Cleaner)

**Nettoyeur Windows 11 sécurisé et transparent**

Libérez de l'espace disque en toute sécurité avec un outil open source qui respecte votre vie privée.

[🚀 Télécharger](#-installation) • [📖 Documentation](#-guide-dutilisation) • [🔒 Sécurité](#️-sécurité-et-confidentialité)

</div>

---

## 🎯 Pourquoi 5GH'z Cleaner ?

**Un nettoyeur Windows qui met la sécurité et la transparence en priorité.**

- ✅ **Sécurité maximale** - 350+ chemins système protégés, point de restauration automatique
- ✅ **Zéro télémétrie** - Aucune collecte de données, fonctionnement 100% local
- ✅ **Prévisualisation obligatoire** - Voyez exactement ce qui sera supprimé avant toute action
- ✅ **100% gratuit et open source** - Code auditable, pas de publicités, pas de version premium
- ✅ **Interface moderne** - Simple et intuitive, conçue pour Windows 11

---

## 🚀 Installation

### Télécharger l'exécutable (Recommandé)

1. Téléchargez la dernière version depuis [**Releases**](https://github.com/UndKiMi/5Ghz_Cleaner/releases)
2. Lancez `5Ghz_Cleaner.exe`
3. Acceptez l'élévation des privilèges (nécessaire pour le nettoyage système)

> **Note Windows SmartScreen** : Si Windows affiche un avertissement, cliquez sur "Informations complémentaires" puis "Exécuter quand même". C'est normal pour les applications sans certificat de signature (coût : 500€/an).

### Depuis le code source

**Prérequis** : Python 3.11+

```bash
git clone https://github.com/UndKiMi/5Ghz_Cleaner.git
cd 5Ghz_Cleaner
pip install -r requirements.txt
python main.py
```

---

## 📖 Guide d'utilisation

### Démarrage rapide

1. **Lancez** l'application
2. **Sélectionnez** les options de nettoyage souhaitées
3. **Cliquez** sur "🔍 Prévisualiser" pour voir ce qui sera supprimé
4. **Vérifiez** la liste des fichiers
5. **Cliquez** sur "🧹 Nettoyer" pour confirmer

> 💡 Un point de restauration Windows est automatiquement créé avant chaque nettoyage.

### Options disponibles

**Nettoyage rapide**
- Fichiers temporaires Windows et applications
- Cache Windows Update
- Prefetch et cache miniatures
- Historique des fichiers récents
- Rapports d'erreur système
- Corbeille (avec confirmation)
- Windows.old (avec confirmation)

**Options avancées**
- Libération RAM Standby
- Vidage cache DNS
- Désactivation télémétrie Windows
- Nettoyage logs système
- Arrêt services optionnels

---

## 🔒 Sécurité et confidentialité

### Protection système

- **350+ chemins critiques protégés** - Système Windows, applications Microsoft, navigateurs, antivirus
- **Point de restauration automatique** - Créé avant chaque nettoyage
- **Prévisualisation obligatoire** - Aucune suppression sans votre validation
- **Logs détaillés** - Traçabilité complète de toutes les opérations

### Confidentialité garantie

- **Zéro télémétrie** - Aucune donnée collectée ou transmise
- **Fonctionnement 100% local** - Aucune connexion Internet requise
- **Code open source** - Entièrement auditable sur GitHub
- **Conforme RGPD** - Respect total de votre vie privée

**Vérifiez par vous-même** :
```bash
python backend/telemetry_checker.py
```

---

## ❓ Questions fréquentes

**Est-ce sûr d'utiliser ce logiciel ?**  
Oui. Le code est open source et auditable. Un point de restauration est automatiquement créé avant chaque nettoyage, vous permettant de revenir en arrière si nécessaire.

**Mes données sont-elles collectées ?**  
Non. Aucune donnée n'est collectée, stockée ou transmise. Le logiciel fonctionne entièrement en local.

**Combien d'espace puis-je libérer ?**  
Cela dépend de votre utilisation. En moyenne, entre 500 Mo et 10 Go peuvent être récupérés.

**Pourquoi la prévisualisation est-elle obligatoire ?**  
C'est une mesure de sécurité pour éviter toute suppression accidentelle. Vous voyez exactement ce qui sera supprimé avant toute action.

**Compatible avec Windows 10 ?**  
Non, ce logiciel est conçu spécifiquement pour Windows 11 (Build 22000+).

---

## 📝 Documentation

- [**CHANGELOG.md**](CHANGELOG.md) - Historique des versions
- [**SECURITY.md**](SECURITY.md) - Rapport de sécurité détaillé
- [**PRIVACY.md**](PRIVACY.md) - Politique de confidentialité
- [**LICENSE**](LICENSE) - Licence CC BY-NC-SA 4.0

---

## 🤝 Contribuer

Les contributions sont bienvenues ! Vous pouvez :
- Signaler des bugs via [GitHub Issues](https://github.com/UndKiMi/5Ghz_Cleaner/issues)
- Proposer des améliorations
- Soumettre des pull requests
- Améliorer la documentation

---

## 📜 Licence

**Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**

✅ **Autorisé** : Utilisation gratuite, modification, distribution (avec attribution)  
❌ **Interdit** : Usage commercial, vente du logiciel

Voir [LICENSE](LICENSE) pour les détails complets.

---

<div align="center">

**5GH'z Cleaner** - Nettoyeur Windows 11 sécurisé

[GitHub](https://github.com/UndKiMi/5Ghz_Cleaner) • [Releases](https://github.com/UndKiMi/5Ghz_Cleaner/releases) • [Issues](https://github.com/UndKiMi/5Ghz_Cleaner/issues)

**Licence** : CC BY-NC-SA 4.0

</div>
