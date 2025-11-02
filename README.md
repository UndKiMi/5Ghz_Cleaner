# 🧹 5GH'z Cleaner

**Nettoyez et optimisez votre PC Windows 11 en quelques clics !**

Un outil simple et efficace pour libérer de l'espace disque, accélérer votre ordinateur et surveiller ses performances.

![Version](https://img.shields.io/badge/Version-1.7.0-green.svg)
![Windows 11](https://img.shields.io/badge/Windows-11-0078D6.svg)
![Gratuit](https://img.shields.io/badge/Gratuit-100%25-brightgreen.svg)

## 🎯 À quoi ça sert ?

5GH'z Cleaner vous aide à :
- 🗑️ **Libérer de l'espace** - Supprime les fichiers temporaires inutiles
- ⚡ **Accélérer votre PC** - Libère la mémoire RAM et optimise le disque
- 📊 **Surveiller votre système** - Températures, mémoire, espace disque en temps réel
- 🛡️ **En toute sécurité** - Sauvegarde automatique avant chaque action

### Pourquoi choisir 5GH'z Cleaner ?

- ✅ **Facile à utiliser** - Interface claire et intuitive
- ✅ **Rapide** - Nettoyage en quelques minutes
- ✅ **Sûr** - Sauvegarde automatique et point de restauration
- ✅ **Gratuit** - 100% gratuit et sans publicité
- ✅ **Transparent** - Code source ouvert, aucune donnée collectée

## ✨ Que peut faire 5GH'z Cleaner ?

### 🧹 Nettoyage

- **Fichiers temporaires** - Supprime les fichiers inutiles qui encombrent votre disque
- **Corbeille** - Vide la corbeille en un clic
- **Cache Windows** - Nettoie les fichiers de mise à jour obsolètes
- **Miniatures** - Supprime le cache des aperçus d'images

### ⚡ Optimisation

- **Libérer la mémoire** - Récupère jusqu'à 20% de RAM
- **Optimiser le disque** - Défragmente (HDD) ou optimise (SSD/NVMe) automatiquement
- **Vider le cache DNS** - Résout les problèmes de connexion internet

### 📊 Surveillance

- **Température** - Surveille la température de votre processeur et carte graphique
- **Mémoire RAM** - Affiche l'utilisation en temps réel
- **Espace disque** - Montre l'espace disponible sur vos disques

### 🛡️ Sécurité

- **Sauvegarde automatique** - Tous les fichiers sont sauvegardés avant suppression
- **Point de restauration** - Créé automatiquement au démarrage
- **Prévisualisation** - Voyez ce qui sera supprimé avant de confirmer
- **Protection** - Impossible de supprimer des fichiers système importants

---

## 🚀 Comment l'installer ?

### Ce dont vous avez besoin

- **Windows 11** (version 64-bit)
- **Python 3.11 ou plus récent** - [Télécharger ici](https://www.python.org/downloads/)
  - ⚠️ Cochez "Add Python to PATH" pendant l'installation
- **Droits administrateur** sur votre PC

### Étapes d'installation

**1. Téléchargez le logiciel**
```bash
git clone https://github.com/UndKiMi/5Ghz_Cleaner.git
```
Ou téléchargez le ZIP depuis GitHub et décompressez-le.

**2. Ouvrez un terminal dans le dossier**
- Faites un clic droit dans le dossier
- Sélectionnez "Ouvrir dans le Terminal" ou "PowerShell"

**3. Installez les composants nécessaires**
```bash
pip install -r requirements.txt
```

**4. Lancez le logiciel**
```bash
python main.py
```

## 🎯 Comment l'utiliser ?

### Première utilisation

1. **Lancez le logiciel**
   ```bash
   python main.py
   ```
   - Une fenêtre va s'ouvrir
   - Le logiciel va demander les droits administrateur (c'est normal)

2. **Prévisualisez avant de nettoyer** (recommandé)
   - Cliquez sur le bouton **"🔍 Prévisualiser"**
   - Attendez quelques secondes
   - Vous verrez exactement ce qui sera supprimé
   - Cochez ou décochez ce que vous voulez garder

3. **Lancez le nettoyage**
   - Cliquez sur **"🧹 Nettoyer"**
   - Le logiciel fait une sauvegarde automatique
   - Attendez la fin du nettoyage

### Actions rapides disponibles

| Bouton | À quoi ça sert | Temps d'attente |
|--------|------------------|------------------|
| 🧹 **Nettoyer** | Supprime les fichiers temporaires | 10 minutes |
| 💾 **Libérer RAM** | Libère la mémoire | 10 minutes |
| 🗑️ **Vider corbeille** | Vide la corbeille | 10 minutes |
| 🌐 **Vider DNS** | Résout les problèmes internet | 10 minutes |

⚠️ **Pourquoi 10 minutes ?** Pour éviter de nettoyer trop souvent et protéger votre système.

### Optimiser votre disque

1. Allez dans l'onglet **"Configuration"**
2. Trouvez votre disque (ex: C:\)
3. Cliquez sur **"Optimiser"**
4. Le logiciel détecte automatiquement votre type de disque
5. Attendez la fin (quelques minutes)

---

## 🆕 Quoi de neuf dans cette version ?

### Version 1.7.0 - Améliorations de sécurité

**Plus sûr que jamais !**
- ✅ Sauvegarde automatique de tous les fichiers avant suppression
- ✅ Vérification de l'intégrité du logiciel au démarrage
- ✅ Protection renforcée contre les suppressions accidentelles
- ✅ Temps d'attente de 10 minutes entre chaque nettoyage

**Plus rapide !**
- ⚡ Nettoyage 3 à 4 fois plus rapide
- ⚡ Prévisualisation en quelques secondes
- ⚡ Optimisation disque améliorée

**Plus simple !**
- 🎨 Interface plus claire
- 🎨 Pas de fenêtres pop-up gênantes
- 🎨 Retour visuel sur toutes les actions

## ❓ Problèmes courants

### Le logiciel ne se lance pas

**Erreur "Python n'est pas reconnu"**
- Vérifiez que Python est installé
- Réinstallez Python en cochant "Add to PATH"

**Erreur "Module not found"**
```bash
pip install -r requirements.txt
```

### Le logiciel demande les droits administrateur

**C'est normal !** Le logiciel a besoin de ces droits pour :
- Supprimer les fichiers temporaires système
- Optimiser le disque
- Libérer la mémoire

Vous pouvez refuser, mais certaines fonctions seront limitées.

### Mon antivirus bloque le logiciel

**C'est un faux positif.** 5GH'z Cleaner est sûr :
- ✅ Code source ouvert et vérifiable
- ✅ Aucune donnée collectée
- ✅ Aucune connexion internet

**Pour autoriser le logiciel :**
1. Ouvrez votre antivirus
2. Ajoutez une exception pour le dossier 5Ghz_Cleaner
3. Relancez le logiciel

### Le nettoyage est bloqué pendant 10 minutes

**C'est une protection !** Pour éviter de nettoyer trop souvent et protéger votre système.

Si vous avez vraiment besoin de nettoyer avant, redémarrez le logiciel.

### J'ai supprimé quelque chose par erreur

**Pas de panique !** Deux solutions :

1. **Restaurer depuis la sauvegarde**
   - Les fichiers sont dans `Documents/5GH'zCleaner-backups`
   - Copiez-les à leur emplacement d'origine

2. **Utiliser le point de restauration**
   - Tapez "Restauration" dans la recherche Windows
   - Sélectionnez "Créer un point de restauration"
   - Cliquez sur "Restauration du système"
   - Choisissez le point créé par 5GH'z Cleaner

## 💡 Conseils d'utilisation

### Pour de meilleurs résultats

1. **Utilisez la prévisualisation**
   - Voyez toujours ce qui sera supprimé avant de confirmer
   - Décochez ce que vous voulez garder

2. **Nettoyez régulièrement**
   - Une fois par semaine est idéal
   - Pas besoin de nettoyer tous les jours

3. **Optimisez votre disque**
   - Une fois par mois suffit
   - Le logiciel détecte automatiquement votre type de disque

4. **Surveillez les températures**
   - Si votre PC chauffe beaucoup, vérifiez les températures
   - CPU > 80°C = nettoyez la poussière de votre PC

### Ce qu'il ne faut PAS faire

❌ **Ne nettoyez pas trop souvent** - Une fois par semaine maximum
❌ **Ne décochez pas les protections** - Elles sont là pour votre sécurité
❌ **Ne fermez pas pendant un nettoyage** - Attendez toujours la fin
❌ **Ne supprimez pas les sauvegardes** - Elles peuvent vous sauver

### Besoin d'aide ?

- 🐛 **Vous avez trouvé un bug ?** Signalez-le sur [GitHub Issues](https://github.com/UndKiMi/5Ghz_Cleaner/issues)
- ❓ **Une question ?** Consultez d'abord cette documentation
- 💡 **Une idée d'amélioration ?** Partagez-la sur GitHub

## 📄 Licence et avertissement

### Licence

**Gratuit pour un usage personnel** - Licence CC BY-NC-SA 4.0

Vous pouvez :
- ✅ Utiliser gratuitement
- ✅ Partager avec vos amis
- ✅ Modifier le code

Vous ne pouvez pas :
- ❌ Vendre ce logiciel
- ❌ L'utiliser commercialement

### Avertissement important

⚠️ **Utilisez ce logiciel à vos propres risques**

Bien que 5GH'z Cleaner soit conçu pour être sûr :
- Un point de restauration est créé automatiquement
- Tous les fichiers sont sauvegardés avant suppression
- Les fichiers système sont protégés

**Mais** l'auteur ne peut être tenu responsable en cas de problème.

💡 **Conseil :** Utilisez toujours la prévisualisation avant de nettoyer !

---

<div align="center">

**5GH'z Cleaner v1.7.0** • Novembre 2025

Fait avec ❤️ pour les utilisateurs de Windows 11

[GitHub](https://github.com/UndKiMi/5Ghz_Cleaner) • [Signaler un bug](https://github.com/UndKiMi/5Ghz_Cleaner/issues) • [Licence](LICENSE)

</div>
