# Politique de Confidentialité - 5GH'z Cleaner

## 🔒 Engagement de Confidentialité

**5GH'z Cleaner** est conçu avec la confidentialité comme priorité absolue.

### ✅ Garanties de Confidentialité

1. **AUCUNE TÉLÉMÉTRIE**
   - Aucune donnée n'est collectée
   - Aucune connexion réseau n'est établie
   - Aucune information n'est envoyée à des serveurs externes

2. **AUCUNE COLLECTE DE DONNÉES**
   - Aucun historique de navigation
   - Aucune adresse IP
   - Aucun identifiant unique
   - Aucune donnée personnelle

3. **AUCUN TRACKING**
   - Pas de cookies
   - Pas d'analytics
   - Pas de suivi comportemental
   - Pas de fingerprinting

### 🛡️ Vérification de Conformité

L'application inclut un module de vérification de télémétrie (`backend/telemetry_checker.py`) qui peut être exécuté à tout moment pour confirmer:

```bash
python -m backend.telemetry_checker
```

Ce module vérifie:
- ✓ Absence de connexions réseau actives
- ✓ Absence de requêtes externes
- ✓ Absence de fichiers de collecte de données

### 📊 Monitoring Matériel (Onglet Configuration)

L'onglet "Configuration" affiche les informations matérielles de votre système:
- CPU (température, utilisation, fréquence)
- RAM (utilisation, mémoire disponible)
- GPU (nom, température si disponible)
- Disques (utilisation, espace libre)

**IMPORTANT**: Toutes ces données sont:
- ✅ Collectées localement sur votre machine
- ✅ Affichées uniquement dans l'interface
- ✅ JAMAIS envoyées à des serveurs externes
- ✅ JAMAIS stockées dans des fichiers
- ✅ Supprimées à la fermeture de l'application

### 🔐 Sécurité des Données

- Toutes les opérations sont effectuées localement
- Aucune connexion Internet n'est requise
- Le code source est open-source et vérifiable
- Aucune dépendance suspecte

### 📝 Logs et Journaux

Les logs affichés dans la console sont:
- Uniquement pour le débogage local
- Jamais envoyés à des serveurs
- Jamais stockés de manière permanente
- Visibles uniquement par l'utilisateur

### ⚖️ Conformité

Cette application est conforme aux réglementations:
- RGPD (Règlement Général sur la Protection des Données)
- CCPA (California Consumer Privacy Act)
- Aucune donnée personnelle n'est traitée

### 🔍 Transparence

Le code source complet est disponible et peut être audité:
- Tous les modules sont documentés
- Aucun code obfusqué
- Aucune dépendance cachée
- Licence open-source CC BY-NC-SA 4.0

### 📞 Contact

Pour toute question concernant la confidentialité:
- GitHub: https://github.com/UndKiMi
- Vérifiez le code source vous-même

---

**Dernière mise à jour**: 2025-01-12  
**Version**: 1.6.0

**Engagement**: Aucune donnée utilisateur ne sera jamais collectée, stockée ou transmise sans consentement explicite.
