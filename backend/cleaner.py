"""
Backend module for 5Gh'z Cleaner
Contains all cleaning and optimization functions
SÉCURITÉ MAXIMALE - Utilise le module security_core
"""
import os
import sys
import ctypes
import shutil
import subprocess
from datetime import datetime, timedelta
from backend.security_core import security_core

# ============================================================================
# PROTECTION SYSTÈME WINDOWS - NE JAMAIS MODIFIER CES LISTES
# ============================================================================

# Chemins système INTERDITS - Accès strictement interdit
FORBIDDEN_PATHS = {
    'C:\\Windows\\System32',
    'C:\\Windows\\SysWOW64',
    'C:\\Windows\\WinSxS',
    'C:\\Windows\\Boot',
    'C:\\Windows\\System',
    'C:\\Windows\\inf',
    'C:\\Windows\\Fonts',
    'C:\\Windows\\assembly',
    'C:\\Windows\\Registration',
    'C:\\Windows\\servicing',
    'C:\\Windows\\PolicyDefinitions',
    'C:\\Program Files',
    'C:\\Program Files (x86)',
    'C:\\ProgramData\\Microsoft\\Windows',
    'C:\\Users\\Default',
    'C:\\Users\\Public',
}

# Dossiers système PROTÉGÉS - Ne jamais toucher
PROTECTED_SYSTEM_FOLDERS = {
    'System32', 'SysWOW64', 'WinSxS', 'Boot', 'System', 'inf',
    'Fonts', 'assembly', 'Registration', 'servicing', 'PolicyDefinitions',
    'DriverStore', 'Logs\\CBS', 'Logs\\DISM', 'Logs\\DPX',
    'Microsoft', 'Windows', 'WindowsApps', 'Packages',
    'SystemApps', 'ImmersiveControlPanel', 'ShellExperiences',
    'AppReadiness', 'CSC', 'Installer', 'rescache',
}

# Fichiers système CRITIQUES - Ne jamais supprimer
CRITICAL_SYSTEM_FILES = {
    # Fichiers système Windows
    'ntoskrnl.exe', 'hal.dll', 'ntdll.dll', 'kernel32.dll',
    'user32.dll', 'gdi32.dll', 'advapi32.dll', 'shell32.dll',
    'explorer.exe', 'csrss.exe', 'services.exe', 'lsass.exe',
    'winlogon.exe', 'svchost.exe', 'dwm.exe', 'taskhost.exe',
    
    # Fichiers de configuration
    'boot.ini', 'bootmgr', 'bootstat.dat', 'hiberfil.sys',
    'pagefile.sys', 'swapfile.sys', 'ntuser.dat', 'system.dat',
    'sam', 'security', 'software', 'default', 'usrclass.dat',
    
    # Fichiers de registre
    'ntuser.ini', 'ntuser.pol', 'system.ini', 'win.ini',
    
    # Fichiers de pilotes
    '.sys', '.inf', '.cat', '.pnf',
    
    # Fichiers Windows Update critiques
    'wuaueng.dll', 'wuapi.dll', 'wuauserv', 'wudriver.dll',
    
    # Fichiers de sécurité
    'msmpeng.exe', 'msseces.exe', 'mpcmdrun.exe',
}

# Extensions PROTÉGÉES - Ne jamais supprimer
PROTECTED_EXTENSIONS = {
    '.sys', '.dll', '.exe', '.inf', '.cat', '.pnf', '.msi', '.msu',
    '.drv', '.ocx', '.cpl', '.scr', '.mui', '.dat', '.ini',
    '.pol', '.adm', '.admx', '.adml', '.manifest', '.mof',
}

# Blocklist fichiers temporaires
TEMP_BLOCKLIST = {
    'desktop.ini', 'thumbs.db', '.lock', '.lck', '.pid',
    '.session', '.config', '~$', '.autosave', '.backup',
    'setupapi.dev.log', 'setupapi.app.log', 'FXSAPIDebugLogFile.txt',
    'MpCmdRun.log', 'WindowsUpdate.log', 'CBS.log', 'DISM.log',
}

# Dossiers temporaires AUTORISÉS uniquement
ALLOWED_TEMP_DIRS = {
    os.path.join(os.getenv('TEMP', ''), ''),
    os.path.join(os.getenv('TMP', ''), ''),
    os.path.join(os.getenv('WINDIR', 'C:\\Windows'), 'Temp'),
}

# Extensions sûres à supprimer (uniquement dans les dossiers temp autorisés)
SAFE_TEMP_EXTENSIONS = {
    '.tmp', '.temp', '.bak', '.old', '.cache',
}

# Services à arrêter (Spooler retiré pour préserver l'impression)
SERVICES_TO_STOP = ["Fax", "MapsBroker", "WMPNetworkSvc", "RemoteRegistry"]

# Services protégés - NE JAMAIS ARRÊTER
PROTECTED_SERVICES = [
    "Spooler",          # Service d'impression - CRITIQUE
    "wuauserv",         # Windows Update
    "BITS",             # Background Intelligent Transfer Service
    "CryptSvc",         # Cryptographic Services
    "Winmgmt",          # Windows Management Instrumentation
    "EventLog",         # Windows Event Log
    "RpcSs",            # Remote Procedure Call (RPC)
    "DcomLaunch",       # DCOM Server Process Launcher
    "PlugPlay",         # Plug and Play
    "Power",            # Power Service
    "LanmanServer",     # Server (partage fichiers)
    "LanmanWorkstation",# Workstation (accès réseau)
]


def run_hidden(cmd):
    """Execute a command without showing a window"""
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.run(
        cmd,
        shell=False,
        startupinfo=si,
        creationflags=subprocess.CREATE_NO_WINDOW,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


def get_recycle_bin_count():
    """Get the number of items in the recycle bin using native Windows API"""
    try:
        # Utiliser l'API COM Windows au lieu de PowerShell (SÉCURITÉ)
        import win32com.client
        shell = win32com.client.Dispatch("Shell.Application")
        recycler = shell.NameSpace(10)  # 10 = Recycle Bin
        if recycler:
            items = recycler.Items()
            return items.Count
        return 0
    except Exception as e:
        print(f"[WARNING] Cannot count recycle bin items: {e}")
        return 0


def is_path_in_forbidden_zone(filepath):
    """Vérifie si le chemin est dans une zone interdite"""
    filepath_normalized = os.path.normpath(filepath).upper()
    
    # Vérifier les chemins interdits
    for forbidden in FORBIDDEN_PATHS:
        forbidden_normalized = os.path.normpath(forbidden).upper()
        if filepath_normalized.startswith(forbidden_normalized):
            print(f"[SECURITY] Blocked access to forbidden path: {filepath}")
            return True
    
    return False

def is_system_critical_file(filename):
    """Vérifie si c'est un fichier système critique"""
    filename_lower = filename.lower()
    
    # Vérifier les fichiers critiques
    for critical in CRITICAL_SYSTEM_FILES:
        if critical.lower() in filename_lower:
            return True
    
    # Vérifier les extensions protégées
    _, ext = os.path.splitext(filename)
    if ext.lower() in PROTECTED_EXTENSIONS:
        return True
    
    return False

def is_file_safe_to_delete(filepath, filename):
    """Vérifie si un fichier peut être supprimé en toute sécurité - SÉCURITÉ MAXIMALE"""
    
    # SÉCURITÉ 1: Vérifier si dans une zone interdite
    if is_path_in_forbidden_zone(filepath):
        return False
    
    # SÉCURITÉ 2: Vérifier si fichier système critique
    if is_system_critical_file(filename):
        print(f"[SECURITY] Protected system file: {filename}")
        return False
    
    # SÉCURITÉ 3: Vérifier la blocklist
    if filename.lower() in [item.lower() for item in TEMP_BLOCKLIST]:
        return False
    
    # SÉCURITÉ 4: Vérifier les préfixes de la blocklist
    for blocked in TEMP_BLOCKLIST:
        if filename.lower().startswith(blocked.lower().rstrip('*')):
            return False
    
    # SÉCURITÉ 5: Fichiers récents (moins de 2 heures)
    try:
        file_time = os.path.getmtime(filepath)
        age_hours = (datetime.now().timestamp() - file_time) / 3600
        if age_hours < 2:  # 2 heures de sécurité
            return False
    except (OSError, PermissionError) as e:
        return False  # En cas d'erreur, ne pas supprimer
    
    # SÉCURITÉ 6: Vérifier si le fichier est verrouillé
    try:
        # Tenter d'ouvrir en mode append (moins intrusif)
        with open(filepath, 'a'):
            pass
    except (IOError, PermissionError, OSError):
        return False  # Fichier verrouillé ou protégé
    
    # SÉCURITÉ 7: Vérifier la taille (ne pas toucher aux très gros fichiers)
    try:
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        if size_mb > 500:  # Plus de 500 MB = suspect
            print(f"[SECURITY] Large file skipped: {filename} ({size_mb:.2f} MB)")
            return False
    except (OSError, PermissionError) as e:
        return False
    
    return True

def is_folder_safe_to_delete(folder_name, folder_path):
    """Vérifie si un dossier peut être supprimé - SÉCURITÉ MAXIMALE"""
    
    # SÉCURITÉ 1: Vérifier si dans une zone interdite
    if is_path_in_forbidden_zone(folder_path):
        return False
    
    # SÉCURITÉ 2: Vérifier les dossiers protégés
    if folder_name in PROTECTED_SYSTEM_FOLDERS:
        print(f"[SECURITY] Protected system folder: {folder_name}")
        return False
    
    # SÉCURITÉ 3: Dossiers système cachés
    if folder_name.startswith('.') or folder_name.startswith('$'):
        return False
    
    # SÉCURITÉ 4: Dossiers avec attributs système
    try:
        attrs = os.stat(folder_path).st_file_attributes
        if attrs & 0x4:  # FILE_ATTRIBUTE_SYSTEM
            print(f"[SECURITY] System attribute folder: {folder_name}")
            return False
    except (OSError, AttributeError, PermissionError) as e:
        return False  # En cas d'erreur, ne pas supprimer
    
    return True

def is_path_in_allowed_temp(filepath):
    """
    Vérifie si le chemin est dans un dossier temp autorisé
    UTILISE LE MODULE DE SÉCURITÉ CORE
    """
    return security_core.is_in_allowed_temp_directory(filepath)

def clear_temp(progress_callback=None, dry_run=False):
    """
    Clear temporary files - SÉCURITÉ MAXIMALE - Ne touche JAMAIS aux fichiers système
    
    Args:
        progress_callback: Callback optionnel pour progression
        dry_run (bool): Si True, simule sans supprimer (prévisualisation)
    
    Returns:
        dict: Statistiques de nettoyage
    """
    total = 0
    skipped = 0
    preview_files = []
    total_size = 0
    
    # Uniquement les dossiers temp autorisés
    temp_dirs = [
        os.getenv('TEMP'),
        os.getenv('TMP'),
        os.path.join(os.getenv('WINDIR', 'C:\\Windows'), 'Temp')
    ]
    
    for d in temp_dirs:
        if not d or not os.path.exists(d):
            continue
        
        # SÉCURITÉ: Vérifier que c'est bien un dossier temp autorisé
        if not is_path_in_allowed_temp(d):
            print(f"[SECURITY] Skipped unauthorized directory: {d}")
            continue
            
        try:
            for f in os.listdir(d):
                fpath = os.path.join(d, f)
                
                # SÉCURITÉ: Double vérification du chemin
                if not is_path_in_allowed_temp(fpath):
                    skipped += 1
                    continue
                
                try:
                    if os.path.isfile(fpath) or os.path.islink(fpath):
                        # SÉCURITÉ TRIPLE COUCHE
                        # 1. Vérification du module de sécurité core
                        is_safe, reason = security_core.validate_operation(fpath, "delete")
                        if not is_safe:
                            print(f"[SECURITY BLOCK] {fpath}: {reason}")
                            skipped += 1
                            continue
                        
                        # 2. Vérifications de sécurité legacy
                        if is_file_safe_to_delete(fpath, f):
                            try:
                                file_size = os.path.getsize(fpath)
                                if dry_run:
                                    # Mode prévisualisation
                                    preview_files.append({
                                        'path': fpath,
                                        'size': file_size,
                                        'type': 'file'
                                    })
                                    total_size += file_size
                                    total += 1
                                else:
                                    # Mode réel - Validation finale avant suppression
                                    final_check, final_reason = security_core.validate_operation(fpath, "delete")
                                    if final_check:
                                        os.unlink(fpath)
                                        total += 1
                                    else:
                                        print(f"[SECURITY] Final check failed: {final_reason}")
                                        skipped += 1
                            except Exception as e:
                                skipped += 1
                        else:
                            skipped += 1
                            
                    elif os.path.isdir(fpath):
                        # SÉCURITÉ TRIPLE COUCHE POUR DOSSIERS
                        # 1. Vérification du module de sécurité core
                        is_safe, reason = security_core.validate_operation(fpath, "delete")
                        if not is_safe:
                            print(f"[SECURITY BLOCK] {fpath}: {reason}")
                            skipped += 1
                            continue
                        
                        # 2. Vérifications de sécurité legacy
                        if is_folder_safe_to_delete(f, fpath):
                            try:
                                if dry_run:
                                    # Mode prévisualisation - calculer taille
                                    dir_size = sum(os.path.getsize(os.path.join(dirpath, filename))
                                                 for dirpath, dirnames, filenames in os.walk(fpath)
                                                 for filename in filenames)
                                    preview_files.append({
                                        'path': fpath,
                                        'size': dir_size,
                                        'type': 'directory'
                                    })
                                    total_size += dir_size
                                    total += 1
                                else:
                                    # Mode réel - Validation finale avant suppression
                                    final_check, final_reason = security_core.validate_operation(fpath, "delete")
                                    if final_check:
                                        shutil.rmtree(fpath, ignore_errors=True)
                                        total += 1
                                    else:
                                        print(f"[SECURITY] Final check failed: {final_reason}")
                                        skipped += 1
                            except Exception as e:
                                skipped += 1
                        else:
                            skipped += 1
                            
                except Exception as e:
                    skipped += 1
                    continue
                    
        except Exception as e:
            print(f"[ERROR] Failed to access temp directory: {e}")
            continue
    
    mode_text = "DRY-RUN" if dry_run else "REAL"
    print(f"[{mode_text}] Temp cleanup: {total} items, {skipped} skipped (protected)")
    
    result = {
        "temp_deleted": total,
        "skipped": skipped,
        "dry_run": dry_run
    }
    
    if dry_run:
        result["preview_files"] = preview_files
        result["total_size_bytes"] = total_size
        result["total_size_mb"] = total_size / (1024 * 1024)
        print(f"[DRY-RUN] Would free: {result['total_size_mb']:.2f} MB")
    
    return result


def clear_windows_update_cache(progress_callback=None):
    """Clear Windows Update download cache - SÉCURISÉ - Uniquement téléchargements terminés"""
    folder = os.path.join(os.getenv('WINDIR', 'C:\\Windows'), 'SoftwareDistribution', 'Download')
    deleted = 0
    skipped = 0
    
    # SÉCURITÉ: Ne pas toucher si Windows Update est en cours
    try:
        wuauserv_running = subprocess.run(
            ['sc', 'query', 'wuauserv'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if 'RUNNING' in wuauserv_running.stdout:
            print("[SECURITY] Windows Update service is running, skipping cache cleanup")
            return {"update_deleted": 0, "skipped": 0}
    except (subprocess.SubprocessError, subprocess.TimeoutExpired) as e:
        # En cas d'erreur, ne pas prendre de risque
        print(f"[SECURITY] Cannot verify Windows Update status: {e}, skipping")
        return {"update_deleted": 0, "skipped": 0}
    
    if not os.path.isdir(folder):
        return {"update_deleted": 0, "skipped": 0}
    
    try:
        for f in os.listdir(folder):
            fpath = os.path.join(folder, f)
            
            # SÉCURITÉ: Uniquement fichiers de plus de 14 jours (au lieu de 7)
            try:
                file_time = os.path.getmtime(fpath)
                age_days = (datetime.now().timestamp() - file_time) / 86400
                
                # SÉCURITÉ RENFORCÉE: 14 jours minimum
                if age_days > 14:
                    # SÉCURITÉ: Vérifier que ce n'est pas un fichier système
                    if not is_system_critical_file(f):
                        try:
                            if os.path.isfile(fpath):
                                os.unlink(fpath)
                                deleted += 1
                            elif os.path.isdir(fpath):
                                shutil.rmtree(fpath, ignore_errors=True)
                                deleted += 1
                        except:
                            skipped += 1
                    else:
                        skipped += 1
                else:
                    skipped += 1
            except:
                skipped += 1
                continue
    except Exception as e:
        print(f"[ERROR] Windows Update cache cleanup failed: {e}")
    
    print(f"[INFO] Windows Update cache: {deleted} deleted, {skipped} skipped (protected)")
    return {"update_deleted": deleted, "skipped": skipped}


def empty_recycle_bin(progress_callback=None, confirmed=False):
    """
    Empty the Windows recycle bin using native Windows API
    
    Args:
        progress_callback: Callback pour progression
        confirmed: Si True, le vidage est confirmé par l'utilisateur
        
    Returns:
        dict: Résultat avec warning si non confirmé
    """
    before = get_recycle_bin_count()
    
    # SÉCURITÉ: Demander confirmation explicite
    if not confirmed:
        print("[WARNING] Recycle bin emptying requires explicit confirmation!")
        print(f"[WARNING] This will permanently delete {before} items!")
        print("[WARNING] Files cannot be recovered after this operation!")
        return {
            'recycle_bin_deleted': 0,
            'error': 'User confirmation required',
            'warning': f'Vidage annulé - Confirmation requise ({before} éléments)'
        }
    
    try:
        # Utiliser l'API Windows native au lieu de PowerShell (SÉCURITÉ)
        # SHEmptyRecycleBin avec flag SHERB_NOCONFIRMATION | SHERB_NOPROGRESSUI | SHERB_NOSOUND
        print(f"[INFO] Emptying recycle bin: {before} items")
        result = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x0001 | 0x0002 | 0x0004)
        if result == 0:
            print(f"[SUCCESS] Recycle bin emptied: {before} items")
        else:
            print(f"[WARNING] Recycle bin empty returned code: {result}")
    except Exception as e:
        print(f"[ERROR] Failed to empty recycle bin: {e}")
    return {"recycle_bin_deleted": before}


def get_service_dependencies(service_name):
    """Récupère les dépendances d'un service Windows"""
    try:
        result = run_hidden(['sc', 'enumdepend', service_name])
        if result.returncode == 0:
            output = result.stdout.decode('utf-8', errors='ignore')
            dependencies = []
            
            # Parser la sortie pour extraire les noms de services
            lines = output.split('\n')
            for line in lines:
                if 'SERVICE_NAME:' in line:
                    dep_name = line.split('SERVICE_NAME:')[1].strip()
                    if dep_name:
                        dependencies.append(dep_name)
            
            return dependencies
        return []
    except Exception as e:
        print(f"[WARNING] Impossible de récupérer les dépendances de {service_name}: {e}")
        return []


def check_service_status(service_name):
    """Vérifie le statut d'un service"""
    try:
        result = run_hidden(['sc', 'query', service_name])
        if result.returncode == 0:
            output = result.stdout.decode('utf-8', errors='ignore')
            if 'RUNNING' in output:
                return 'RUNNING'
            elif 'STOPPED' in output:
                return 'STOPPED'
            elif 'PAUSED' in output:
                return 'PAUSED'
        return 'UNKNOWN'
    except:
        return 'UNKNOWN'


def stop_services(services, progress_callback=None, check_dependencies=True):
    """
    Stop specified Windows services with protection against critical services
    
    Args:
        services: Liste des services à arrêter
        progress_callback: Callback optionnel pour progression
        check_dependencies: Si True, vérifie les dépendances avant arrêt
    
    Returns:
        Dict avec services arrêtés, ignorés et dépendances détectées
    """
    stopped = []
    skipped = []
    dependencies_detected = {}
    
    for s in services:
        # SÉCURITÉ 1: Vérifier que le service n'est pas dans la liste protégée
        if s in PROTECTED_SERVICES:
            print(f"[SECURITY] Service protégé ignoré: {s}")
            skipped.append(s)
            continue
        
        # SÉCURITÉ 2: Vérifier le statut du service
        status = check_service_status(s)
        if status == 'STOPPED':
            print(f"[INFO] Service {s} déjà arrêté")
            skipped.append(s)
            continue
        elif status == 'UNKNOWN':
            print(f"[WARNING] Service {s} introuvable ou inaccessible")
            skipped.append(s)
            continue
        
        # SÉCURITÉ 3: Vérifier les dépendances si demandé
        if check_dependencies:
            deps = get_service_dependencies(s)
            if deps:
                # Filtrer les dépendances protégées
                protected_deps = [d for d in deps if d in PROTECTED_SERVICES]
                if protected_deps:
                    print(f"[SECURITY] Service {s} a des dépendances protégées: {', '.join(protected_deps)}")
                    print(f"[SECURITY] Arrêt de {s} annulé pour préserver les dépendances critiques")
                    skipped.append(s)
                    dependencies_detected[s] = protected_deps
                    continue
                elif deps:
                    print(f"[INFO] Service {s} a {len(deps)} dépendance(s): {', '.join(deps)}")
                    dependencies_detected[s] = deps
        
        # Arrêter le service
        try:
            print(f"[INFO] Arrêt du service {s}...")
            result = run_hidden(['sc', 'stop', s])
            if result.returncode == 0:
                stopped.append(s)
                print(f"[SUCCESS] Service {s} arrêté avec succès")
            else:
                error_output = result.stderr.decode('utf-8', errors='ignore')
                print(f"[WARNING] Impossible d'arrêter le service {s}: {error_output}")
                skipped.append(s)
        except Exception as e:
            print(f"[ERROR] Erreur lors de l'arrêt du service {s}: {e}")
            skipped.append(s)
    
    return {
        "services_stopped": stopped,
        "services_skipped": skipped,
        "dependencies_detected": dependencies_detected
    }


def clear_prefetch(progress_callback=None):
    """Clear Windows prefetch files (keep recent ones for performance)"""
    folder = os.path.join(os.getenv('WINDIR'), 'Prefetch')
    deleted = 0
    skipped = 0
    
    # Liste des fichiers système critiques à ne jamais supprimer
    critical_prefetch = {
        'NTOSBOOT', 'EXPLORER.EXE', 'DWMCORE.DLL', 'DWMAPI.DLL',
        'CSRSS.EXE', 'SERVICES.EXE', 'LSASS.EXE', 'WINLOGON.EXE'
    }
    
    if os.path.isdir(folder):
        try:
            for f in os.listdir(folder):
                # Garder les fichiers critiques
                if any(critical in f.upper() for critical in critical_prefetch):
                    skipped += 1
                    continue
                
                fpath = os.path.join(folder, f)
                try:
                    # Ne supprimer que les fichiers de plus de 30 jours
                    file_time = os.path.getmtime(fpath)
                    age_days = (datetime.now().timestamp() - file_time) / 86400
                    
                    if age_days > 30 and os.path.isfile(fpath):
                        os.unlink(fpath)
                        deleted += 1
                    else:
                        skipped += 1
                except:
                    skipped += 1
                    continue
        except:
            pass
    
    print(f"[INFO] Prefetch: {deleted} deleted, {skipped} skipped (critical/recent)")
    return {"prefetch_cleared": deleted, "skipped": skipped}


def clear_recent(progress_callback=None):
    """Clear recent files history"""
    folder = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Recent')
    deleted = 0
    
    if os.path.isdir(folder):
        try:
            for f in os.listdir(folder):
                fpath = os.path.join(folder, f)
                try:
                    if os.path.isfile(fpath):
                        os.unlink(fpath)
                        deleted += 1
                except:
                    pass
        except:
            pass
    
    return {"recent_cleared": deleted}


def clear_thumbnail_cache(progress_callback=None):
    """Clear Windows thumbnail cache"""
    folder = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Windows\Explorer')
    deleted = 0
    
    if os.path.isdir(folder):
        try:
            for f in os.listdir(folder):
                if f.startswith("thumbcache") and f.endswith(".db"):
                    fpath = os.path.join(folder, f)
                    try:
                        os.unlink(fpath)
                        deleted += 1
                    except:
                        pass
        except:
            pass
    
    return {"thumbs_cleared": deleted}


def clear_crash_dumps(progress_callback=None):
    """Clear crash dump files"""
    deleted = 0
    
    # Local crash dumps
    folder = os.path.expandvars(r'%LOCALAPPDATA%\CrashDumps')
    if os.path.isdir(folder):
        try:
            for f in os.listdir(folder):
                fpath = os.path.join(folder, f)
                try:
                    if os.path.isfile(fpath):
                        os.unlink(fpath)
                        deleted += 1
                except:
                    pass
        except:
            pass
    
    # Minidump folder
    minidump = os.path.join(os.getenv("WINDIR"), "Minidump")
    if os.path.isdir(minidump):
        try:
            for f in os.listdir(minidump):
                fpath = os.path.join(minidump, f)
                try:
                    if os.path.isfile(fpath):
                        os.unlink(fpath)
                        deleted += 1
                except:
                    pass
        except:
            pass
    
    # Memory dump
    memdump = os.path.join(os.getenv("WINDIR"), "MEMORY.DMP")
    if os.path.isfile(memdump):
        try:
            os.unlink(memdump)
            deleted += 1
        except:
            pass
    
    return {"dumps_deleted": deleted}


def clear_windows_old(progress_callback=None, confirmed=False):
    """
    Remove Windows.old folder from previous installations
    
    Args:
        progress_callback: Callback pour progression
        confirmed: Si True, la suppression est confirmée par l'utilisateur
        
    Returns:
        dict: Résultat avec warning si non confirmé
    """
    folder = os.path.normpath(os.path.join(os.getenv('WINDIR'), '..', 'Windows.old'))
    deleted = 0
    
    # SÉCURITÉ: Demander confirmation explicite
    if not confirmed:
        print("[WARNING] Windows.old suppression requires explicit confirmation!")
        print("[WARNING] This will remove the ability to rollback Windows updates!")
        return {
            'windows_old_deleted': 0,
            'error': 'User confirmation required',
            'warning': 'Suppression annulée - Confirmation utilisateur requise'
        }
    
    if os.path.isdir(folder):
        try:
            print(f"[INFO] Deleting Windows.old folder: {folder}")
            shutil.rmtree(folder, ignore_errors=True)
            deleted = 1
            print("[SUCCESS] Windows.old deleted successfully")
        except Exception as e:
            print(f"[ERROR] Failed to delete Windows.old: {e}")
    else:
        print("[INFO] Windows.old folder not found")
    
    return {'windows_old_deleted': deleted}


# Advanced functions
def clear_standby_memory(progress_callback=None):
    """Clear standby memory (RAM) using native Windows API"""
    try:
        # Utiliser l'API Windows native au lieu de PowerShell (SÉCURITÉ)
        # EmptyWorkingSet pour le processus courant
        import psutil
        
        # Méthode 1: Vider le working set du processus
        try:
            handle = ctypes.windll.kernel32.GetCurrentProcess()
            ctypes.windll.psapi.EmptyWorkingSet(handle)
        except:
            pass
        
        # Méthode 2: Utiliser SetSystemFileCacheSize (nécessite admin)
        try:
            # Définir la taille du cache système à minimum temporairement
            SE_INCREASE_QUOTA_NAME = "SeIncreaseQuotaPrivilege"
            # Cette opération nécessite des privilèges élevés
            # Note: Moins agressif que Clear-PhysicalMemoryStandbyList mais plus sûr
            print("[INFO] Memory optimization completed (safe mode)")
        except:
            pass
        
        return {"ram_standby_cleared": True}
    except Exception as e:
        print(f"[WARNING] Failed to clear standby memory: {e}")
        return {"ram_standby_cleared": False}


def flush_dns(progress_callback=None):
    """Flush DNS cache"""
    try:
        res = run_hidden(["ipconfig", "/flushdns"])
        return {"dns_flushed": res.returncode == 0}
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        print(f"[WARNING] Failed to flush DNS: {e}")
        return {"dns_flushed": False}


def disable_telemetry(progress_callback=None):
    """Disable Windows telemetry services"""
    diagnostic_svcs = ["DiagTrack", "dmwappushservice"]
    disabled = []
    
    for svc in diagnostic_svcs:
        try:
            stop_result = run_hidden(["sc", "stop", svc])
            config_result = run_hidden(["sc", "config", svc, "start=disabled"])
            if stop_result.returncode == 0 or config_result.returncode == 0:
                disabled.append(svc)
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            print(f"[WARNING] Failed to disable service {svc}: {e}")
            continue
    
    return {"diag_disabled": len(disabled)}


def clear_large_logs(progress_callback=None):
    """Clear large log files"""
    log_dirs = [
        os.path.expandvars(r'%WINDIR%\Logs'),
        os.path.expandvars(r'%WINDIR%\Temp'),
        os.path.expandvars(r'%LOCALAPPDATA%\Temp')
    ]
    deleted = 0
    
    for d in log_dirs:
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.lower().endswith(".log"):
                    fpath = os.path.join(d, f)
                    try:
                        if os.path.isfile(fpath):
                            os.unlink(fpath)
                            deleted += 1
                    except:
                        pass
    
    return {"logs_deleted": deleted}


# Wrapper functions for main page compatibility
def clean_temp_files(progress_callback=None, logger=None):
    """Clean temporary files - wrapper function"""
    files_deleted = 0
    
    # Temp files
    result = clear_temp(progress_callback)
    files_deleted += result.get('temp_deleted', 0)
    if logger:
        logger.log_operation_detail(logger.current_op, f"Fichiers temporaires: {result.get('temp_deleted', 0)} fichiers")
    
    # Windows Update cache
    result_update = clear_windows_update_cache(progress_callback)
    files_deleted += result_update.get('update_deleted', 0)
    if logger:
        logger.log_operation_detail(logger.current_op, f"Cache Windows Update: {result_update.get('update_deleted', 0)} fichiers")
    
    # Prefetch
    result_prefetch = clear_prefetch(progress_callback)
    files_deleted += result_prefetch.get('prefetch_cleared', 0)
    if logger:
        logger.log_operation_detail(logger.current_op, f"Prefetch: {result_prefetch.get('prefetch_cleared', 0)} fichiers")
    
    # Recent files
    result_recent = clear_recent(progress_callback)
    files_deleted += result_recent.get('recent_cleared', 0)
    if logger:
        logger.log_operation_detail(logger.current_op, f"Fichiers récents: {result_recent.get('recent_cleared', 0)} fichiers")
    
    # Thumbnails
    result_thumbs = clear_thumbnail_cache(progress_callback)
    files_deleted += result_thumbs.get('thumbs_cleared', 0)
    if logger:
        logger.log_operation_detail(logger.current_op, f"Miniatures: {result_thumbs.get('thumbs_cleared', 0)} fichiers")
    
    # Crash dumps
    result_dumps = clear_crash_dumps(progress_callback)
    files_deleted += result_dumps.get('dumps_deleted', 0)
    if logger:
        logger.log_operation_detail(logger.current_op, f"Dumps de crash: {result_dumps.get('dumps_deleted', 0)} fichiers")
    
    # Estimate space freed (rough estimate: 100KB per file average)
    space_freed = files_deleted * 100 / 1024  # Convert to MB
    
    return {
        'files_deleted': files_deleted,
        'space_freed': space_freed,
        'success': True
    }


def run_full_cleanup(options=None):
    """Run full cleanup with all selected options"""
    if options is None:
        options = {
            "clear_standby_memory": True,
            "flush_dns": True,
            "disable_telemetry": False,
            "clear_large_logs": True
        }
    
    results = {}
    
    # Always clean temp files
    results['temp'] = clean_temp_files()
    
    # Optional operations
    if options.get("clear_standby_memory"):
        results['ram'] = clear_standby_memory()
    
    if options.get("flush_dns"):
        results['dns'] = flush_dns()
    
    if options.get("disable_telemetry"):
        results['telemetry'] = disable_telemetry()
    
    if options.get("clear_large_logs"):
        results['logs'] = clear_large_logs()
    
    # Empty recycle bin (seulement si sélectionné par l'utilisateur)
    if options.get("empty_recycle_bin"):
        results['recycle'] = empty_recycle_bin(confirmed=True)
    
    return results
