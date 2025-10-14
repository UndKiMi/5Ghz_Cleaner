"""
Script de nettoyage du projet
Supprime les fichiers obsolètes et réorganise la structure
"""
import os
import shutil
from pathlib import Path

def cleanup_project():
    """Nettoie le projet en supprimant les fichiers obsolètes"""
    
    project_root = Path(__file__).parent
    
    # Fichiers à supprimer (obsolètes ou doublons)
    files_to_delete = [
        # Fichiers de test
        "test_hardware_monitor.py",
        
        # Scripts obsolètes
        "setup.py",
        "reinstall_librehardwaremonitor.bat",
        
        # Fichiers de développement
        "requirements-dev.txt",
        
        # Documentation obsolète (garder seulement README.md)
        "CONTRIBUTING.md",
        "GUIDE_MIGRATION.md",
        "INSTALLATION.md",
        "PRIVACY.md",
        "QUICK_START.md",
        "REORGANISATION_COMPLETE.md",
        "REORGANISATION_SUMMARY.md",
        "SECURITY.md",
        
        # Fichiers backend obsolètes (à vérifier avant suppression)
        # "backend/cleaner.py",  # Utilisé - NE PAS SUPPRIMER
        # "backend/dry_run.py",  # À vérifier
        # "backend/logger.py",  # Non utilisé
        # "backend/security_core.py",  # Doublon
        # "backend/signature_manager.py",  # Non utilisé
    ]
    
    # Dossiers à supprimer
    folders_to_delete = [
        "Documentations",  # Toute la documentation
        "scripts",  # Scripts obsolètes
        "__pycache__",  # Cache Python (racine)
        "backend/__pycache__",
        "config/__pycache__",
        "frontend/__pycache__",
        "frontend/pages/__pycache__",
    ]
    
    print("=" * 70)
    print("  NETTOYAGE DU PROJET")
    print("=" * 70)
    print()
    
    # Supprimer les fichiers
    print("[1/3] Suppression des fichiers obsoletes")
    deleted_files = 0
    for file_path in files_to_delete:
        full_path = project_root / file_path
        if full_path.exists():
            try:
                full_path.unlink()
                print(f"  [OK] Supprime: {file_path}")
                deleted_files += 1
            except Exception as e:
                print(f"  [ERREUR] {file_path} - {e}")
        else:
            print(f"  [SKIP] Deja absent: {file_path}")
    print(f"  => {deleted_files} fichier(s) supprime(s)\n")
    
    # Supprimer les dossiers
    print("[2/3] Suppression des dossiers obsoletes")
    deleted_folders = 0
    for folder_path in folders_to_delete:
        full_path = project_root / folder_path
        if full_path.exists():
            try:
                shutil.rmtree(full_path)
                print(f"  [OK] Supprime: {folder_path}/")
                deleted_folders += 1
            except Exception as e:
                print(f"  [ERREUR] {folder_path}/ - {e}")
        else:
            print(f"  [SKIP] Deja absent: {folder_path}/")
    print(f"  => {deleted_folders} dossier(s) supprime(s)\n")
    
    # Créer un fichier .gitignore propre
    print("[3/3] Creation du .gitignore")
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
libs/*.dll
libs/*.exe
libs/*.pdb
!libs/README_LIBREHARDWAREMONITOR.md
!libs/.gitignore

# Logs
*.log

# Temporary files
*.tmp
*.bak
*.old
"""
    
    gitignore_path = project_root / ".gitignore"
    with open(gitignore_path, "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    print(f"  [OK] .gitignore cree")
    print("  => Configuration terminee\n")
    
    print("=" * 70)
    print("  NETTOYAGE TERMINE")
    print("=" * 70)
    print()
    print("Structure finale du projet:")
    print("  5Ghz_Cleaner/")
    print("  +-- backend/          # Logique metier")
    print("  +-- config/           # Configuration")
    print("  +-- frontend/         # Interface utilisateur")
    print("  +-- libs/             # Bibliotheques externes")
    print("  +-- assets/           # Ressources (icones, etc.)")
    print("  +-- main.py           # Point d'entree")
    print("  +-- requirements.txt  # Dependances")
    print("  +-- README.md         # Documentation principale")
    print("  +-- LICENSE           # Licence")
    print()

if __name__ == "__main__":
    cleanup_project()
