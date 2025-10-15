#!/usr/bin/env python3
"""NETTOYAGE AUTOMATIQUE - Exécutez ce fichier"""
import os
from pathlib import Path
import shutil

# Liste complète des fichiers à supprimer
TO_DELETE = [
    "build.ps1", "FINAL_PUSH_READY.md", "CLEANUP_PLAN.md", 
    "CLEANUP_COMPLETE.md", "cleanup_project.py", "cleanup_radical.py",
    "NETTOYAGE_FINAL.md", "5Ghz_Cleaner.spec", "app.manifest",
    "reorganize_project.py", ".bandit", ".pylintrc", "pytest.ini",
    "docs/BADGES_FIXED.md", "docs/REORGANIZATION_SUMMARY.md",
    "docs/development/BUILD_IMPROVEMENTS_SUMMARY.md",
    "docs/development/GITHUB_PUSH_SUMMARY.md",
    "docs/development/COMMIT_MESSAGE.txt",
    "docs/development/BUILD_GUIDE.md",
]

DIRS_TO_DELETE = ["tests", "__pycache__"]

print("\n🧹 NETTOYAGE AUTOMATIQUE\n" + "="*50)
deleted = 0

for f in TO_DELETE:
    p = Path(f)
    if p.exists():
        p.unlink()
        print(f"✅ {f}")
        deleted += 1

for d in DIRS_TO_DELETE:
    p = Path(d)
    if p.exists() and p.is_dir():
        shutil.rmtree(p)
        print(f"✅ {d}/")
        deleted += 1

print(f"\n✅ {deleted} éléments supprimés")
print("\n⚠️  Supprimez maintenant: CLEAN_NOW.py")
print("🚀 Puis: git add . && git commit -m 'Clean' && git push\n")
