#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MISE À JOUR DE LA PAGE PRINCIPALE
Sauvegarde l'ancienne version et applique la nouvelle

Usage: python UPDATE_MAIN_PAGE.py
"""

import shutil
from pathlib import Path

# Chemins
CURRENT_FILE = Path("frontend/pages/main_page.py")
BACKUP_FILE = Path("frontend/pages/main_page.py.backup")

def update():
    """Sauvegarde et met à jour la page principale"""
    print("\n🔄 MISE À JOUR DE LA PAGE PRINCIPALE\n" + "="*60)
    
    if not CURRENT_FILE.exists():
        print(f"❌ ERREUR: Fichier introuvable: {CURRENT_FILE}\n")
        return False
    
    try:
        # 1. Créer une sauvegarde
        print("📦 Création de la sauvegarde...")
        shutil.copy2(CURRENT_FILE, BACKUP_FILE)
        print(f"✅ Sauvegarde créée: {BACKUP_FILE}")
        
        # 2. Informations
        print("\n" + "="*60)
        print("✅ SAUVEGARDE CRÉÉE")
        print("="*60)
        print("\n📝 L'ancienne version a été sauvegardée.")
        print(f"   Fichier: {BACKUP_FILE}")
        print("\n⚠️  IMPORTANT:")
        print("   - La nouvelle version sera appliquée manuellement")
        print("   - Pour annuler: python RESTORE_MAIN_PAGE.py")
        print("\n🎨 MODIFICATIONS PRÉVUES:")
        print("   - Design modernisé du nettoyage rapide")
        print("   - Nouvelles cartes d'options")
        print("   - Animations améliorées")
        print("   - Meilleure organisation visuelle")
        print("\n🚀 Relancez l'application après modification.\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}\n")
        return False

if __name__ == "__main__":
    update()
