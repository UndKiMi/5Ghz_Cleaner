# 🛡️ FAQ Antivirus - 5GH'z Cleaner

## ❓ Questions Fréquentes sur la Sécurité

---

### Mon antivirus détecte 5GH'z Cleaner comme un virus. Est-ce dangereux ?

**Non, c'est un faux positif.** 5GH'z Cleaner est 100% sûr.

**Pourquoi cette détection ?**

Les outils d'optimisation système déclenchent souvent des faux positifs car ils utilisent des fonctionnalités similaires aux malwares :

- ✅ **Nettoyage de fichiers** → Ressemble à un ransomware
- ✅ **Demande de privilèges administrateur** → Ressemble à un trojan
- ✅ **Monitoring matériel** → Ressemble à un spyware
- ✅ **Modification du registre** → Ressemble à un rootkit

**Mais 5GH'z Cleaner est légitime :**

- ✅ Code source open-source sur GitHub
- ✅ Aucune télémétrie ou connexion internet
- ✅ Toutes les données restent locales
- ✅ Backup automatique avant toute modification
- ✅ Signé numériquement (si version signée)
- ✅ Checksums SHA-256 publics

---

### Comment vérifier que le fichier est authentique ?

**Méthode 1: Vérifier la signature numérique**

1. Clic droit sur `5Ghz_Cleaner.exe`
2. Propriétés > Onglet "Signatures numériques"
3. Vérifier que le signataire est **UndKiMi**
4. Statut doit être : **Cette signature numérique est correcte**

**Méthode 2: Vérifier le hash SHA-256**

```powershell
# Dans PowerShell
Get-FileHash 5Ghz_Cleaner.exe -Algorithm SHA256
```

Comparer avec le hash dans `CHECKSUMS.txt` (fourni avec chaque release).

**Méthode 3: Consulter le code source**

- GitHub: https://github.com/UndKiMi/5Ghz_Cleaner
- Licence: CC BY-NC-SA 4.0
- Tout le code est vérifiable

---

### Comment ajouter une exception dans mon antivirus ?

#### Windows Defender

1. Ouvrir **Windows Security** (Sécurité Windows)
2. **Protection contre les virus et menaces**
3. Gérer les paramètres
4. **Exclusions** > Ajouter ou supprimer des exclusions
5. Ajouter une exclusion > **Fichier**
6. Sélectionner `5Ghz_Cleaner.exe`

**Ou via PowerShell (admin) :**

```powershell
Add-MpPreference -ExclusionPath "C:\chemin\vers\5Ghz_Cleaner.exe"
```

#### Kaspersky

1. Ouvrir Kaspersky
2. **Paramètres** (icône engrenage)
3. **Menaces et exclusions**
4. **Gérer les exclusions** > Ajouter
5. Sélectionner le fichier

#### Bitdefender

1. Ouvrir Bitdefender
2. **Protection** > Paramètres
3. **Exclusions**
4. Ajouter une exclusion > Fichier
5. Sélectionner `5Ghz_Cleaner.exe`

#### Avira

1. Ouvrir Avira
2. **Sécurité** > Paramètres
3. **Exceptions**
4. Ajouter > Fichier
5. Sélectionner le fichier

#### Norton

1. Ouvrir Norton
2. **Paramètres** > Antivirus
3. **Analyses et risques** > Exclusions/Faibles risques
4. Configurer > Éléments à exclure
5. Ajouter le fichier

---

### Pourquoi le logiciel demande des privilèges administrateur ?

Certaines opérations nécessitent des privilèges élevés :

**Opérations nécessitant admin :**
- ✅ Nettoyage des fichiers système temporaires (`C:\Windows\Temp`)
- ✅ Vidage du cache DNS
- ✅ Optimisation des services Windows
- ✅ Création de point de restauration système
- ✅ Défragmentation/TRIM des disques
- ✅ Modification du registre Windows

**Sécurité :**
- ✅ Utilise UAC natif Windows (pas de bypass)
- ✅ Vous pouvez refuser et utiliser en mode limité
- ✅ Demande explicite avec raison claire
- ✅ Pas d'élévation silencieuse

**Mode sans admin :**
Si vous refusez les privilèges, le logiciel fonctionne en mode limité :
- ✅ Monitoring matériel (CPU, RAM, GPU, disques)
- ✅ Analyse de l'espace disque
- ✅ Nettoyage des fichiers utilisateur
- ❌ Pas de nettoyage système
- ❌ Pas d'optimisations avancées

---

### Le logiciel envoie-t-il des données sur internet ?

**Non, absolument aucune télémétrie.**

**Garanties :**
- ✅ **Aucune connexion internet** - Le logiciel ne se connecte jamais
- ✅ **Aucune télémétrie** - Pas de tracking, analytics, ou statistiques
- ✅ **100% local** - Toutes les données restent sur votre PC
- ✅ **Pas de compte** - Pas d'inscription ou login requis
- ✅ **Open source** - Code vérifiable sur GitHub

**Vérification :**
Vous pouvez vérifier avec un firewall ou Wireshark que le logiciel ne fait aucune connexion réseau.

---

### Quelles données le logiciel collecte-t-il ?

**Données lues (localement uniquement) :**
- ✅ Utilisation CPU, RAM, GPU (via WMI Windows)
- ✅ Températures matérielles (via LibreHardwareMonitor)
- ✅ Espace disque disponible
- ✅ Liste des fichiers temporaires
- ✅ Services Windows actifs

**Données stockées :**
- ✅ Logs locaux (dans `logs/` - optionnel)
- ✅ Configuration utilisateur (dans `config/`)
- ✅ Backups automatiques (dans `backups/` - avant modifications)

**Données envoyées :**
- ❌ **AUCUNE** - Rien n'est envoyé nulle part

---

### Le logiciel modifie-t-il des fichiers système critiques ?

**Non, jamais.**

**Protections en place :**

1. **Listes noires strictes** - Fichiers/dossiers interdits :
   - `C:\Windows\System32`
   - `C:\Windows\SysWOW64`
   - `C:\Program Files`
   - Tous les fichiers `.sys`, `.dll`, `.exe` système

2. **Validation quadruple couche** :
   - Vérification du chemin
   - Vérification de l'extension
   - Vérification du dossier parent
   - Vérification de la liste blanche

3. **Backup automatique** :
   - Avant toute suppression
   - Avant toute modification du registre
   - Rollback automatique si erreur

4. **Dossiers autorisés uniquement** :
   - `%TEMP%` (fichiers temporaires utilisateur)
   - `C:\Windows\Temp` (temporaires système - avec admin)
   - Corbeille
   - Cache navigateurs

**Fichiers JAMAIS touchés :**
- ❌ Fichiers système Windows
- ❌ Pilotes (`.sys`, `.inf`)
- ❌ DLLs système
- ❌ Registre critique
- ❌ Documents utilisateur
- ❌ Applications installées

---

### Comment désinstaller complètement le logiciel ?

**5GH'z Cleaner est portable** - pas d'installation requise.

**Pour supprimer :**

1. **Fermer l'application**
2. **Supprimer le fichier** `5Ghz_Cleaner.exe`
3. **Supprimer les données** (optionnel) :
   - `logs/` - Fichiers de log
   - `config/` - Configuration
   - `backups/` - Backups automatiques

**Aucune trace dans :**
- ❌ Registre Windows
- ❌ Program Files
- ❌ AppData
- ❌ Services Windows
- ❌ Démarrage automatique

---

### Puis-je utiliser le logiciel sur Windows 10 ?

**Non, Windows 11 uniquement.**

5GH'z Cleaner est spécifiquement conçu pour Windows 11 :
- ✅ Optimisé pour l'interface Windows 11
- ✅ Utilise les API Windows 11
- ✅ Testé uniquement sur Windows 11 (Build 22000+)

**Pourquoi pas Windows 10 ?**
- Différences dans les API système
- Différences dans la structure des fichiers
- Risque de compatibilité et bugs

---

### Le logiciel est-il gratuit ?

**Oui, 100% gratuit.**

**Licence :** CC BY-NC-SA 4.0

**Vous pouvez :**
- ✅ Utiliser gratuitement
- ✅ Modifier le code
- ✅ Partager avec d'autres
- ✅ Contribuer au projet

**Vous ne pouvez pas :**
- ❌ Vendre le logiciel
- ❌ Utilisation commerciale
- ❌ Retirer les crédits

---

### Comment signaler un faux positif aux éditeurs antivirus ?

**Microsoft Defender :**
https://www.microsoft.com/en-us/wdsi/filesubmission

**VirusTotal :**
1. Uploader le fichier : https://www.virustotal.com
2. Attendre les résultats
3. Cliquer sur chaque détection
4. "Report false positive" pour chaque éditeur

**Kaspersky :**
https://opentip.kaspersky.com

**Bitdefender :**
https://www.bitdefender.com/submit/

**Avira :**
https://www.avira.com/en/analysis/submit

**Norton :**
https://submit.norton.com

**Avast/AVG :**
https://www.avast.com/false-positive-file-form.php

---

### Combien de temps pour que les antivirus acceptent le logiciel ?

**Délais typiques :**

- **Microsoft Defender :** 1-3 jours après soumission
- **VirusTotal éditeurs :** 1-7 jours après signalement
- **SmartScreen (réputation) :** 1-2 semaines avec signature EV
- **Réputation complète :** 1-3 mois d'utilisation

**Facteurs accélérant :**
- ✅ Signature numérique valide (surtout EV)
- ✅ Soumissions multiples
- ✅ Nombre d'utilisateurs croissant
- ✅ Pas de modifications du fichier

---

### Le logiciel peut-il endommager mon PC ?

**Non, impossible.**

**Protections multiples :**

1. **Point de restauration automatique**
   - Créé avant toute opération
   - Permet de revenir en arrière

2. **Backup automatique**
   - Avant toute suppression
   - Avant toute modification

3. **Validation stricte**
   - 4 couches de vérification
   - Listes blanches/noires

4. **Mode lecture seule**
   - Monitoring sans modification
   - Analyse sans danger

5. **Rollback automatique**
   - Si erreur détectée
   - Restauration immédiate

**Pire scénario possible :**
- Suppression de fichiers temporaires → Aucun impact
- Erreur d'optimisation → Rollback automatique
- Bug logiciel → Point de restauration disponible

---

### Où trouver de l'aide ?

**Documentation :**
- README.md - Guide complet
- ANTIVIRUS_OPTIMIZATION_REPORT.md - Détails techniques
- GitHub Wiki - Tutoriels

**Support :**
- GitHub Issues : https://github.com/UndKiMi/5Ghz_Cleaner/issues
- Discussions : https://github.com/UndKiMi/5Ghz_Cleaner/discussions

**Contribuer :**
- Code source : https://github.com/UndKiMi/5Ghz_Cleaner
- Pull Requests bienvenues
- Licence : CC BY-NC-SA 4.0

---

## 🔒 Garanties de Sécurité

**5GH'z Cleaner garantit :**

1. ✅ **Aucune télémétrie** - 0 connexion internet
2. ✅ **Code open-source** - 100% vérifiable
3. ✅ **Backup automatique** - Avant toute modification
4. ✅ **Validation stricte** - 4 couches de sécurité
5. ✅ **API natives Windows** - Pas de drivers suspects
6. ✅ **Signature numérique** - Certificat valide (si signé)
7. ✅ **Checksums publics** - Vérification d'intégrité
8. ✅ **Licence libre** - CC BY-NC-SA 4.0

---

## 📞 Contact

**Problème persistant ?**

1. Vérifier la documentation complète
2. Chercher dans les Issues GitHub
3. Créer une nouvelle Issue avec détails
4. Joindre les logs (si applicable)

**Faux positif non résolu ?**

1. Vérifier que vous avez la dernière version
2. Vérifier la signature numérique
3. Soumettre aux éditeurs antivirus
4. Signaler sur GitHub

---

**Dernière mise à jour :** 2025-01-02  
**Version :** 1.7.0  
**Auteur :** UndKiMi  
**Licence :** CC BY-NC-SA 4.0
