# 🚀 Guide de Démarrage Rapide

**Commencez à utiliser 5GH'z Cleaner en 5 minutes.**

Ce guide vous explique comment installer et utiliser le logiciel pour la première fois.

---

## ⚡ Installation (2 minutes)

### Option 1: Télécharger l'Exécutable (Recommandé)

**Étape 1**: Téléchargez la dernière version
- Allez sur [Releases](https://github.com/UndKiMi/5Ghz_Cleaner/releases)
- Téléchargez `5Ghz_Cleaner.exe`

**Étape 2**: Vérifiez l'intégrité (optionnel mais recommandé)
```powershell
Get-FileHash "5Ghz_Cleaner.exe" -Algorithm SHA256
# Comparez avec le fichier CHECKSUMS.txt
```

**Étape 3**: Lancez l'application
- Double-cliquez sur `5Ghz_Cleaner.exe`
- Si Windows SmartScreen s'affiche: "Plus d'infos" → "Exécuter quand même"

### Option 2: Depuis le Code Source

**Prérequis**: Python 3.11 ou supérieur installé

**Étape 1**: Téléchargez le code
```bash
git clone https://github.com/UndKiMi/5Ghz_Cleaner.git
cd 5Ghz_Cleaner
```

**Étape 2**: Installez les dépendances
```bash
pip install -r requirements.txt
```

**Étape 3**: Lancez l'application
```bash
python main.py
```

---

## 🎯 Première Utilisation (3 minutes)

### 📌 Étape 1: Lancez l'Application

- Double-cliquez sur `5Ghz_Cleaner.exe`
- Ou exécutez `python main.py` si vous utilisez le code source

### 📋 Étape 2: Sélectionnez Ce Que Vous Voulez Nettoyer

**Onglet "Nettoyage Rapide"**:
- ☑️ Cochez les options souhaitées (fichiers temporaires, cache, etc.)
- ❓ Survolez les icônes "ℹ️" pour voir les descriptions

**Onglet "Options Avancées"** (optionnel):
- Options plus techniques (RAM, DNS, télémétrie, etc.)

### 🔍 Étape 3: Prévisualisez (OBLIGATOIRE)

1. **Cliquez** sur le bouton "🔍 Prévisualiser" (Dry-Run)
2. **Attendez** l'analyse (aucune suppression réelle)
3. **Lisez** la liste des fichiers qui seront supprimés
4. **Vérifiez** que tout est OK

> 💡 **Important**: Le bouton "Nettoyer" ne se débloque qu'après la prévisualisation.

### 🧹 Étape 4: Nettoyez

1. **Cliquez** sur "🧹 Nettoyer"
2. **Confirmez** si demandé (Windows.old, Corbeille)
3. **Attendez** la fin du nettoyage
4. **Consultez** le résumé (espace libéré, fichiers supprimés)

✅ **Terminé !** Votre PC est nettoyé.

---

## ✅ Checklist de Sécurité

### 👉 Avant le Nettoyage

- ✅ **Point de restauration** - Créé automatiquement par le logiciel
- ✅ **Prévisualisation** - Toujours obligatoire
- ✅ **Sauvegarde** - Recommandé pour vos fichiers importants

### ⏳ Pendant le Nettoyage

- ⚠️ **Ne fermez pas** l'application
- ⚠️ **N'éteignez pas** votre PC
- ✅ **Attendez** la fin complète

### ✓ Après le Nettoyage

- ✅ **Vérifiez** que tout fonctionne normalement
- ✅ **Consultez les logs** si besoin (`Documents/5GH'zCleaner-logs/`)
- ✅ **Redémarrez** votre PC si recommandé

---

## 🔒 Ce Qui Est Protégé

### ❌ Impossible à Supprimer (Protégé)

**Votre système est protégé**. Ces éléments ne seront JAMAIS supprimés:

- ❌ **Windows** - Tous les fichiers système (200+ chemins)
- ❌ **Vos applications** - Office, navigateurs, antivirus, etc.
- ❌ **Vos drivers** - GPU (NVIDIA, AMD, Intel), audio, etc.
- ❌ **Services critiques** - 12 services Windows essentiels

### ✅ Ce Qui Peut Être Nettoyé

**Uniquement ce qui est sûr à supprimer**:

- ✅ **Fichiers temporaires** - Cache Windows et applications
- ✅ **Cache navigateurs** - Si vous le sélectionnez
- ✅ **Corbeille** - Avec confirmation
- ✅ **Windows.old** - Ancienne installation (avec confirmation)

---

## 🧪 Vérifier la Sécurité (Optionnel)

**Vous voulez vérifier que le logiciel est sûr ?**

```bash
# Vérifier l'absence de télémétrie
python backend/telemetry_checker.py

# Lancer tous les tests de sécurité
python tests/test_all_security.py
```

**Résultat attendu**: Tous les tests passent ✅

---

## 📊 Onglet Configuration (Optionnel)

**Voir l'état de votre PC en temps réel**:

1. Cliquez sur l'onglet "⚙️ Configuration"
2. Consultez: CPU, RAM, GPU, Disques
3. Code couleur:
   - 🟢 **Vert**: Tout va bien
   - 🟡 **Jaune**: Attention
   - 🔴 **Rouge**: Problème

> 🔒 **Confidentialité**: Ces informations sont affichées uniquement sur votre écran, jamais envoyées à Internet.

---

## ❓ Problèmes Courants

### ⚠️ "Windows a protégé votre PC"

**Pourquoi ?** Le logiciel n'a pas de certificat Microsoft officiel (coût: 500€/an).

**Solution**:
1. Cliquez sur "Plus d'infos"
2. Cliquez sur "Exécuter quand même"
3. (Optionnel) Vérifiez le checksum SHA256 pour confirmer l'authenticité

### 🚫 "Accès refusé"

**Pourquoi ?** Certaines opérations nécessitent les droits administrateur.

**Solution**:
- Clic droit sur `5Ghz_Cleaner.exe`
- Sélectionnez "Exécuter en tant qu'administrateur"

### 📦 "Module non trouvé" (Code source uniquement)

**Pourquoi ?** Les dépendances Python ne sont pas installées.

**Solution**:
```bash
pip install -r requirements.txt
```

### ❓ Autre Problème ?

- Consultez la [FAQ dans le README](README.md#-questions-fréquentes-faq)
- Ouvrez une [issue sur GitHub](https://github.com/UndKiMi/5Ghz_Cleaner/issues)

---

## 📚 Pour Aller Plus Loin

| Document | Description | Temps |
|----------|-------------|-------|
| **[README.md](README.md)** | Vue d'ensemble complète | 10 min |
| **[SECURITY.md](SECURITY.md)** | Détails sur la sécurité | 15 min |
| **[PRIVACY.md](PRIVACY.md)** | Politique de confidentialité | 3 min |
| **[INSTALLATION.md](INSTALLATION.md)** | Guide d'installation détaillé | 5 min |

---

## 🔧 Commandes Utiles

### Vérifier la Sécurité

```bash
# Vérifier l'absence de télémétrie
python backend/telemetry_checker.py

# Vérifier l'intégrité des fichiers
python backend/signature_manager.py --verify
```

### Lancer les Tests

```bash
# Tous les tests (45 tests)
python tests/run_all_tests.py

# Uniquement les tests de sécurité (7 tests)
python tests/test_all_security.py
```

---

## 💡 Conseils d'Utilisation

### 1️⃣ Toujours Prévisualiser

- ❌ **JAMAIS** nettoyer sans prévisualisation
- ✅ **TOUJOURS** vérifier ce qui sera supprimé
- 💡 C'est obligatoire de toute façon !

### 2️⃣ Consultez les Logs

**Où ?** `C:\Users\<VotreNom>\Documents\5GH'zCleaner-logs/`

**Pourquoi ?** Pour voir exactement ce qui a été nettoyé et quand.

### 3️⃣ Point de Restauration Automatique

- ✅ Créé automatiquement avant chaque nettoyage
- ✅ Permet de restaurer Windows si problème
- ✅ Sécurité maximale

### 4️⃣ Nettoyez Régulièrement

- 📅 **Recommandé**: Une fois par mois
- 💾 **Résultat**: PC plus rapide, plus d'espace disque

---

## 🔗 Liens Utiles

- 🏠 **[Page GitHub](https://github.com/UndKiMi/5Ghz_Cleaner)** - Code source
- 📥 **[Téléchargements](https://github.com/UndKiMi/5Ghz_Cleaner/releases)** - Dernière version
- 🐛 **[Signaler un bug](https://github.com/UndKiMi/5Ghz_Cleaner/issues)** - Issues GitHub

---

## ⏱️ Résumé Ultra-Rapide

**En 4 étapes simples**:

1. 📥 **Téléchargez** `5Ghz_Cleaner.exe`
2. ▶️ **Lancez** l'application
3. 🔍 **Prévisualisez** ce qui sera supprimé
4. 🧹 **Nettoyez** en un clic

✅ **Terminé !** Votre PC est nettoyé.

---

**⏱️ Temps total**: 5 minutes  
**🎯 Difficulté**: Facile  
**💻 Compatibilité**: Windows 11 (64-bit) uniquement

> ⚠️ **Important**: Non compatible avec Windows 10 ou versions antérieures.

---

<div align="center">

**Besoin d'aide ?**

[README Complet](README.md) • [FAQ](README.md#-questions-fréquentes-faq) • [Signaler un Bug](https://github.com/UndKiMi/5Ghz_Cleaner/issues)

**5GH'z Cleaner** - Nettoyage Simple et Sécurisé

</div>  
