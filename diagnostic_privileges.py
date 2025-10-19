"""
Diagnostic complet des privilèges et tokens Windows
Détecte précisément si un token est admin ET a les bons droits
"""
import ctypes
from ctypes import wintypes, byref, sizeof
import os


def check_admin_status():
    """Vérifie si le processus est admin"""
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        print(f"[{'✓' if is_admin else '✗'}] IsUserAnAdmin: {is_admin}")
        return is_admin
    except Exception as e:
        print(f"[✗] IsUserAnAdmin failed: {e}")
        return False


def check_token_elevation():
    """Vérifie si le token est élevé (UAC)"""
    try:
        kernel32 = ctypes.windll.kernel32
        advapi32 = ctypes.windll.advapi32
        
        # Ouvrir le processus
        pid = os.getpid()
        PROCESS_QUERY_INFORMATION = 0x0400
        process_handle = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, pid)
        
        if not process_handle:
            print(f"[✗] OpenProcess failed: {kernel32.GetLastError()}")
            return False
        
        # Ouvrir le token
        TOKEN_QUERY = 0x0008
        token_handle = wintypes.HANDLE()
        if not advapi32.OpenProcessToken(process_handle, TOKEN_QUERY, byref(token_handle)):
            print(f"[✗] OpenProcessToken failed: {kernel32.GetLastError()}")
            kernel32.CloseHandle(process_handle)
            return False
        
        # Vérifier TokenElevation
        class TOKEN_ELEVATION(ctypes.Structure):
            _fields_ = [("TokenIsElevated", wintypes.DWORD)]
        
        TokenElevation = 20
        elevation = TOKEN_ELEVATION()
        return_length = wintypes.DWORD()
        
        if advapi32.GetTokenInformation(
            token_handle,
            TokenElevation,
            byref(elevation),
            sizeof(elevation),
            byref(return_length)
        ):
            is_elevated = bool(elevation.TokenIsElevated)
            print(f"[{'✓' if is_elevated else '✗'}] TokenIsElevated: {is_elevated}")
            
            kernel32.CloseHandle(token_handle)
            kernel32.CloseHandle(process_handle)
            return is_elevated
        else:
            print(f"[✗] GetTokenInformation failed: {kernel32.GetLastError()}")
            kernel32.CloseHandle(token_handle)
            kernel32.CloseHandle(process_handle)
            return False
            
    except Exception as e:
        print(f"[✗] check_token_elevation failed: {e}")
        return False


def check_privilege_status(privilege_name):
    """Vérifie si un privilège spécifique est activé"""
    try:
        kernel32 = ctypes.windll.kernel32
        advapi32 = ctypes.windll.advapi32
        
        # Structures
        class LUID(ctypes.Structure):
            _fields_ = [("LowPart", wintypes.DWORD), ("HighPart", wintypes.LONG)]
        
        class LUID_AND_ATTRIBUTES(ctypes.Structure):
            _fields_ = [("Luid", LUID), ("Attributes", wintypes.DWORD)]
        
        class PRIVILEGE_SET(ctypes.Structure):
            _fields_ = [
                ("PrivilegeCount", wintypes.DWORD),
                ("Control", wintypes.DWORD),
                ("Privilege", LUID_AND_ATTRIBUTES * 1)
            ]
        
        # Ouvrir processus et token
        pid = os.getpid()
        PROCESS_QUERY_INFORMATION = 0x0400
        process_handle = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, pid)
        
        if not process_handle:
            return None, f"OpenProcess failed: {kernel32.GetLastError()}"
        
        TOKEN_QUERY = 0x0008
        token_handle = wintypes.HANDLE()
        if not advapi32.OpenProcessToken(process_handle, TOKEN_QUERY, byref(token_handle)):
            error = kernel32.GetLastError()
            kernel32.CloseHandle(process_handle)
            return None, f"OpenProcessToken failed: {error}"
        
        # Lookup LUID
        luid = LUID()
        if not advapi32.LookupPrivilegeValueW(None, privilege_name, byref(luid)):
            error = kernel32.GetLastError()
            kernel32.CloseHandle(token_handle)
            kernel32.CloseHandle(process_handle)
            return None, f"LookupPrivilegeValue failed: {error}"
        
        # Créer PRIVILEGE_SET
        priv_set = PRIVILEGE_SET()
        priv_set.PrivilegeCount = 1
        priv_set.Control = 1  # PRIVILEGE_SET_ALL_NECESSARY
        priv_set.Privilege[0].Luid = luid
        priv_set.Privilege[0].Attributes = 0
        
        # Vérifier le privilège
        result = wintypes.BOOL()
        if advapi32.PrivilegeCheck(token_handle, byref(priv_set), byref(result)):
            status = bool(result.value)
            kernel32.CloseHandle(token_handle)
            kernel32.CloseHandle(process_handle)
            return status, "OK"
        else:
            error = kernel32.GetLastError()
            kernel32.CloseHandle(token_handle)
            kernel32.CloseHandle(process_handle)
            return None, f"PrivilegeCheck failed: {error}"
            
    except Exception as e:
        return None, f"Exception: {e}"


def diagnostic_complet():
    """Diagnostic complet du contexte d'exécution"""
    print("\n" + "=" * 70)
    print("DIAGNOSTIC COMPLET - PRIVILÈGES & TOKENS WINDOWS")
    print("=" * 70)
    
    # Informations de base
    print("\n[1] INFORMATIONS DE BASE")
    print(f"    PID: {os.getpid()}")
    print(f"    Python: {os.sys.version.split()[0]}")
    
    # Vérification admin
    print("\n[2] STATUT ADMINISTRATEUR")
    is_admin = check_admin_status()
    
    # Vérification élévation token
    print("\n[3] ÉLÉVATION DU TOKEN (UAC)")
    is_elevated = check_token_elevation()
    
    # Vérification privilèges
    print("\n[4] PRIVILÈGES SPÉCIFIQUES")
    privileges = [
        ("SeDebugPrivilege", "CRITIQUE pour EmptyStandbyList"),
        ("SeProfileSingleProcessPrivilege", "Profiling"),
        ("SeIncreaseQuotaPrivilege", "Quota mémoire"),
        ("SeShutdownPrivilege", "Arrêt système"),
        ("SeBackupPrivilege", "Sauvegarde"),
    ]
    
    for priv_name, description in privileges:
        status, message = check_privilege_status(priv_name)
        if status is None:
            print(f"    [?] {priv_name}: Erreur - {message}")
        elif status:
            print(f"    [✓] {priv_name}: ACTIVÉ ({description})")
        else:
            print(f"    [✗] {priv_name}: NON ACTIVÉ ({description})")
    
    # Résumé
    print("\n" + "=" * 70)
    print("RÉSUMÉ")
    print("=" * 70)
    
    if not is_admin:
        print("[✗] Application NON lancée en administrateur")
        print("    Solution: Clic droit > Exécuter en tant qu'administrateur")
    elif not is_elevated:
        print("[✗] Token NON élevé (UAC)")
        print("    Solution: Vérifier le manifeste requireAdministrator")
    else:
        print("[✓] Application correctement lancée en administrateur")
        print("[INFO] Si EmptyStandbyList échoue, vérifiez SeDebugPrivilege")
    
    print()


if __name__ == "__main__":
    diagnostic_complet()
    input("Appuyez sur Entrée pour quitter...")
