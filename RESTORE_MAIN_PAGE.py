#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT D'ANNULATION - Restaure la page principale originale
Exécutez ce script pour annuler toutes les modifications de main_page.py

Usage: python RESTORE_MAIN_PAGE.py
"""

import shutil
from pathlib import Path

# Chemins
BACKUP_FILE = Path("frontend/pages/main_page.py.backup")
CURRENT_FILE = Path("frontend/pages/main_page.py")

def restore():
    """Restaure la version originale"""
    print("\n🔄 RESTAURATION DE LA PAGE PRINCIPALE\n" + "="*60)
    
    if not BACKUP_FILE.exists():
        print("❌ ERREUR: Fichier de sauvegarde introuvable!")
        print(f"   Cherché: {BACKUP_FILE}")
        print("\n⚠️  La sauvegarde n'a pas été créée.")
        print("   Impossible de restaurer.\n")
        return False
    
    try:
        # Restaurer depuis la sauvegarde
        shutil.copy2(BACKUP_FILE, CURRENT_FILE)
        print(f"✅ Fichier restauré: {CURRENT_FILE}")
        print(f"   Depuis: {BACKUP_FILE}")
        
        # Supprimer la sauvegarde
        BACKUP_FILE.unlink()
        print(f"✅ Sauvegarde supprimée: {BACKUP_FILE}")
        
        print("\n" + "="*60)
        print("✅ RESTAURATION TERMINÉE")
        print("="*60)
        print("\n📝 La page principale a été restaurée à son état original.")
        print("🚀 Relancez l'application pour voir les changements.\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR lors de la restauration: {e}\n")
        return False

if __name__ == "__main__":
    restore()
