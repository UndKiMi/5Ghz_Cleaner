"""
Script de test pour vérifier l'activation des privilèges Windows
Doit être lancé en tant qu'administrateur
"""
import ctypes
from ctypes import wintypes, byref, sizeof
import sys

# Vérifier si admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("[ERROR] Ce script doit être lancé en tant qu'administrateur!")
    print("[INFO] Clic droit > Exécuter en tant qu'administrateur")
    sys.exit(1)

print("[INFO] Application lancée avec privilèges administrateur")
print()

# Structures
class LUID(ctypes.Structure):
    _fields_ = [("LowPart", wintypes.DWORD), ("HighPart", wintypes.LONG)]

class LUID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = [("Luid", LUID), ("Attributes", wintypes.DWORD)]

class TOKEN_PRIVILEGES(ctypes.Structure):
    _fields_ = [("PrivilegeCount", wintypes.DWORD), ("Privileges", LUID_AND_ATTRIBUTES * 1)]

# Constantes
TOKEN_ADJUST_PRIVILEGES = 0x0020
TOKEN_QUERY = 0x0008
SE_PRIVILEGE_ENABLED = 0x00000002

# Privilèges à tester
privileges_to_test = [
    ("SeDebugPrivilege", "CRITIQUE pour EmptyStandbyList"),
    ("SeProfileSingleProcessPrivilege", "Profiling"),
    ("SeIncreaseQuotaPrivilege", "Quota"),
]

print("=" * 70)
print("TEST D'ACTIVATION DES PRIVILÈGES WINDOWS")
print("=" * 70)
print()

try:
    kernel32 = ctypes.windll.kernel32
    advapi32 = ctypes.windll.advapi32
    
    # Obtenir le handle du processus
    process_handle = kernel32.GetCurrentProcess()
    print(f"[✓] Process handle obtenu: {process_handle}")
    
    # Ouvrir le token
    token_handle = wintypes.HANDLE()
    result = advapi32.OpenProcessToken(
        process_handle,
        TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY,
        byref(token_handle)
    )
    
    if not result:
        error = kernel32.GetLastError()
        print(f"[✗] OpenProcessToken failed: {error}")
        sys.exit(1)
    
    print(f"[✓] Token handle obtenu: {token_handle.value}")
    print()
    
    # Tester chaque privilège
    success_count = 0
    for privilege_name, description in privileges_to_test:
        print(f"Testing: {privilege_name} ({description})")
        
        luid = LUID()
        if not advapi32.LookupPrivilegeValueW(None, privilege_name, byref(luid)):
            error = kernel32.GetLastError()
            print(f"  [✗] LookupPrivilegeValue failed: {error}")
            continue
        
        print(f"  [✓] LUID: {luid.LowPart}")
        
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
            print(f"  [✗] AdjustTokenPrivileges failed: {error}")
        else:
            # Vérifier GetLastError() même si succès (peut retourner ERROR_NOT_ALL_ASSIGNED)
            error = kernel32.GetLastError()
            if error == 0:
                print(f"  [✓] Privilège activé avec succès!")
                success_count += 1
            elif error == 1300:  # ERROR_NOT_ALL_ASSIGNED
                print(f"  [⚠] Privilège non assigné (ERROR_NOT_ALL_ASSIGNED)")
                print(f"      Le compte n'a pas ce privilège dans la politique de sécurité")
            else:
                print(f"  [⚠] Warning code: {error}")
        print()
    
    # Fermer le handle
    kernel32.CloseHandle(token_handle)
    
    print("=" * 70)
    print(f"RÉSULTAT: {success_count}/{len(privileges_to_test)} privilèges activés")
    print("=" * 70)
    print()
    
    if success_count == 0:
        print("[ERROR] AUCUN privilège n'a pu être activé!")
        print("[INFO] Vérifiez que le compte a les privilèges nécessaires dans:")
        print("       secpol.msc > Stratégies locales > Attribution des droits utilisateur")
    elif success_count < len(privileges_to_test):
        print("[WARNING] Certains privilèges n'ont pas pu être activés")
        print("[INFO] EmptyStandbyList nécessite SeDebugPrivilege")
    else:
        print("[SUCCESS] Tous les privilèges ont été activés!")
        print("[INFO] EmptyStandbyList devrait fonctionner correctement")

except Exception as e:
    print(f"[ERROR] Exception: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
input("Appuyez sur Entrée pour quitter...")
