"""
5Gh'z Cleaner - Windows Cleaning & Optimisation Tool
Author: UndKiMi
Repository: https://github.com/UndKiMi/5Ghz_Cleaner
"""
import sys
import os
import ctypes
import flet as ft
from backend.elevation import elevate
from frontend.app import main


def check_windows_version():
    """Vérifie que Windows est compatible"""
    try:
        version = sys.getwindowsversion()
        # Windows 10 = 10.0, Windows 11 = 10.0 (build 22000+)
        if version.major < 10:
            print("[ERROR] Windows 10 or later is required")
            print(f"[ERROR] Current version: {version.major}.{version.minor}")
            return False
        return True
    except AttributeError:
        print("[ERROR] Not running on Windows")
        return False


def create_restore_point():
    """Crée un point de restauration système avant le nettoyage"""
    try:
        print("[INFO] Creating system restore point...")
        import subprocess
        result = subprocess.run(
            ['powershell', '-Command', 
             'Checkpoint-Computer -Description "5GHz Cleaner - Before Cleaning" -RestorePointType "MODIFY_SETTINGS"'],
            capture_output=True,
            timeout=30
        )
        if result.returncode == 0:
            print("[INFO] System restore point created successfully")
            return True
        else:
            print("[WARNING] Could not create restore point (may require manual creation)")
            return False
    except Exception as e:
        print(f"[WARNING] Restore point creation failed: {e}")
        return False


def check_critical_processes():
    """Vérifie qu'aucun processus critique n'est en cours"""
    critical_processes = [
        'wuauclt.exe',  # Windows Update
        'msiexec.exe',  # Windows Installer
        'setup.exe',    # Installation en cours
        'dism.exe',     # DISM
    ]
    
    try:
        import subprocess
        result = subprocess.run(
            ['tasklist'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        running_critical = []
        for process in critical_processes:
            if process.lower() in result.stdout.lower():
                running_critical.append(process)
        
        if running_critical:
            print("[WARNING] Critical processes detected:")
            for proc in running_critical:
                print(f"  - {proc}")
            print("[WARNING] It's recommended to close these before cleaning")
            return False
        
        return True
    except Exception as e:
        print(f"[WARNING] Could not check processes: {e}")
        return True  # Ne pas bloquer si la vérification échoue


def verify_disk_space():
    """Vérifie qu'il y a assez d'espace disque"""
    try:
        import shutil
        c_drive = "C:\\"
        usage = shutil.disk_usage(c_drive)
        free_gb = usage.free / (1024**3)
        
        if free_gb < 5:  # Moins de 5 GB
            print(f"[WARNING] Low disk space: {free_gb:.2f} GB free")
            print("[WARNING] Cleaning may be limited")
            return False
        
        print(f"[INFO] Disk space: {free_gb:.2f} GB free")
        return True
    except Exception as e:
        print(f"[WARNING] Could not check disk space: {e}")
        return True


if __name__ == "__main__":
    print("=" * 60)
    print("5Gh'z Cleaner - Windows Cleaning & Optimisation Tool")
    print("Author: UndKiMi")
    print("=" * 60)
    print()
    
    # SÉCURITÉ 1: Vérifier la version de Windows
    if not check_windows_version():
        print("\n[ERROR] Incompatible system. Exiting...")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # SÉCURITÉ 2: Vérifier l'espace disque
    verify_disk_space()
    
    # SÉCURITÉ 3: Vérifier les processus critiques
    check_critical_processes()
    
    # SÉCURITÉ 4: Demander les privilèges administrateur
    print("[INFO] Checking administrator privileges...")
    try:
        elevate()
        print("[INFO] Administrator privileges confirmed")
    except Exception as e:
        print(f"[ERROR] Failed to obtain administrator privileges: {e}")
        print("[ERROR] This application requires administrator rights")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print()
    
    # SÉCURITÉ 5: Créer un point de restauration (optionnel)
    # create_restore_point()  # Décommenté si souhaité
    
    # Lancer l'application Flet
    print("[INFO] Launching Flet application...")
    try:
        ft.app(target=main)
    except Exception as e:
        print(f"[ERROR] Application crashed: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)
    
    print()
    print("[INFO] Application closed successfully")
    print("=" * 60)