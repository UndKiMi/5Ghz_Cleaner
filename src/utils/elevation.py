"""
Elevation module for requesting administrator privileges
Supports conditional elevation based on required operations
Version 1.7.0 - Validation post-élévation ajoutée
"""
import sys
import ctypes


class SecurityError(Exception):
    """Exception levée en cas d'erreur de sécurité"""
    pass


def is_admin():
    """Check if the current process has administrator privileges"""
    try:
        result = ctypes.windll.shell32.IsUserAnAdmin()
        print(f"[INFO] Administrator check result: {result}")
        return result
    except Exception as e:
        print(f"[WARNING] Failed to check admin privileges: {e}")
        return False


def elevate(force=False):
    """
    Request administrator privileges if not already elevated
    
    Args:
        force (bool): If True, force elevation. If False, just check and inform.
    """
    try:
        if not is_admin():
            if force:
                print("[WARNING] Application not running as administrator")
                print("[INFO] Requesting UAC elevation...")
                params = ' '.join([f'"{arg}"' for arg in sys.argv])
                ctypes.windll.shell32.ShellExecuteW(
                    None, 
                    "runas", 
                    sys.executable, 
                    params, 
                    None, 
                    1
                )
                print("[INFO] UAC prompt displayed, waiting for user response...")
                sys.exit(0)
            else:
                print("[INFO] Running in standard user mode")
                print("[INFO] Some operations will require administrator privileges")
                return False
        else:
            print("[SUCCESS] Application running with administrator privileges")
            return True
    except Exception as e:
        print(f"[ERROR] Elevation failed: {e}")
        if force:
            sys.exit(0)
        return False


def elevate_with_validation(force=True):
    """
    Élève les privilèges avec validation post-élévation
    
    Args:
        force: Si True, force l'élévation
        
    Returns:
        bool: True si élévation réussie et validée
        
    Raises:
        SecurityError: Si l'élévation échoue ou n'est pas validée
    """
    print("[SECURITY] Requesting privilege elevation with validation...")
    
    # Tenter l'élévation
    if elevate(force=force):
        # Vérifier que l'élévation a réussi
        if not is_admin():
            error_msg = "Elevation failed: Process does not have admin rights after elevation"
            print(f"[CRITICAL] {error_msg}")
            raise SecurityError(error_msg)
        
        print("[SUCCESS] Elevation validated successfully")
        return True
    else:
        if force:
            error_msg = "Elevation was required but failed"
            print(f"[CRITICAL] {error_msg}")
            raise SecurityError(error_msg)
        return False


def elevate_if_needed(operation_type="standard"):
    """
    Conditionally request elevation based on operation type
    
    Args:
        operation_type (str): Type of operation
            - "standard": User temp files only (no admin needed)
            - "system": System-wide cleaning (admin required)
            - "services": Service management (admin required)
    
    Returns:
        bool: True if has admin rights or not needed, False otherwise
    """
    # Operations qui ne nécessitent PAS d'admin
    non_admin_operations = ["standard", "user", "preview", "dry-run"]
    
    if operation_type in non_admin_operations:
        print(f"[INFO] Operation '{operation_type}' does not require administrator privileges")
        return True
    
    # Operations qui nécessitent admin
    if not is_admin():
        print(f"[WARNING] Operation '{operation_type}' requires administrator privileges")
        print("[INFO] Please restart the application as administrator")
        return False
    
    return True


# Liste des opérations par niveau de privilège
OPERATIONS_NO_ADMIN = [
    "clear_user_temp",           # Fichiers temp utilisateur
    "clear_user_recent",         # Historique utilisateur
    "clear_user_thumbnails",     # Cache miniatures utilisateur
    "preview_cleaning",          # Prévisualisation (dry-run)
    "view_logs",                 # Consultation logs
]

OPERATIONS_REQUIRE_ADMIN = [
    "clear_system_temp",         # Fichiers temp système
    "clear_windows_update",      # Cache Windows Update
    "clear_prefetch",            # Prefetch système
    "clear_windows_old",         # Windows.old
    "stop_services",             # Arrêt services
    "disable_telemetry",         # Désactivation télémétrie
    "clear_system_logs",         # Logs système
    "empty_recycle_bin",         # Corbeille (toutes partitions)
    "clear_standby_memory",      # RAM Standby
    "flush_dns",                 # Cache DNS
]
