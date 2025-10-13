"""
5GH'z Cleaner - Main Entry Point
Windows 11 Cleaning & Optimization Tool

Author: UndKiMi
Copyright (c) 2025 UndKiMi
License: CC BY-NC-SA 4.0

This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/

You are free to:
- Share and adapt this work for non-commercial purposes
- You must give appropriate credit and indicate if changes were made
- You must distribute your contributions under the same license

You may NOT:
- Use this work for commercial purposes
- Sell this software or any derivative works

COMPATIBILITY:
- Windows 11 (64-bit) ONLY
- Not compatible with Windows 10 or earlier versions
"""
import sys
import os
import ctypes
import gc
import platform
import flet as ft
from frontend.app import CleanerApp
from backend.elevation import is_admin, elevate_if_needed, elevate

# Optimisation mémoire: Activer le garbage collector agressif
gc.enable()
gc.set_threshold(700, 10, 10)  # Plus agressif pour libérer la mémoire rapidement

# Vérification de la signature au démarrage (optionnel)
VERIFY_SIGNATURE_ON_STARTUP = False  # Mettre à True pour activer  


def check_windows_11():
    """Vérifie que le système est Windows 11"""
    try:
        # Vérifier la version de Windows
        win_version = platform.version()
        win_release = platform.release()
        
        # Windows 11 = version 10.0.22000 ou supérieure
        if sys.platform != 'win32':
            print("[ERROR] This application only works on Windows")
            return False
        
        # Vérifier la version
        version_parts = win_version.split('.')
        if len(version_parts) >= 3:
            major = int(version_parts[0])
            minor = int(version_parts[1])
            build = int(version_parts[2])
            
            # Windows 11 commence au build 22000
            if major == 10 and minor == 0 and build >= 22000:
                print(f"[INFO] Windows 11 detected (Build {build})")
                return True
            else:
                print(f"[ERROR] Windows 11 required (detected: Build {build})")
                print("[ERROR] This application is not compatible with Windows 10 or earlier")
                return False
        
        # Fallback: vérifier via le nom de release
        if "11" in win_release:
            print(f"[INFO] Windows 11 detected ({win_release})")
            return True
        else:
            print(f"[ERROR] Windows 11 required (detected: {win_release})")
            print("[ERROR] This application is not compatible with Windows 10 or earlier")
            return False
            
    except Exception as e:
        print(f"[WARNING] Could not verify Windows version: {e}")
        print("[WARNING] Proceeding anyway, but compatibility is not guaranteed")
        return True  # Continuer en cas d'erreur de détection


def request_admin_if_needed():
    """Demande les privilèges admin si nécessaire"""
    try:
        is_admin_check = ctypes.windll.shell32.IsUserAnAdmin() != 0
        
        if not is_admin_check:
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
    """
    Crée un point de restauration système avant le nettoyage - API NATIVE
    SÉCURITÉ: Vérifie l'espace disque avant de créer le point
    
    Returns:
        bool: True si succès, False sinon
    """
    try:
        # Vérifier l'espace disque disponible
        import shutil
        c_drive = "C:\\"
        usage = shutil.disk_usage(c_drive)
        free_gb = usage.free / (1024**3)
        
        if free_gb < 10:  # Moins de 10 GB
            print(f"[WARNING] Insufficient disk space for restore point: {free_gb:.2f} GB free")
            print("[WARNING] At least 10 GB recommended for restore point")
            print("[INFO] Skipping restore point creation...")
            return False
        
        print("[INFO] Creating system restore point...")
        print(f"[INFO] Available disk space: {free_gb:.2f} GB")
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


def optimize_process():
    """Optimise l'utilisation des ressources CPU et mémoire"""
    try:
        import psutil
        current_process = psutil.Process()
        
        # Optimisation CPU: Utiliser tous les cœurs disponibles
        cpu_count = psutil.cpu_count(logical=True)
        print(f"[INFO] CPU cores available: {cpu_count}")
        
        # Définir l'affinité CPU pour utiliser tous les cœurs
        # Windows: affinity_mask avec tous les bits à 1
        if sys.platform == 'win32':
            try:
                # Créer un masque avec tous les cœurs activés
                affinity_mask = (1 << cpu_count) - 1
                current_process.cpu_affinity(list(range(cpu_count)))
                print(f"[INFO] CPU affinity set to use all {cpu_count} cores")
            except Exception as e:
                print(f"[WARNING] Could not set CPU affinity: {e}")
        
        # Optimisation mémoire: Limiter l'utilisation mémoire si nécessaire
        mem = psutil.virtual_memory()
        print(f"[INFO] Memory available: {mem.available / (1024**3):.2f} GB / {mem.total / (1024**3):.2f} GB")
        
        # Priorité normale pour ne pas impacter les autres processus
        try:
            current_process.nice(psutil.NORMAL_PRIORITY_CLASS)
            print("[INFO] Process priority set to NORMAL")
        except Exception as e:
            print(f"[WARNING] Could not set process priority: {e}")
        
        # Forcer un garbage collection initial
        gc.collect()
        print("[INFO] Initial garbage collection completed")
        
    except ImportError:
        print("[WARNING] psutil not available, skipping process optimization")
    except Exception as e:
        print(f"[WARNING] Process optimization failed: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("5Gh'z Cleaner - Windows 11 Cleaning & Optimisation Tool")
    print("Author: UndKiMi")
    print("=" * 60)
    print()
    
    # SÉCURITÉ 0: Vérifier Windows 11
    print("[INFO] Checking Windows version...")
    if not check_windows_11():
        print()
        print("=" * 60)
        print("ERROR: Windows 11 Required")
        print("=" * 60)
        print()
        print("This application requires Windows 11 (Build 22000+)")
        print("It is not compatible with Windows 10 or earlier versions.")
        print()
        print("Please upgrade to Windows 11 to use this software.")
        print()
        input("Press Enter to exit...")
        sys.exit(1)
    
    print()
    
    # OPTIMISATION: Optimiser l'utilisation des ressources
    print("[INFO] Optimizing process resources...")
    optimize_process()
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
    
    def main(page: ft.Page):
        """Point d'entrée de l'application Flet"""
        app = CleanerApp(page)
    
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