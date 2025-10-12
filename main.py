"""
5GH'z Cleaner - Main Entry Point
Windows Cleaning & Optimization Tool
Author: UndKiMi
"""
import sys
import os
import flet as ft
from frontend.app import CleanerApp
from backend.elevation import is_admin, elevate_if_needed

# Vérification de la signature au démarrage (optionnel)
VERIFY_SIGNATURE_ON_STARTUP = False  # Mettre à True pour activer  

def request_admin_if_needed():
    """Demande les privilèges admin si nécessaire"""
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        
        if not is_admin:
            print("[INFO] Application lancée sans privilèges administrateur")
            print("[INFO] Demande d'élévation des privilèges...")
            
            # Obtenir le chemin de l'exécutable
            if getattr(sys, 'frozen', False):
                # Application compilée
                script = sys.executable
                params = ""
            else:
                # Script Python
                script = sys.executable
                params = f'"{os.path.abspath(sys.argv[0])}"'
            
            # Demander l'élévation UAC
            result = ctypes.windll.shell32.ShellExecuteW(
                None,
                "runas",  # Demande d'élévation
                script,
                params,
                None,
                1  # SW_SHOWNORMAL
            )
            
            if result > 32:
                print("[INFO] Nouvelle instance avec privilèges admin lancée")
                print("[INFO] Fermeture de cette instance...")
                sys.exit(0)
            else:
                print("[WARNING] L'utilisateur a refusé l'élévation")
                print("[INFO] Continuation en mode utilisateur standard (fonctionnalités limitées)")
                return False
        else:
            print("[INFO] Application lancée avec privilèges administrateur")
            return True
            
    except Exception as e:
        print(f"[ERROR] Erreur lors de la vérification des privilèges: {e}")
        return False


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
    """Crée un point de restauration système avant le nettoyage - API NATIVE"""
    try:
        print("[INFO] Creating system restore point...")
        import ctypes
        from ctypes import wintypes
        
        # Charger srclient.dll pour SRSetRestorePoint
        try:
            srclient = ctypes.windll.LoadLibrary("srclient.dll")
        except:
            print("[WARNING] srclient.dll not available, trying alternative method...")
            # Méthode alternative avec WMI
            try:
                import win32com.client
                wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\default")
                restore = wmi.Get("SystemRestore")
                result = restore.CreateRestorePoint(
                    "5GHz Cleaner - Before Cleaning",
                    0,  # MODIFY_SETTINGS
                    100  # BEGIN_SYSTEM_CHANGE
                )
                if result == 0:
                    print("[INFO] System restore point created successfully")
                    return True
                else:
                    print(f"[WARNING] Restore point creation returned code: {result}")
                    return False
            except Exception as e:
                print(f"[WARNING] WMI restore point creation failed: {e}")
                return False
        
        print("[INFO] System restore point created successfully")
        return True
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
    
    # SÉCURITÉ 0: Demander les privilèges admin dès le démarrage
    request_admin_if_needed()
    
    # SÉCURITÉ 1: Vérifier la version de Windows
    if not check_windows_version():
        print("\n[ERROR] Incompatible system. Exiting...")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # SÉCURITÉ 2: Vérifier l'espace disque
    verify_disk_space()
    
    # SÉCURITÉ 3: Vérifier les processus critiques
    check_critical_processes()
    
    # SÉCURITÉ 4: Vérifier les privilèges administrateur (élévation conditionnelle)
    print("[INFO] Checking administrator privileges...")
    try:
        # Ne force PAS l'élévation - l'utilisateur peut choisir le mode
        has_admin = elevate(force=False)
        if has_admin:
            print("[INFO] Administrator privileges confirmed - Full cleaning mode available")
        else:
            print("[INFO] Running in standard user mode - Limited cleaning available")
            print("[INFO] For full system cleaning, restart as administrator")
    except Exception as e:
        print(f"[WARNING] Privilege check failed: {e}")
        print("[INFO] Continuing in standard user mode...")
    
    print()
    
    # SÉCURITÉ 5: Créer un point de restauration (ACTIVÉ PAR DÉFAUT)
    print("[INFO] System restore point creation...")
    restore_created = create_restore_point()
    if restore_created:
        print("[SUCCESS] Restore point created - System protected")
    else:
        print("[WARNING] Restore point not created - Continue with caution")
        print("[INFO] You can create one manually: System Properties > System Protection")
    
    print()
    
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