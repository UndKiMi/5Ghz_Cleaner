"""
Solution complète et fiable pour EmptyStandbyList sous Windows
Corrige ERROR_INVALID_HANDLE (6) et STATUS_PRIVILEGE_NOT_HELD (0xC0000061)

Compatible: Python 3.11, PyInstaller, Windows 11
Auteur: UndKiMi
"""
import ctypes
from ctypes import wintypes, Structure, POINTER, byref, sizeof
import os
import sys


# ============================================================================
# STRUCTURES WINDOWS
# ============================================================================

class LUID(Structure):
    _fields_ = [("LowPart", wintypes.DWORD), ("HighPart", wintypes.LONG)]


class LUID_AND_ATTRIBUTES(Structure):
    _fields_ = [("Luid", LUID), ("Attributes", wintypes.DWORD)]


class TOKEN_PRIVILEGES(Structure):
    _fields_ = [
        ("PrivilegeCount", wintypes.DWORD),
        ("Privileges", LUID_AND_ATTRIBUTES * 1)
    ]


# ============================================================================
# CONSTANTES
# ============================================================================

# Token Access Rights
TOKEN_ADJUST_PRIVILEGES = 0x0020
TOKEN_QUERY = 0x0008

# Process Access Rights
PROCESS_ALL_ACCESS = 0x1F0FFF
PROCESS_QUERY_INFORMATION = 0x0400

# Privilege Attributes
SE_PRIVILEGE_ENABLED = 0x00000002

# Privilege Names - TOUS REQUIS
SE_DEBUG_NAME = "SeDebugPrivilege"  # CRITIQUE pour EmptyStandbyList
SE_PROFILE_SINGLE_PROCESS_NAME = "SeProfileSingleProcessPrivilege"
SE_INCREASE_QUOTA_NAME = "SeIncreaseQuotaPrivilege"

# System Information Classes
SystemMemoryListInformation = 80

# Memory List Commands
MemoryPurgeStandbyList = 4

# NTSTATUS Codes
STATUS_SUCCESS = 0x00000000
STATUS_PRIVILEGE_NOT_HELD = 0xC0000061


# ============================================================================
# FONCTION PRINCIPALE - ACTIVATION DES PRIVILÈGES
# ============================================================================

def enable_privileges_robust():
    """
    Active les privilèges Windows de façon robuste
    Corrige ERROR_INVALID_HANDLE (6) en utilisant OpenProcess au lieu de GetCurrentProcess
    
    Returns:
        bool: True si succès, False sinon
    """
    print("\n" + "=" * 70)
    print("ACTIVATION DES PRIVILÈGES WINDOWS")
    print("=" * 70)
    
    try:
        kernel32 = ctypes.windll.kernel32
        advapi32 = ctypes.windll.advapi32
        
        # ÉTAPE 1: Obtenir le PID du processus courant
        pid = os.getpid()
        print(f"[1/5] PID du processus: {pid}")
        
        # ÉTAPE 2: Ouvrir le processus avec OpenProcess (pas GetCurrentProcess!)
        # C'EST LA CLÉ POUR ÉVITER ERROR 6
        process_handle = kernel32.OpenProcess(
            PROCESS_ALL_ACCESS,  # Tous les droits
            False,               # N'hérite pas
            pid                  # PID réel
        )
        
        if not process_handle:
            error = kernel32.GetLastError()
            print(f"[✗] OpenProcess failed: {error}")
            return False
        
        print(f"[2/5] Process handle obtenu: 0x{process_handle:08X}")
        
        # ÉTAPE 3: Ouvrir le token du processus
        token_handle = wintypes.HANDLE()
        result = advapi32.OpenProcessToken(
            process_handle,
            TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY,
            byref(token_handle)
        )
        
        if not result:
            error = kernel32.GetLastError()
            print(f"[✗] OpenProcessToken failed: {error}")
            kernel32.CloseHandle(process_handle)
            return False
        
        print(f"[3/5] Token handle obtenu: 0x{token_handle.value:08X}")
        
        # ÉTAPE 4: Activer chaque privilège
        privileges_to_enable = [
            (SE_DEBUG_NAME, "CRITIQUE pour EmptyStandbyList"),
            (SE_PROFILE_SINGLE_PROCESS_NAME, "Profiling système"),
            (SE_INCREASE_QUOTA_NAME, "Augmentation quota"),
        ]
        
        print("[4/5] Activation des privilèges:")
        success_count = 0
        
        for privilege_name, description in privileges_to_enable:
            print(f"  → {privilege_name} ({description})")
            
            # Lookup LUID
            luid = LUID()
            if not advapi32.LookupPrivilegeValueW(None, privilege_name, byref(luid)):
                error = kernel32.GetLastError()
                print(f"    [✗] LookupPrivilegeValue failed: {error}")
                continue
            
            # Créer TOKEN_PRIVILEGES
            tp = TOKEN_PRIVILEGES()
            tp.PrivilegeCount = 1
            tp.Privileges[0].Luid = luid
            tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED
            
            # Activer le privilège
            if not advapi32.AdjustTokenPrivileges(
                token_handle,
                False,
                byref(tp),
                0,
                None,
                None
            ):
                error = kernel32.GetLastError()
                print(f"    [✗] AdjustTokenPrivileges failed: {error}")
                continue
            
            # Vérifier GetLastError même si succès
            error = kernel32.GetLastError()
            if error == 0:
                print(f"    [✓] Activé avec succès")
                success_count += 1
            elif error == 1300:  # ERROR_NOT_ALL_ASSIGNED
                print(f"    [✗] Privilège non assigné au compte")
                print(f"        Solution: secpol.msc > Stratégies locales > Attribution des droits")
                print(f"        Ajouter votre compte à '{privilege_name}'")
            else:
                print(f"    [⚠] Warning code: {error}")
        
        # ÉTAPE 5: Nettoyer les handles
        kernel32.CloseHandle(token_handle)
        kernel32.CloseHandle(process_handle)  # IMPORTANT: fermer le handle du processus
        
        print(f"[5/5] Handles fermés")
        print("=" * 70)
        print(f"RÉSULTAT: {success_count}/{len(privileges_to_enable)} privilèges activés")
        print("=" * 70)
        
        return success_count > 0
        
    except Exception as e:
        print(f"[✗] Exception: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# FONCTION - VIDER LA RAM STANDBY
# ============================================================================

def empty_standby_list():
    """
    Vide la RAM Standby en utilisant NtSetSystemInformation
    Nécessite que enable_privileges_robust() ait été appelé avec succès
    
    Returns:
        bool: True si succès, False sinon
    """
    print("\n" + "=" * 70)
    print("VIDAGE DE LA RAM STANDBY")
    print("=" * 70)
    
    try:
        ntdll = ctypes.windll.ntdll
        
        # Commande pour vider la Standby List
        command = ctypes.c_int(MemoryPurgeStandbyList)
        
        print("[INFO] Appel à NtSetSystemInformation...")
        print(f"       SystemInformationClass: {SystemMemoryListInformation}")
        print(f"       Command: {MemoryPurgeStandbyList} (MemoryPurgeStandbyList)")
        
        # Appel à l'API
        result = ntdll.NtSetSystemInformation(
            SystemMemoryListInformation,
            byref(command),
            sizeof(command)
        )
        
        # Convertir en unsigned pour affichage
        result_unsigned = ctypes.c_ulong(result).value
        
        print(f"[INFO] Code retour: {result} (0x{result_unsigned:08X})")
        
        if result == STATUS_SUCCESS or result == 0:
            print("[✓] RAM Standby vidée avec succès!")
            return True
        elif result_unsigned == STATUS_PRIVILEGE_NOT_HELD or result == -1073741727:
            print("[✗] STATUS_PRIVILEGE_NOT_HELD")
            print("    Causes possibles:")
            print("    1. SeDebugPrivilege non assigné au compte")
            print("    2. Privilèges non activés (enable_privileges_robust échoué)")
            print("    3. Application non lancée en administrateur")
            return False
        else:
            print(f"[✗] Erreur NTSTATUS: 0x{result_unsigned:08X}")
            error_codes = {
                0xC0000022: "STATUS_ACCESS_DENIED",
                0xC000000D: "STATUS_INVALID_PARAMETER",
                0xC0000008: "STATUS_INVALID_HANDLE",
            }
            if result_unsigned in error_codes:
                print(f"    {error_codes[result_unsigned]}")
            return False
            
    except Exception as e:
        print(f"[✗] Exception: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# FONCTION - VÉRIFICATION ADMIN
# ============================================================================

def is_admin():
    """Vérifie si le processus est lancé en administrateur"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# ============================================================================
# FONCTION - OBTENIR INFO MÉMOIRE
# ============================================================================

def get_memory_info():
    """Obtient les informations mémoire pour calculer la RAM Standby"""
    try:
        import psutil
        mem = psutil.virtual_memory()
        
        # Estimation RAM Standby (approximative)
        # Standby ≈ Total - (Used + Available)
        standby_mb = (mem.total - mem.used - mem.available) / (1024 * 1024)
        
        return {
            'total_mb': mem.total / (1024 * 1024),
            'available_mb': mem.available / (1024 * 1024),
            'used_mb': mem.used / (1024 * 1024),
            'standby_mb': max(0, standby_mb),  # Éviter valeurs négatives
        }
    except ImportError:
        print("[WARNING] psutil non disponible, impossible de calculer la RAM Standby")
        return None


# ============================================================================
# PROGRAMME PRINCIPAL
# ============================================================================

def main():
    """Programme principal de test"""
    print("\n" + "=" * 70)
    print("TEST COMPLET - EMPTYSTANDBYLIST")
    print("=" * 70)
    
    # Vérification 1: Admin
    if not is_admin():
        print("\n[✗] ERREUR: Application non lancée en administrateur!")
        print("[INFO] Relancez avec: Clic droit > Exécuter en tant qu'administrateur")
        return False
    
    print("\n[✓] Application lancée en administrateur")
    
    # Vérification 2: Mémoire avant
    mem_before = get_memory_info()
    if mem_before:
        print(f"\n[INFO] Mémoire AVANT vidage:")
        print(f"       Total: {mem_before['total_mb']:.0f} MB")
        print(f"       Disponible: {mem_before['available_mb']:.0f} MB")
        print(f"       Utilisée: {mem_before['used_mb']:.0f} MB")
        print(f"       Standby (estimée): {mem_before['standby_mb']:.0f} MB")
    
    # Étape 1: Activer les privilèges
    if not enable_privileges_robust():
        print("\n[✗] ÉCHEC: Impossible d'activer les privilèges")
        print("[INFO] Vérifiez que SeDebugPrivilege est assigné à votre compte")
        return False
    
    # Étape 2: Vider la RAM Standby
    if not empty_standby_list():
        print("\n[✗] ÉCHEC: Impossible de vider la RAM Standby")
        return False
    
    # Vérification 3: Mémoire après
    import time
    time.sleep(1)  # Attendre que Windows libère la mémoire
    
    mem_after = get_memory_info()
    if mem_after and mem_before:
        print(f"\n[INFO] Mémoire APRÈS vidage:")
        print(f"       Disponible: {mem_after['available_mb']:.0f} MB")
        print(f"       Standby (estimée): {mem_after['standby_mb']:.0f} MB")
        freed = mem_after['available_mb'] - mem_before['available_mb']
        print(f"\n[✓] RAM libérée: {freed:.0f} MB")
    
    print("\n" + "=" * 70)
    print("TEST TERMINÉ AVEC SUCCÈS")
    print("=" * 70)
    return True


if __name__ == "__main__":
    success = main()
    print()
    input("Appuyez sur Entrée pour quitter...")
    sys.exit(0 if success else 1)
