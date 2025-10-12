# 5GH'z Cleaner Design System

## 📁 Structure du Projet (Optimisée)

```
5Ghz_Cleaner/
├── 📂 assets/                   # Ressources statiques
│   └── icons/                   # Icônes SVG
│       ├── cleaning.svg
│       ├── folder.svg
│       └── shield_check.svg
│
├── 📂 backend/                  # Logique métier & sécurité
│   ├── __init__.py
│   ├── cleaner.py              # ⚙️ Fonctions de nettoyage (7 niveaux de sécurité)
│   ├── elevation.py            # 🔐 Gestion privilèges admin
│   ├── logger.py               # 📝 Système de logging détaillé
│   └── security.py             # 🛡️ Gestionnaire de sécurité système
│
├── 📂 frontend/                 # Interface utilisateur
│   ├── design_system/          # 🎨 Design System modulaire
│   │   ├── __init__.py         # Exports centralisés
│   │   ├── theme.py            # Tokens (Colors, Spacing, Typography, BorderRadius)
│   │   ├── buttons.py          # Composants boutons
│   │   ├── containers.py       # Composants conteneurs
│   │   ├── text.py             # Composants texte
│   │   ├── icons.py            # Composants icônes
│   │   └── inputs.py           # Composants inputs
│   │
│   ├── pages/                  # 📄 Pages de l'application
│   │   ├── __init__.py
│   │   └── main_page.py        # Page principale avec nettoyage
│   │
│   ├── __init__.py
│   └── app.py                  # 🚀 Application Flet principale
│
├── 📂 build/                    # Build artifacts (ignoré)
├── 📂 dist/                     # Distribution (ignoré)
│
├── 📄 main.py                   # 🎯 Point d'entrée (5 niveaux de sécurité)
├── 📄 requirements.txt          # Dépendances Python
├── 📄 build.bat                 # Script de build
├── 📄 run.bat                   # Script de lancement
└── 📄 DESIGN_SYSTEM.md          # Documentation (ce fichier)
```

## 🎨 Design System

### Import Rapide
```python
# Import complet du design system
from frontend.design_system import *
from frontend.design_system.theme import Colors, Spacing, Typography, BorderRadius

# Import des modules backend
from backend.logger import CleaningLogger
from backend.security import security_manager
from backend import cleaner
```

### 🧩 Composants UI

#### Boutons
| Composant | Usage | Exemple |
|-----------|-------|---------|
| `PrimaryButton` | Action principale | `PrimaryButton("Nettoyer", on_click=handler)` |
| `SecondaryButton` | Action secondaire | `SecondaryButton("Annuler", on_click=handler)` |
| `IconButton` | Icône seule | `IconButton(icon=ft.Icons.SETTINGS)` |
| `TextButton` | Texte seul | `TextButton("En savoir plus")` |

#### Conteneurs
| Composant | Usage | Exemple |
|-----------|-------|---------|
| `Card` | Carte avec ombre | `Card(content=Column([...]), shadow_level="lg")` |
| `Panel` | Panneau de contenu | `Panel(content=Column([...]))` |
| `WarningBox` | Boîte d'avertissement | `WarningBox("Message important")` |
| `Divider` | Séparateur horizontal | `Divider()` |
| `Spacer` | Espace vertical | `Spacer(height=Spacing.MD)` |

#### Texte
| Composant | Usage | Exemple |
|-----------|-------|---------|
| `Heading` | Titres (1-6) | `Heading("Titre", level=1)` |
| `BodyText` | Texte corps | `BodyText("Contenu", size=13)` |
| `Caption` | Légende | `Caption("Note", size=11)` |
| `Link` | Lien cliquable | `Link("Cliquez ici", url="...")` |

#### Icônes
| Composant | Usage | Exemple |
|-----------|-------|---------|
| `ShieldIcon` | Icône bouclier avec glow | `ShieldIcon(size=83, with_glow=True)` |
| `WarningIcon` | Icône avertissement | `WarningIcon()` |
| `InfoIcon` | Icône information | `InfoIcon()` |
| `SuccessIcon` | Icône succès | `SuccessIcon()` |
| `ErrorIcon` | Icône erreur | `ErrorIcon()` |

#### Inputs
| Composant | Usage | Exemple |
|-----------|-------|---------|
| `Checkbox` | Case à cocher | `Checkbox(label="Option")` |
| `CustomCheckbox` | Multi-lignes | `CustomCheckbox.create("Titre", "Description")` |
| `Slider` | Curseur | `Slider(min=0, max=100)` |
| `Switch` | Interrupteur | `Switch(label="Activer")` |
| `TextField` | Champ texte | `TextField(label="Nom")` |

### 📝 Système de Logging

Le système de logging crée des rapports détaillés de chaque nettoyage.

```python
# 1. Initialiser le logger
logger = CleaningLogger()

# 2. Logger une opération
op_index = logger.log_operation_start(
    "Nettoyage fichiers temporaires",
    "Suppression des fichiers temporaires système"
)

# 3. Ajouter des détails
logger.log_operation_detail(op_index, "Fichiers temporaires: 150 fichiers")
logger.log_operation_detail(op_index, "Cache Windows Update: 45 fichiers")

# 4. Terminer l'opération
logger.log_operation_end(
    op_index,
    files_deleted=195,
    space_freed_mb=450.5,
    success=True
)

# 5. Finaliser et sauvegarder
log_info = logger.finalize()
# Crée: Documents/5GH'zCleaner-logs/cleaning_YYYYMMDD_HHMMSS.txt
```

**Contenu du log :**
- ✅ Horodatage de chaque opération
- ✅ Nombre de fichiers supprimés
- ✅ Espace disque libéré (MB/GB)
- ✅ Durée de chaque opération
- ✅ Détails des erreurs
- ✅ Résumé global de la session

### 🛡️ Système de Sécurité

Le `SecurityManager` protège Windows avec plusieurs niveaux de vérification.

```python
from backend.security import security_manager

# Vérifier l'intégrité du système
if security_manager.verify_system_integrity():
    print("✓ Système sain")

# Vérifier s'il est sûr de procéder
if security_manager.is_safe_to_proceed():
    # Lancer le nettoyage
    pass

# Vérifier si un fichier est système
if security_manager.is_system_file(filepath):
    print("⚠️ Fichier système protégé")

# Vérifier les droits admin
if security_manager.verify_admin_rights():
    print("✓ Droits administrateur")
```

**Protections actives :**
- ✅ Vérification version Windows (10+)
- ✅ Contrôle fichiers système critiques
- ✅ Vérification santé disque
- ✅ Détection processus critiques
- ✅ Vérification services Windows
- ✅ Protection zones interdites (System32, etc.)

### ✨ Animations

**Transitions de page (300ms)**
```python
# Fade out
container.opacity = 0
page.update()
time.sleep(0.3)

# Changement de contenu
page.controls.clear()
page.add(new_content)

# Fade in
container.opacity = 1
page.update()
```

**Barre de progression fluide**
```python
# Animation progressive en 20 étapes
for i in range(steps):
    progress_bar.value = current + (increment * (i + 1))
    percentage_text.value = f"{int(progress_bar.value * 100)}%"
    page.update()
    time.sleep(0.01)  # 10ms entre chaque étape
```

**Paramètres d'animation :**
- Durée : 300ms
- Courbe : `EASE_IN_OUT`
- Étapes progression : 20
- Intervalle : 10ms

### 🏗️ Architecture

#### MainPage (`frontend/pages/main_page.py`)

**Méthodes publiques :**
- `build()` - Construction de la page principale

**Méthodes de construction :**
- `_build_header()` - En-tête avec logo et titre
- `_build_tabs()` - Onglets de navigation
- `_build_actions_section()` - Section actions rapides
- `_build_advanced_options()` - Options avancées
- `_build_action_button()` - Bouton de lancement
- `_build_footer()` - Pied de page

**Méthodes de nettoyage :**
- `_start_cleaning(e)` - Démarrage du nettoyage
- `_show_cleaning_page()` - Affichage page de progression
- `_run_cleaning()` - Exécution du nettoyage (thread)
- `_update_cleaning_progress()` - Mise à jour progression
- `_update_task_status()` - Mise à jour statut tâche
- `_return_to_main_page()` - Retour avec animation

**Méthodes utilitaires :**
- `_create_task_item()` - Création élément de tâche
- `_switch_tab()` - Changement d'onglet

#### App (`frontend/app.py`)

**Flux d'application :**
1. `main(page)` - Point d'entrée Flet
2. Affichage conditions d'utilisation
3. Transition vers page principale
4. Gestion du nettoyage

### ⚙️ Backend

#### Cleaner (`backend/cleaner.py`)

**Fonctions de nettoyage :**
- `clear_temp()` - Fichiers temporaires (7 sécurités)
- `clear_windows_update_cache()` - Cache Windows Update
- `clear_prefetch()` - Fichiers prefetch
- `clear_recent()` - Fichiers récents
- `clear_thumbnail_cache()` - Cache miniatures
- `clear_crash_dumps()` - Dumps de crash
- `clear_large_logs()` - Logs volumineux

**Fonctions avancées :**
- `clear_standby_memory()` - RAM Standby
- `flush_dns()` - Cache DNS
- `disable_telemetry()` - Télémétrie Windows
- `empty_recycle_bin()` - Corbeille

**Sécurités intégrées :**
1. Zones interdites (System32, etc.)
2. Fichiers critiques protégés
3. Extensions protégées
4. Vérification temporelle (2h minimum)
5. Vérification verrouillage
6. Vérification taille (500 MB max)
7. Attributs système

### 📋 Bonnes Pratiques

#### Code
1. ✅ Utiliser les composants du design system
2. ✅ Respecter les tokens (Colors, Spacing, Typography, BorderRadius)
3. ✅ Logger toutes les opérations importantes
4. ✅ Animations fluides (300ms, EASE_IN_OUT)
5. ✅ Gestion d'erreurs spécifique (pas de `except:`)
6. ✅ Vérifications de sécurité avant toute opération
7. ✅ Documentation des fonctions

#### Sécurité
1. 🛡️ Toujours vérifier `security_manager.verify_system_integrity()`
2. 🛡️ Ne jamais toucher aux zones interdites
3. 🛡️ Vérifier les fichiers avant suppression
4. 🛡️ Logger toutes les opérations
5. 🛡️ Gestion d'erreurs robuste
6. 🛡️ Privilèges admin requis
7. 🛡️ Vérification processus critiques

#### UI/UX
1. 🎨 Transitions fluides entre les pages
2. 🎨 Feedback visuel immédiat
3. 🎨 Messages d'erreur clairs
4. 🎨 Progression en temps réel
5. 🎨 Animations cohérentes
6. 🎨 Design responsive
7. 🎨 Accessibilité

### 🚀 Performance

**Optimisations :**
- Threading pour opérations longues
- Animations GPU-accelerated (Flet)
- Vérifications en parallèle
- Cache des vérifications
- Logs asynchrones

**Métriques :**
- Temps de démarrage : < 2s
- Transition page : 300ms
- Animation progression : 200ms
- Nettoyage complet : 30-60s
