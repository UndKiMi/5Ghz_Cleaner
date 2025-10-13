# 📝 Guide de Documentation - 5GH'z Cleaner

## 🎯 Objectif

Ce document définit les règles et conventions pour créer et organiser la documentation du projet.

---

## 📁 Structure des Dossiers

### Organisation

```
Documentations/
├── architecture/       <- Architecture et structure du projet
├── updates/           <- Historique des mises à jour (CHANGELOG, etc.)
├── features/          <- Documentation des nouvelles fonctionnalités
├── reports/           <- Rapports de tests, sécurité, releases
└── guides/            <- Guides utilisateur et développeur
```

### Règles de Placement

#### `architecture/`
**Contenu:**
- Documents sur l'architecture du projet
- Structure des dossiers et fichiers
- Diagrammes d'architecture
- Refactoring majeurs

**Exemples:**
- `ARCHITECTURE_MAJOR_UPDATE.md`
- `PROJECT_STRUCTURE.md`
- `RESTRUCTURATION_FINALE.md`

#### `updates/`
**Contenu:**
- CHANGELOG (journal des modifications)
- Notes de version
- Mises à jour de compatibilité
- Résumés de mises à jour majeures

**Exemples:**
- `CHANGELOG.md`
- `CHANGELOG_MAJOR_UPDATE.md`
- `COMPATIBILITY_UPDATE.md`
- `WINDOWS_11_ONLY.md`

#### `features/`
**Contenu:**
- Documentation des nouvelles fonctionnalités
- Améliorations de fonctionnalités existantes
- Corrections de bugs (BUGFIXES)
- Guides d'implémentation

**Exemples:**
- `HARDWARE_MONITOR_IMPROVEMENTS.md`
- `NATIVE_TEMPERATURE_SOLUTION.md`
- `GPU_TEMP_DETECTION.md`
- `BUGFIXES.md`

#### `reports/`
**Contenu:**
- Rapports de tests
- Rapports de sécurité
- Résumés de releases
- Statuts de préparation (GitHub, Release)

**Exemples:**
- `TEST_REPORT_FINAL.md`
- `SECURITY_IMPROVEMENTS.md`
- `FINAL_SUMMARY.md`
- `GITHUB_READY.md`
- `RELEASE_READY.md`

#### `guides/`
**Contenu:**
- Guides utilisateur
- Guides développeur
- Tutoriels
- FAQ

**Exemples:**
- `USER_GUIDE.md`
- `DEVELOPER_GUIDE.md`
- `INSTALLATION_GUIDE.md`

---

## 📝 Conventions de Nommage

### Fichiers Markdown

**Format:** `TITRE_EN_MAJUSCULES.md`

**Exemples valides:**
- ✅ `HARDWARE_MONITOR_IMPROVEMENTS.md`
- ✅ `NATIVE_TEMPERATURE_SOLUTION.md`
- ✅ `BUGFIXES.md`

**Exemples invalides:**
- ❌ `hardware_monitor_improvements.md` (minuscules)
- ❌ `HardwareMonitorImprovements.md` (CamelCase)
- ❌ `hardware-monitor-improvements.md` (kebab-case)

### Préfixes Courants

- `CHANGELOG_` - Journaux de modifications
- `TEST_` - Rapports de tests
- `SECURITY_` - Documents de sécurité
- `GUIDE_` - Guides et tutoriels
- `FIX_` - Corrections de bugs
- `FEATURE_` - Nouvelles fonctionnalités

---

## 📄 Structure Standard d'un Document

### Template de Base

```markdown
# 📚 [Titre du Document]

## 📋 Vue d'ensemble

[Description courte et claire du contenu]

**Date de création:** [Date]
**Version:** [Version]
**Auteur:** UndKiMi

---

## 🎯 Objectif

[Pourquoi ce document existe-t-il?]

---

## 📖 Contenu Principal

### Section 1
[Contenu détaillé]

### Section 2
[Contenu détaillé]

---

## ✅ Résumé

[Points clés à retenir]

---

## 🔗 Liens Connexes

- [Document 1](./path/to/doc1.md)
- [Document 2](./path/to/doc2.md)

---

**Version:** [Version]
**Dernière mise à jour:** [Date]
```

### Sections Obligatoires

1. **Titre avec emoji** - Facilite la navigation visuelle
2. **Vue d'ensemble** - Résumé en 2-3 phrases
3. **Contenu principal** - Corps du document
4. **Résumé** - Points clés
5. **Footer** - Version et date

### Sections Optionnelles

- **Objectif** - Pour les documents techniques
- **Exemples** - Code et cas d'usage
- **Tests** - Validation et résultats
- **Liens connexes** - Références croisées

---

## 🎨 Style et Formatage

### Emojis

Utilisez des emojis pour améliorer la lisibilité:

- 📚 Documentation générale
- 🎯 Objectifs
- ✅ Succès / Complété
- ❌ Erreur / Échec
- ⚠️ Avertissement
- 🔐 Sécurité
- 🚀 Performance
- 📊 Statistiques
- 🔍 Détails
- 💡 Astuce
- 📝 Note
- 🔗 Lien

### Titres

```markdown
# Titre Principal (H1) - Une seule fois par document
## Titre de Section (H2)
### Sous-section (H3)
#### Sous-sous-section (H4)
```

### Code

**Inline:** Utilisez \`backticks\` pour le code inline

**Blocs:**
\```python
def example():
    return "Hello World"
\```

### Listes

**Non ordonnées:**
```markdown
- Point 1
- Point 2
  - Sous-point
```

**Ordonnées:**
```markdown
1. Étape 1
2. Étape 2
3. Étape 3
```

### Tableaux

```markdown
| Colonne 1 | Colonne 2 | Colonne 3 |
|-----------|-----------|-----------|
| Valeur 1  | Valeur 2  | Valeur 3  |
```

### Liens

**Interne:** `[Texte](./chemin/relatif.md)`
**Externe:** `[Texte](https://example.com)`

---

## 🔄 Workflow de Création

### 1. Créer le Document

```bash
# Dans le bon dossier selon le type
cd Documentations/features/  # ou architecture/, updates/, etc.
```

### 2. Utiliser le Template

Copiez le template de base et remplissez les sections.

### 3. Ajouter au INDEX.md

Mettez à jour `Documentations/INDEX.md` avec:
- Lien vers le nouveau document
- Description courte
- Catégorie appropriée

### 4. Commit

```bash
git add Documentations/
git commit -m "docs: Add [NOM_DU_DOCUMENT]"
```

---

## 📊 Checklist de Qualité

Avant de finaliser un document, vérifiez:

- [ ] Titre clair avec emoji approprié
- [ ] Vue d'ensemble présente
- [ ] Contenu structuré avec H2/H3
- [ ] Code formaté correctement
- [ ] Liens fonctionnels
- [ ] Footer avec version et date
- [ ] Orthographe et grammaire vérifiées
- [ ] Ajouté à INDEX.md
- [ ] Placé dans le bon dossier

---

## 🚫 À Éviter

### ❌ Mauvaises Pratiques

1. **Fichiers à la racine du projet**
   - ❌ `c:\5Ghz_Cleaner\NOUVEAU_DOCUMENT.md`
   - ✅ `c:\5Ghz_Cleaner\Documentations\features\NOUVEAU_DOCUMENT.md`

2. **Noms de fichiers incohérents**
   - ❌ `nouveauDocument.md`
   - ✅ `NOUVEAU_DOCUMENT.md`

3. **Documents sans structure**
   - Pas de sections
   - Pas de formatage
   - Pas de résumé

4. **Liens cassés**
   - Vérifiez toujours les liens relatifs

5. **Duplication**
   - Ne créez pas de documents redondants
   - Mettez à jour l'existant si possible

---

## 📚 Exemples de Bons Documents

### Exemple 1: Nouvelle Fonctionnalité

**Fichier:** `Documentations/features/HARDWARE_MONITOR_IMPROVEMENTS.md`

**Contenu:**
- Vue d'ensemble de la fonctionnalité
- Modifications effectuées
- Exemples d'utilisation
- Tests et validation
- Impact sur le projet

### Exemple 2: Correction de Bug

**Fichier:** `Documentations/features/BUGFIXES.md`

**Contenu:**
- Liste des bugs corrigés
- Cause de chaque bug
- Solution implémentée
- Tests de validation

### Exemple 3: Mise à Jour

**Fichier:** `Documentations/updates/CHANGELOG.md`

**Contenu:**
- Version
- Date
- Liste des changements (Added, Changed, Fixed, Removed)
- Notes de migration si nécessaire

---

## 🔄 Maintenance

### Révision Régulière

- **Mensuelle:** Vérifier les liens cassés
- **Trimestrielle:** Mettre à jour les statistiques
- **Annuelle:** Archiver les documents obsolètes

### Archivage

Documents obsolètes → `Documentations/archive/`

---

## 📞 Contact

Pour toute question sur la documentation:

- **Repository:** https://github.com/UndKiMi/5Ghz_Cleaner
- **Auteur:** UndKiMi

---

**Version:** 1.0
**Dernière mise à jour:** 13 octobre 2025
**Auteur:** UndKiMi
