#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5GH'z Cleaner - Project Cleanup Script
Supprime les fichiers temporaires et inutiles du projet

Usage: python cleanup_project.py
"""

import os
import shutil
from pathlib import Path

# Fichiers à supprimer
FILES_TO_DELETE = [
    "build.ps1",  # PowerShell - remplacé par build.py
    "FINAL_PUSH_READY.md",  # Temporaire
    "5Ghz_Cleaner.spec",  # Généré automatiquement
    "reorganize_project.py",  # One-time script
    "CLEANUP_PLAN.md",  # Temporaire
    "cleanup_project.py",  # Ce script lui-même (après exécution)
]

# Dossiers à supprimer
DIRS_TO_DELETE = [
    "docs/BADGES_FIXED.md",
    "docs/REORGANIZATION_SUMMARY.md",
    "docs/development/BUILD_IMPROVEMENTS_SUMMARY.md",
    "docs/development/GITHUB_PUSH_SUMMARY.md",
    "docs/development/COMMIT_MESSAGE.txt",
]

def main():
    """Nettoie le projet"""
    print("🧹 NETTOYAGE DU PROJET\n")
    print("=" * 70)
    
    deleted_count = 0
    
    # Supprimer les fichiers
    print("\n📁 Suppression des fichiers...")
    for file_path in FILES_TO_DELETE:
        path = Path(file_path)
        if path.exists():
            try:
                if path.name == "cleanup_project.py":
                    print(f"  [SKIP] {file_path} (sera supprimé à la fin)")
                    continue
                path.unlink()
                print(f"  [OK] Supprimé: {file_path}")
                deleted_count += 1
            except Exception as e:
                print(f"  [ERROR] Impossible de supprimer {file_path}: {e}")
        else:
            print(f"  [SKIP] N'existe pas: {file_path}")
    
    # Supprimer les fichiers de documentation temporaires
    print("\n📚 Suppression de la documentation temporaire...")
    for file_path in DIRS_TO_DELETE:
        path = Path(file_path)
        if path.exists():
            try:
                path.unlink()
                print(f"  [OK] Supprimé: {file_path}")
                deleted_count += 1
            except Exception as e:
                print(f"  [ERROR] Impossible de supprimer {file_path}: {e}")
        else:
            print(f"  [SKIP] N'existe pas: {file_path}")
    
    # Résumé
    print("\n" + "=" * 70)
    print(f"\n✅ NETTOYAGE TERMINÉ")
    print(f"   {deleted_count} fichiers supprimés\n")
    
    print("📝 Fichiers conservés:")
    print("  - build.py (nouveau script Python)")
    print("  - PRIVACY.md (nouveau)")
    print("  - CHANGELOG.md (nouveau)")
    print("  - Tous les fichiers essentiels du projet\n")
    
    print("⚠️  N'oubliez pas de supprimer manuellement:")
    print("  - cleanup_project.py (ce script)\n")

if __name__ == "__main__":
    main()
