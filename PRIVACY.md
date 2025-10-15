# 🔐 Politique de Confidentialité - 5GH'z Cleaner

## 📋 Engagement Absolu

**5GH'z Cleaner ne collecte, ne stocke et ne transmet AUCUNE donnée utilisateur.**

---

## ✅ Ce que nous NE faisons PAS

### Aucune Collecte de Données
- ❌ **Aucune télémétrie** - Pas de tracking, analytics ou statistiques
- ❌ **Aucune connexion Internet** - Tout fonctionne 100% en local
- ❌ **Aucun cookie** - Pas de suivi comportemental
- ❌ **Aucun identifiant** - Pas de UUID, fingerprint ou tracking ID
- ❌ **Aucune donnée personnelle** - Nom, email, IP, localisation, etc.

### Aucune Transmission
- ❌ **Aucun serveur distant** - Pas de communication externe
- ❌ **Aucune API tierce** - Pas d'appels à des services externes
- ❌ **Aucun rapport d'erreur** - Pas de crash reports automatiques
- ❌ **Aucune mise à jour automatique** - Pas de vérification de version en ligne

### Aucun Stockage Cloud
- ❌ **Aucun compte utilisateur** - Pas d'inscription ou login
- ❌ **Aucun stockage distant** - Tout reste sur votre machine
- ❌ **Aucune synchronisation** - Pas de sync entre appareils

---

## ✅ Ce que nous faisons

### Logs Locaux (Optionnels)
- ✅ **Stockage local uniquement** - `C:\Users\<Vous>\Documents\5GH'zCleaner-logs\`
- ✅ **Anonymisation automatique** - Chemins utilisateur remplacés par [USER]
- ✅ **Chiffrement optionnel** - AES-256 si vous installez `cryptography`
- ✅ **Auto-nettoyage** - Suppression automatique après 30 jours
- ✅ **Vous contrôlez** - Vous pouvez supprimer les logs à tout moment

### Données Traitées Localement
- ✅ **Liste des fichiers** - Scannés localement pour le nettoyage
- ✅ **Informations système** - CPU, RAM, température (affichage uniquement)
- ✅ **Historique de nettoyage** - Stocké dans les logs locaux

**IMPORTANT:** Toutes ces données restent sur votre machine et ne sont jamais transmises.

---

## 🔍 Vérification

### Comment Vérifier l'Absence de Télémétrie

Nous fournissons un outil de vérification automatique:

```bash
python backend/telemetry_checker.py
```

Cet outil scanne tout le code source et vérifie:
- ✅ Aucune connexion réseau
- ✅ Aucun appel HTTP/HTTPS
- ✅ Aucune API de tracking
- ✅ Aucun service de télémétrie

### Audit du Code Source

Le code source est **100% ouvert** et auditable:
- 📖 **GitHub:** https://github.com/UndKiMi/5Ghz_Cleaner
- 🔍 **Tous les fichiers** sont visibles et commentés
- ✅ **Aucun code obfusqué** - Tout est lisible

### Outils de Vérification Réseau

Vous pouvez vérifier vous-même avec des outils comme:
- **Wireshark** - Moniteur réseau
- **Process Monitor** - Moniteur d'activité
- **Windows Firewall** - Bloquez l'application et vérifiez qu'elle fonctionne

**Résultat attendu:** Aucune connexion réseau détectée.

---

## 🛡️ Conformité RGPD

### Article 5 - Principes
- ✅ **Minimisation des données** - Aucune donnée collectée
- ✅ **Limitation de la finalité** - Nettoyage local uniquement
- ✅ **Exactitude** - Pas de données à maintenir
- ✅ **Limitation de la conservation** - Logs auto-supprimés après 30 jours
- ✅ **Intégrité et confidentialité** - Chiffrement optionnel

### Article 6 - Licéité du traitement
- ✅ **Pas de traitement** - Aucune donnée personnelle traitée

### Article 7 - Consentement
- ✅ **Pas de consentement nécessaire** - Aucune collecte de données

### Article 15-22 - Droits des personnes
- ✅ **Droit d'accès** - Vous avez accès à tous vos logs locaux
- ✅ **Droit de rectification** - Vous pouvez modifier vos logs
- ✅ **Droit à l'effacement** - Vous pouvez supprimer vos logs
- ✅ **Droit à la portabilité** - Vos logs sont en format texte lisible

---

## 🔒 Sécurité des Données

### Données Locales
- ✅ **Stockage local** - Jamais transmises
- ✅ **Anonymisation** - Chemins utilisateur masqués
- ✅ **Chiffrement optionnel** - AES-256 disponible
- ✅ **Permissions Windows** - Protégées par le système

### Pas de Fuite de Données
- ✅ **Aucune connexion réseau** - Impossible de transmettre
- ✅ **Aucun service tiers** - Pas de risque de fuite
- ✅ **Code auditable** - Vérifiable par tous

---

## 📞 Contact

### Questions sur la Confidentialité

Si vous avez des questions sur notre politique de confidentialité:
1. **Lisez le code source** - Tout est transparent
2. **Utilisez le vérificateur** - `python backend/telemetry_checker.py`
3. **Ouvrez une issue** - [GitHub Issues](https://github.com/UndKiMi/5Ghz_Cleaner/issues)

### Signaler une Violation

Si vous découvrez une collecte de données non documentée:
1. **Ouvrez une issue de sécurité** - [Security Issues](https://github.com/UndKiMi/5Ghz_Cleaner/security)
2. **Fournissez des preuves** - Logs réseau, code source, etc.
3. **Nous corrigerons immédiatement** - Engagement de transparence

---

## 📜 Historique des Modifications

### MAJOR UPDATE (2025-10-15)
- ✅ Ajout anonymisation automatique des logs
- ✅ Ajout chiffrement optionnel AES-256
- ✅ Ajout auto-nettoyage des logs (30 jours)
- ✅ Aucune nouvelle collecte de données

### Version Initiale
- ✅ Aucune télémétrie
- ✅ Aucune connexion réseau
- ✅ 100% local

---

## ✅ Résumé

| Critère | Status |
|---------|--------|
| **Collecte de données** | ❌ Aucune |
| **Connexion Internet** | ❌ Aucune |
| **Télémétrie** | ❌ Aucune |
| **Cookies** | ❌ Aucun |
| **Tracking** | ❌ Aucun |
| **Stockage cloud** | ❌ Aucun |
| **Logs locaux** | ✅ Optionnels, anonymisés |
| **Chiffrement** | ✅ Optionnel (AES-256) |
| **Code open source** | ✅ 100% auditable |
| **Conformité RGPD** | ✅ Complète |

---

**5GH'z Cleaner respecte totalement votre vie privée.**

**Aucune donnée n'est jamais collectée, stockée ou transmise.**

**Vérifiable. Auditable. Transparent.**

---

**Dernière mise à jour:** 2025-10-15  
**Version:** MAJOR UPDATE  
**Auteur:** UndKiMi  
**Licence:** CC BY-NC-SA 4.0
