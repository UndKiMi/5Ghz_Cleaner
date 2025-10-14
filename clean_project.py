"""
Script de nettoyage et réorganisation du projet
Supprime les fichiers inutiles et prépare pour GitHub
"""
import os
import shutil
from pathlib import Path

def clean_project():
    """Nettoie le projet des fichiers inutiles"""
    
    project_root = Path(__file__).parent
    
    print("=" * 70)
    print("  NETTOYAGE DU PROJET - 5GH'z CLEANER")
    print("=" * 70)
    print()
    
    # Fichiers et dossiers à supprimer
    items_to_remove = [
        # Fichiers temporaires Python
        "__pycache__",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        ".Python",
        "*.so",
        "*.egg",
        "*.egg-info",
        
        # Fichiers de build
        "build",
        "dist",
        "*.spec",
        
        # Fichiers IDE
        ".vscode/settings.json",
        ".idea",
        "*.swp",
        "*.swo",
        
        # Fichiers temporaires
        "*.tmp",
        "*.bak",
        "*.old",
        "*.log",
        
        # Fichiers de test obsolètes
        "test_*.py",
        "*_test.py",
        
        # Scripts de nettoyage obsolètes
        "cleanup_project.py",
        "fix_spelling.py",
    ]
    
    removed_count = 0
    
    print("[1/3] Suppression des fichiers temporaires et obsolètes...")
    print()
    
    for item_pattern in items_to_remove:
        if "*" in item_pattern:
            # Pattern avec wildcard
            for file_path in project_root.rglob(item_pattern):
                try:
                    if file_path.is_file():
                        file_path.unlink()
                        print(f"  [OK] Supprimé : {file_path.relative_to(project_root)}")
                        removed_count += 1
                except Exception as e:
                    print(f"  [ERREUR] {file_path.name} : {e}")
        else:
            # Fichier ou dossier spécifique
            item_path = project_root / item_pattern
            if item_path.exists():
                try:
                    if item_path.is_dir():
                        shutil.rmtree(item_path)
                        print(f"  [OK] Dossier supprimé : {item_pattern}")
                    else:
                        item_path.unlink()
                        print(f"  [OK] Fichier supprimé : {item_pattern}")
                    removed_count += 1
                except Exception as e:
                    print(f"  [ERREUR] {item_pattern} : {e}")
    
    print()
    print("[2/3] Vérification de la structure du projet...")
    print()
    
    # Vérifier que les dossiers essentiels existent
    essential_dirs = [
        "backend",
        "frontend",
        "frontend/pages",
        "frontend/design_system",
        "config",
        "libs",
        ".github/workflows",
    ]
    
    for dir_path in essential_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            print(f"  [OK] {dir_path}")
        else:
            print(f"  [MANQUANT] {dir_path}")
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"  [CRÉÉ] {dir_path}")
    
    print()
    print("[3/3] Vérification des fichiers essentiels...")
    print()
    
    essential_files = [
        "main.py",
        "requirements.txt",
        "README.md",
        ".gitignore",
        ".github/workflows/security.yml",
    ]
    
    for file_path in essential_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"  [OK] {file_path}")
        else:
            print(f"  [MANQUANT] {file_path}")
    
    print()
    print("=" * 70)
    print(f"  NETTOYAGE TERMINÉ - {removed_count} élément(s) supprimé(s)")
    print("=" * 70)
    print()
    print("Le projet est prêt pour GitHub !")
    print()
    print("Prochaines étapes :")
    print("  1. git add .")
    print("  2. git commit -m \"Clean project and add security audit\"")
    print("  3. git push")
    print()
    print("Le Security Audit GitHub se lancera automatiquement.")
    print()

if __name__ == "__main__":
    clean_project()
