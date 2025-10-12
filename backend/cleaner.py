"""
Backend module for 5Gh'z Cleaner
Contains all cleaning and optimization functions
"""
import os
import sys
import ctypes
import shutil
import subprocess
from datetime import datetime, timedelta

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
    """Get the number of items in the recycle bin"""
    try:
        c = run_hidden(['PowerShell.exe', '-Command', '(Get-ChildItem -Path "Shell:RecycleBinFolder").Count'])
        return int(c.stdout.decode().strip())
    except (subprocess.SubprocessError, ValueError, AttributeError) as e:
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
    """Vérifie si le chemin est dans un dossier temp autorisé"""
    filepath_normalized = os.path.normpath(filepath).upper()
    
    for allowed in ALLOWED_TEMP_DIRS:
        if allowed:
            allowed_normalized = os.path.normpath(allowed).upper()
            if filepath_normalized.startswith(allowed_normalized):
                return True
    
    return False

def clear_temp(progress_callback=None):
    """Clear temporary files - SÉCURITÉ MAXIMALE - Ne touche JAMAIS aux fichiers système"""
    total = 0
    skipped = 0
    
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
                        # Vérifications de sécurité multiples
                        if is_file_safe_to_delete(fpath, f):
                            try:
                                os.unlink(fpath)
                                total += 1
                            except Exception as e:
                                skipped += 1
                        else:
                            skipped += 1
                            
                    elif os.path.isdir(fpath):
                        # Vérifications de sécurité pour dossiers
                        if is_folder_safe_to_delete(f, fpath):
                            try:
                                shutil.rmtree(fpath, ignore_errors=True)
                                total += 1
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
    
    print(f"[INFO] Temp cleanup: {total} deleted, {skipped} skipped (protected)")
    return {"temp_deleted": total, "skipped": skipped}


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


def empty_recycle_bin(progress_callback=None):
    """Empty the Windows recycle bin"""
    before = get_recycle_bin_count()
    run_hidden(['PowerShell.exe', '-Command', 'Clear-RecycleBin -Force'])
    return {"recycle_bin_deleted": before}


def stop_services(services, progress_callback=None):
    """Stop specified Windows services"""
    stopped = []
    for s in services:
        if run_hidden(['sc', 'stop', s]).returncode == 0:
            stopped.append(s)
    return {"services_stopped": stopped}


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


def clear_windows_old(progress_callback=None):
    """Remove Windows.old folder from previous installations"""
    folder = os.path.normpath(os.path.join(os.getenv('WINDIR'), '..', 'Windows.old'))
    deleted = 0
    
    if os.path.isdir(folder):
        try:
            shutil.rmtree(folder, ignore_errors=True)
            deleted = 1
        except:
            pass
    
    return {'windows_old_deleted': deleted}


# Advanced functions
def clear_standby_memory(progress_callback=None):
    """Clear standby memory (RAM)"""
    try:
        result = run_hidden(["powershell", "-Command", "Clear-PhysicalMemoryStandbyList"])
        return {"ram_standby_cleared": result.returncode == 0}
    except (subprocess.SubprocessError, FileNotFoundError) as e:
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


# Services to stop
SERVICES_TO_STOP = ["Fax", "MapsBroker", "WMPNetworkSvc", "Spooler", "RemoteRegistry"]


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
    
    # Empty recycle bin
    results['recycle'] = empty_recycle_bin()
    
    return results
