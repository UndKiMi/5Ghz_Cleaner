# 🔐 Confidentialité - 5GH'z Cleaner

## 📋 Notre Engagement

**Votre vie privée est sacrée. Aucune donnée n'est collectée, jamais.**

**5GH'z Cleaner** est conçu avec un principe simple: **zéro télémétrie, zéro collecte, zéro tracking**.

## 🚫 Ce Que Nous NE Collectons PAS

**Absolument RIEN.** Voici ce qui n'est jamais collecté:

- 🚫 **Aucune donnée personnelle** - Nom, email, adresse, etc.
- 🚫 **Aucune donnée d'utilisation** - Ce que vous nettoyez, quand, comment
- 🚫 **Aucune donnée système** - Configuration PC, logiciels installés
- 🚫 **Aucune connexion Internet** - L'application fonctionne 100% en local
- 🚫 **Aucun tracking** - Pas de cookies, analytics ou suivi
- 🚫 **Aucun identifiant** - Pas d'ID unique, pas de fingerprinting

## ✅ Comment Vérifier Par Vous-Même ?

**Transparence totale**: Vous pouvez vérifier l'absence de télémétrie vous-même.

### Méthode 1: Outil de Vérification Intégré

```bash
python backend/telemetry_checker.py
```

Vous verrez:
```
✓ STATUT: CONFORME - Aucune télémétrie détectée
✓ Aucune connexion réseau active
✓ Aucune donnée collectée
```

### Méthode 2: Consultez le Code Source

Le code est 100% open source sur GitHub. Vous pouvez:
- Lire chaque ligne de code
- Chercher "requests", "urllib", "socket" (aucune occurrence)
- Vérifier qu'il n'y a aucune connexion réseau

## 📊 Informations Affichées (Onglet Configuration)

**Question**: Si l'application affiche des informations sur mon PC (CPU, RAM, GPU), sont-elles envoyées quelque part ?

**Réponse**: **NON, absolument pas.**

**Comment ça fonctionne**:
1. ✅ Les informations sont lues **localement** sur votre PC
2. ✅ Elles sont **affichées uniquement** dans l'interface
3. ✅ Elles sont **JAMAIS envoyées** à Internet
4. ✅ Elles sont **JAMAIS stockées** dans des fichiers
5. ✅ Elles **disparaissent** quand vous fermez l'application

**Analogie**: C'est comme regarder la température sur un thermomètre - vous la voyez, mais personne d'autre ne la voit.

## 🔐 Sécurité de Vos Données

**Principe simple**: Vos données restent sur votre PC, point.

- ✅ **100% local** - Tout fonctionne sur votre ordinateur
- ✅ **Aucune connexion Internet** - Pas besoin de réseau
- ✅ **Code source ouvert** - Vérifiable par tous
- ✅ **Pas de dépendances suspectes** - Uniquement des bibliothèques officielles

## 📝 Logs - Stockés Localement

**Les logs de nettoyage sont-ils envoyés quelque part ?**

**NON.** Les logs sont:
- ✅ **Stockés localement** dans `Documents/5GH'zCleaner-logs/`
- ✅ **Jamais envoyés** à Internet
- ✅ **Visibles uniquement par vous**
- ✅ **Supprimables** quand vous voulez

**Pourquoi des logs ?** Pour que vous puissiez vérifier ce qui a été nettoyé et quand.

## ⚖️ Conformité Légale

**5GH'z Cleaner est conforme à**:
- ✅ **RGPD** (Europe) - Aucune donnée personnelle traitée
- ✅ **CCPA** (Californie) - Aucune donnée collectée
- ✅ **Toutes les lois sur la vie privée** - Zéro collecte = zéro risque

## 🔍 Transparence Totale

**Vous ne devez pas nous croire sur parole. Vérifiez !**

- ✅ **Code source complet** sur [GitHub](https://github.com/UndKiMi/5Ghz_Cleaner)
- ✅ **Aucun code caché** - Tout est visible
- ✅ **Aucune obfuscation** - Code lisible et commenté
- ✅ **Licence open source** - CC BY-NC-SA 4.0

## ❓ Questions Fréquentes

**Q: Pourquoi devrais-je vous faire confiance ?**
R: Vous ne devez pas ! Vérifiez le code source, lancez le vérificateur de télémétrie, ou utilisez un moniteur réseau pour voir qu'il n'y a aucune connexion.

**Q: Mes données sont-elles vendues à des tiers ?**
R: Impossible - nous n'avons aucune donnée à vendre. Zéro collecte = zéro vente.

**Q: L'application peut-elle changer et commencer à collecter des données ?**
R: Le code est open source. Toute modification serait visible immédiatement. De plus, le vérificateur de télémétrie détecterait tout changement.

**Q: Pourquoi ne pas avoir de télémétrie "anonyme" pour améliorer le logiciel ?**
R: Parce que votre vie privée est plus importante. Nous préférons améliorer le logiciel via les retours volontaires des utilisateurs.

---

<div align="center">

**5GH'z Cleaner** - Votre Vie Privée, Notre Priorité

**Engagement**: Zéro télémétrie, toujours.

[Retour au README](README.md) • [Sécurité](SECURITY.md) • [Guide de Démarrage](QUICK_START.md)

</div>
