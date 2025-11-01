"""
Script pour mettre à jour tous les imports après la réorganisation
"""
import os
import re
from pathlib import Path

# Mapping des anciens chemins vers les nouveaux
IMPORT_MAPPINGS = {
    r'from src.core import': 'from src.core import',
    r'from backend\.cleaner import': 'from src.core.cleaner import',
    r'from backend\.dry_run import': 'from src.core.dry_run import',
    r'from backend\.file_scanner import': 'from src.core.file_scanner import',
    r'from backend\.disk_optimizer import': 'from src.core.disk_optimizer import',
    r'from backend\.ram_manager import': 'from src.core.ram_manager import',
    r'from backend\.advanced_optimizations import': 'from src.core.advanced_optimizations import',
    
    r'from backend\.logger import': 'from src.utils.logger import',
    r'from backend\.logger_safe import': 'from src.utils.logger_safe import',
    r'from backend\.elevation import': 'from src.utils.elevation import',
    r'from backend\.system_commands import': 'from src.utils.system_commands import',
    r'from backend\.quick_actions_config import': 'from src.utils.quick_actions_config import',
    
    r'from backend\.hardware_monitor import': 'from src.services.hardware_monitor import',
    r'from backend\.hardware_sensors import': 'from src.services.hardware_sensors import',
    r'from backend\.security import': 'from src.services.security import',
    r'from backend\.security_core import': 'from src.services.security_core import',
    r'from backend\.security_auditor import': 'from src.services.security_auditor import',
    r'from backend\.signature_manager import': 'from src.services.signature_manager import',
    r'from backend\.telemetry_checker import': 'from src.services.telemetry_checker import',
    
    r'from utils\.console_colors import': 'from src.utils.console_colors import',
    r'from src.utils import': 'from src.utils import',
    
    r'from frontend\.app import': 'from src.ui.app import',
    r'from src.ui import': 'from src.ui import',
    
    r'from scripts.download_librehardwaremonitor import': 'from scripts.download_librehardwaremonitor import',
}

def update_imports_in_file(file_path):
    """Met à jour les imports dans un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Appliquer tous les remplacements
        for old_pattern, new_import in IMPORT_MAPPINGS.items():
            content = re.sub(old_pattern, new_import, content)
        
        # Sauvegarder si modifié
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Updated: {file_path}")
            return True
        return False
    except Exception as e:
        print(f"[ERROR] Error updating {file_path}: {e}")
        return False

def main():
    """Parcourt tous les fichiers Python et met à jour les imports"""
    root_dir = Path(__file__).parent.parent
    updated_count = 0
    
    # Parcourir tous les fichiers .py
    for py_file in root_dir.rglob('*.py'):
        # Ignorer les fichiers dans __pycache__ et .git
        if '__pycache__' in str(py_file) or '.git' in str(py_file):
            continue
        
        if update_imports_in_file(py_file):
            updated_count += 1
    
    print(f"\n[DONE] Total files updated: {updated_count}")

if __name__ == "__main__":
    main()
