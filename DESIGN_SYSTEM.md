# 5GH'z Cleaner Design System

## Structure du Projet

```
5Ghz_Cleaner/
├── assets/
│   └── icons/                    # Icônes SVG personnalisées
│       ├── cleaning.svg
│       ├── folder.svg
│       └── shield_check.svg
├── backend/
│   ├── __init__.py
│   ├── cleaner.py               # Fonctions de nettoyage
│   ├── elevation.py             # Gestion privilèges admin
│   └── logger.py                # Système de logging
├── frontend/
│   ├── design_system/           # Design System
│   │   ├── __init__.py
│   │   ├── theme.py             # Tokens design
│   │   ├── buttons.py
│   │   ├── containers.py
│   │   ├── text.py
│   │   ├── icons.py
│   │   └── inputs.py
│   ├── pages/                   # Pages application
│   │   ├── __init__.py
│   │   └── main_page.py
│   ├── __init__.py
│   ├── app.py                   # App principale
│   ├── constants.py             # (deprecated)
│   └── ui_components.py         # (deprecated)
└── main.py                      # Point d'entrée
```

## Design System

### Import
```python
from frontend.design_system import *
from frontend.design_system.theme import Colors, Spacing, Typography, BorderRadius
from backend.logger import CleaningLogger
```

### Composants

**Boutons**
- `PrimaryButton` - Action principale
- `SecondaryButton` - Action secondaire
- `IconButton` - Icône seule
- `TextButton` - Texte seul

**Conteneurs**
- `Card` - Carte avec ombre
- `Panel` - Panneau
- `WarningBox` - Avertissement
- `Divider` - Séparateur
- `Spacer` - Espace vertical

**Texte**
- `Heading(text, level=1-6)` - Titres
- `BodyText(text, size=13)` - Corps
- `Caption(text, size=11)` - Légende (size optionnel)
- `Link(text, url)` - Lien

**Icônes**
- `ShieldIcon(size=83, with_glow=True)`
- `WarningIcon`, `InfoIcon`, `SuccessIcon`, `ErrorIcon`

**Inputs**
- `Checkbox` - Case à cocher
- `CustomCheckbox.create()` - Multi-lignes
- `Slider` - Curseur
- `Switch` - Interrupteur
- `TextField` - Champ texte

### Système de Logging

```python
# Initialiser
logger = CleaningLogger()

# Logger une opération
op_index = logger.log_operation_start("Nom", "Description")
logger.log_operation_detail(op_index, "Détail")
logger.log_operation_end(op_index, files=10, space_mb=50, success=True)

# Finaliser
log_info = logger.finalize()
# Crée: Documents/5GH'zCleaner-logs/cleaning_YYYYMMDD_HHMMSS.txt
```

### Animations

**Transitions de page**
```python
container.opacity = 0  # Fade out
page.update()
time.sleep(0.3)
# Changement contenu
container.opacity = 1  # Fade in
page.update()
```

**Barre de progression fluide**
- Animation en 20 étapes
- 10ms entre chaque étape
- Transition douce 0→100%

### Architecture Pages

**MainPage** (`frontend/pages/main_page.py`)
- `build()` - Construction page
- `_build_header()` - En-tête
- `_build_tabs()` - Onglets navigation
- `_build_actions_section()` - Actions rapides
- `_build_advanced_options()` - Options avancées
- `_show_cleaning_page()` - Page nettoyage
- `_run_cleaning()` - Processus nettoyage
- `_return_to_main_page()` - Retour avec animation

### Bonnes Pratiques

1. Utiliser les composants du design system
2. Respecter les tokens (Colors, Spacing, Typography)
3. Logger toutes les opérations importantes
4. Animations fluides (300ms, EASE_IN_OUT)
5. Gestion d'erreurs robuste
