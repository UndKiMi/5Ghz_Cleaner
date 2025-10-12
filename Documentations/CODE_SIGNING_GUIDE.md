# 📜 Guide Complet - Certificat Code Signing

## 📋 Vue d'ensemble

Ce document explique comment obtenir un **certificat code signing officiel** pour signer 5GH'z Cleaner et éviter les avertissements Windows SmartScreen.

**Version**: MAJOR UPDATE  
**Auteur**: UndKiMi

---

## 🎯 Pourquoi un Certificat Code Signing?

### Problème Actuel
- ❌ Windows SmartScreen bloque les exécutables non signés
- ❌ Message "Windows a protégé votre PC"
- ❌ Utilisateurs doivent cliquer "Plus d'infos" puis "Exécuter quand même"
- ❌ Perte de confiance des utilisateurs

### Avec un Certificat Officiel
- ✅ Pas d'avertissement SmartScreen
- ✅ Confiance immédiate des utilisateurs
- ✅ Vérification de l'authenticité
- ✅ Protection contre la modification
- ✅ Timestamp garantit la validité même après expiration

---

## 💰 Coût et Fournisseurs

### Certificats Standard (OV - Organization Validation)
**Coût**: 200-400€/an

| Fournisseur | Prix/an | Délai | Réputation |
|-------------|---------|-------|------------|
| **DigiCert** | 400€ | 1-3 jours | ⭐⭐⭐⭐⭐ |
| **Sectigo** | 200€ | 1-2 jours | ⭐⭐⭐⭐ |
| **GlobalSign** | 300€ | 2-3 jours | ⭐⭐⭐⭐ |
| **Comodo** | 180€ | 1-2 jours | ⭐⭐⭐ |

### Certificats EV (Extended Validation)
**Coût**: 400-800€/an

| Fournisseur | Prix/an | Délai | Avantages |
|-------------|---------|-------|-----------|
| **DigiCert EV** | 800€ | 5-7 jours | Réputation immédiate SmartScreen |
| **Sectigo EV** | 500€ | 5-7 jours | Bon rapport qualité/prix |
| **GlobalSign EV** | 600€ | 5-7 jours | Support excellent |

**Recommandation**: **Sectigo EV** (500€/an) - Meilleur rapport qualité/prix

---

## 📝 Processus d'Obtention

### Étape 1: Choisir le Type de Certificat

**Pour 5GH'z Cleaner, nous recommandons:**
- **Certificat EV (Extended Validation)** - 500€/an
- **Raison**: Réputation SmartScreen immédiate
- **Alternative**: Certificat OV (200€/an) si budget limité

### Étape 2: Préparer les Documents

#### Pour un Certificat OV (Individual)
- ✅ Pièce d'identité valide (passeport, carte d'identité)
- ✅ Justificatif de domicile (< 3 mois)
- ✅ Numéro de téléphone vérifiable

#### Pour un Certificat EV (Organization)
- ✅ Documents d'entreprise (KBIS, statuts)
- ✅ Numéro SIRET/SIREN
- ✅ Pièce d'identité du représentant légal
- ✅ Justificatif de domicile de l'entreprise
- ✅ Numéro de téléphone professionnel

### Étape 3: Commander le Certificat

**Exemple avec Sectigo EV:**

1. **Aller sur**: https://sectigo.com/ssl-certificates-tls/code-signing
2. **Sélectionner**: "EV Code Signing Certificate"
3. **Remplir le formulaire**:
   - Nom de l'organisation: "UndKiMi" ou votre entreprise
   - Pays: France
   - Email de contact
   - Informations de facturation

4. **Payer**: 500€/an (carte bancaire, PayPal, virement)

5. **Validation**:
   - Sectigo vous contacte par téléphone
   - Vérification des documents (2-5 jours)
   - Appel de confirmation

6. **Réception**:
   - Certificat envoyé par email
   - Format: `.pfx` ou `.p12`
   - Mot de passe fourni séparément

### Étape 4: Installer le Certificat

**Sur Windows:**

```powershell
# Importer le certificat dans le magasin personnel
Import-PfxCertificate -FilePath ".\certificate.pfx" -CertStoreLocation "Cert:\CurrentUser\My" -Password (ConvertTo-SecureString -String "VotreMotDePasse" -AsPlainText -Force)
```

**Vérifier l'installation:**

```powershell
# Lister les certificats code signing
Get-ChildItem -Path "Cert:\CurrentUser\My" -CodeSigningCert
```

### Étape 5: Signer l'Exécutable

**Avec signtool (Windows SDK):**

```powershell
# Télécharger Windows SDK: https://developer.microsoft.com/windows/downloads/windows-sdk/

# Signer l'exécutable
signtool sign /f "certificate.pfx" /p "MotDePasse" /tr http://timestamp.sectigo.com /td SHA256 /fd SHA256 "5Ghz_Cleaner.exe"
```

**Vérifier la signature:**

```powershell
# Vérifier
signtool verify /pa /v "5Ghz_Cleaner.exe"

# Afficher les détails
Get-AuthenticodeSignature "5Ghz_Cleaner.exe" | Format-List *
```

---

## 🔧 Solution Temporaire: Certificat Auto-Signé

**Pour le développement uniquement:**

### Créer un Certificat Auto-Signé

```powershell
# Exécuter le script fourni
.\scripts\create_self_signed_cert.ps1
```

**Ce script crée:**
- ✅ Certificat auto-signé valide 5 ans
- ✅ Clé privée protégée par mot de passe
- ✅ Installation automatique dans Trusted Root

### Signer avec le Certificat Auto-Signé

```powershell
# Signer l'exécutable
.\scripts\sign_executable.ps1 -FilePath "dist\5Ghz_Cleaner.exe"
```

### ⚠️ Limitations du Certificat Auto-Signé

- ❌ **Windows SmartScreen affichera toujours un avertissement**
- ❌ **Pas de confiance automatique**
- ❌ **Utilisateurs doivent installer manuellement le certificat**
- ❌ **Pas adapté pour la distribution publique**

**Utilisation recommandée:**
- ✅ Tests en interne
- ✅ Développement
- ✅ Démonstrations privées

---

## 📊 Comparaison des Options

| Aspect | Auto-Signé | OV Standard | EV (Recommandé) |
|--------|------------|-------------|-----------------|
| **Coût** | Gratuit | 200€/an | 500€/an |
| **SmartScreen** | ❌ Avertissement | ⚠️ Réputation progressive | ✅ Immédiat |
| **Confiance** | ❌ Faible | ⚠️ Moyenne | ✅ Élevée |
| **Validation** | Aucune | Email + Téléphone | Documents + Appel |
| **Délai** | Immédiat | 1-2 jours | 5-7 jours |
| **Durée** | 5 ans | 1-3 ans | 1-3 ans |
| **Usage** | Développement | Production | Production Pro |

---

## 🎯 Recommandation pour 5GH'z Cleaner

### Option 1: Budget Disponible (500€/an)
**Certificat EV Sectigo** - 500€/an
- ✅ Réputation SmartScreen immédiate
- ✅ Confiance maximale des utilisateurs
- ✅ Pas d'avertissements
- ✅ Professionnel

**ROI**: Si 100+ téléchargements/mois, le coût est justifié

### Option 2: Budget Limité (200€/an)
**Certificat OV Sectigo** - 200€/an
- ⚠️ Réputation SmartScreen progressive (2-3 mois)
- ✅ Signature valide
- ✅ Moins cher
- ⚠️ Avertissements initiaux

**ROI**: Bon compromis pour démarrer

### Option 3: Gratuit (Développement)
**Certificat Auto-Signé** - Gratuit
- ❌ Avertissements permanents
- ✅ Gratuit
- ✅ Bon pour tests
- ❌ Pas pour distribution publique

---

## 📅 Timeline Recommandée

### Phase 1: Développement (Actuel)
- ✅ Utiliser certificat auto-signé
- ✅ Tests internes
- ✅ Validation fonctionnelle

### Phase 2: Beta Publique (1-2 mois)
- 🎯 Obtenir certificat OV (200€/an)
- 🎯 Distribution limitée
- 🎯 Collecter feedback

### Phase 3: Production (3-6 mois)
- 🎯 Upgrade vers certificat EV (500€/an)
- 🎯 Distribution large
- 🎯 Réputation SmartScreen établie

---

## 🔗 Liens Utiles

### Fournisseurs de Certificats
- **Sectigo**: https://sectigo.com/ssl-certificates-tls/code-signing
- **DigiCert**: https://www.digicert.com/signing/code-signing-certificates
- **GlobalSign**: https://www.globalsign.com/en/code-signing-certificate

### Documentation Microsoft
- **Code Signing Best Practices**: https://docs.microsoft.com/en-us/windows-hardware/drivers/install/authenticode
- **Windows SDK**: https://developer.microsoft.com/windows/downloads/windows-sdk/
- **SmartScreen**: https://docs.microsoft.com/en-us/windows/security/threat-protection/microsoft-defender-smartscreen/

### Outils
- **signtool.exe**: Inclus dans Windows SDK
- **OpenSSL**: https://www.openssl.org/ (alternative)

---

## ❓ FAQ

### Q: Puis-je utiliser un certificat SSL pour signer du code?
**R**: Non, vous avez besoin d'un certificat **Code Signing** spécifique.

### Q: Le certificat fonctionne sur macOS et Linux?
**R**: Non, les certificats Code Signing Windows sont spécifiques à Windows. Pour macOS, utilisez un certificat Apple Developer.

### Q: Que se passe-t-il si le certificat expire?
**R**: Si vous avez utilisé un **timestamp**, la signature reste valide même après expiration. Sans timestamp, la signature devient invalide.

### Q: Puis-je partager mon certificat?
**R**: ❌ **NON!** Le certificat et sa clé privée doivent rester **strictement confidentiels**. Ne jamais les partager ou les commiter sur Git.

### Q: Combien de temps pour la réputation SmartScreen?
**R**: 
- **EV**: Immédiat
- **OV**: 2-3 mois avec 1000+ téléchargements
- **Auto-signé**: Jamais

---

## 🔐 Sécurité du Certificat

### Bonnes Pratiques

1. **Stockage Sécurisé**
   - ✅ Stocker le `.pfx` dans un coffre-fort de mots de passe
   - ✅ Utiliser un mot de passe fort (20+ caractères)
   - ✅ Sauvegarder dans un endroit sûr (cloud chiffré)

2. **Utilisation**
   - ✅ Ne signer que sur une machine sécurisée
   - ✅ Scanner les fichiers avant signature
   - ✅ Vérifier la signature après

3. **Protection**
   - ❌ Ne jamais commiter le certificat sur Git
   - ❌ Ne jamais partager la clé privée
   - ❌ Ne jamais envoyer par email non chiffré

### En Cas de Compromission

Si votre certificat est compromis:
1. **Révoquer immédiatement** auprès du fournisseur
2. **Notifier les utilisateurs**
3. **Commander un nouveau certificat**
4. **Re-signer tous les exécutables**

---

## 📈 Impact sur le Score de Sécurité

### Avant (Score Actuel: 83/100)
- ❌ Pas de certificat code signing (-8 pts)
- ⚠️ Windows SmartScreen peut bloquer

### Après Certificat OV (+6 pts → 89/100)
- ✅ Signature Authenticode valide
- ⚠️ Réputation progressive

### Après Certificat EV (+8 pts → 91/100)
- ✅ Signature Authenticode EV
- ✅ Réputation SmartScreen immédiate
- ✅ Confiance maximale

---

**Auteur**: UndKiMi  
**Version**: MAJOR UPDATE  
**Coût Recommandé**: 500€/an (Sectigo EV)
