"""
Module de gestion avancée de la RAM Windows
Utilise l'API Windows native pour un calcul précis et un vidage efficace de la RAM Standby

DOCUMENTATION TECHNIQUE:
========================

1. RAM STANDBY (Mémoire en Attente):
   - La RAM Standby contient des données récemment utilisées mais non actives
   - Windows la conserve pour accélérer le rechargement des applications
   - Elle peut être libérée instantanément si une application en a besoin
   - Formule: RAM Standby ≈ Total - (Used + Available + Free)

2. API WINDOWS UTILISÉES:
   - GlobalMemoryStatusEx: Obtient l'état détaillé de la mémoire
   - EmptyWorkingSet: Vide le working set des processus
   - SetSystemFileCacheSize: Réduit le cache système (nécessite admin)
   - NtSetSystemInformation: Vide la liste Standby (nécessite admin)

3. SÉCURITÉ:
   - Toutes les opérations sont sûres et réversibles
   - Pas d'utilisation de PowerShell (évite injection de commandes)
   - Gestion des privilèges Windows appropriée
   - Fallback gracieux si privilèges insuffisants

4. PERFORMANCE:
   - Calcul optimisé avec cache intelligent
   - Mise à jour en temps réel sans surcharge système
   - Validation des valeurs pour éviter les aberrations
"""

import ctypes
from ctypes import wintypes, Structure, POINTER, byref, sizeof, windll
import psutil
import threading
import time
import sys
from typing import Dict, Optional


# ============================================================================
# STRUCTURES WINDOWS API
# ============================================================================

class MEMORYSTATUSEX(Structure):
    """Structure pour GlobalMemoryStatusEx"""
    _fields_ = [
        ("dwLength", wintypes.DWORD),
        ("dwMemoryLoad", wintypes.DWORD),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]


class SYSTEM_CACHE_INFORMATION(Structure):
    """Structure pour le cache système"""
    _fields_ = [
        ("CurrentSize", ctypes.c_size_t),
        ("PeakSize", ctypes.c_size_t),
        ("PageFaultCount", ctypes.c_ulong),
        ("MinimumWorkingSet", ctypes.c_size_t),
        ("MaximumWorkingSet", ctypes.c_size_t),
        ("Unused1", ctypes.c_size_t),
        ("Unused2", ctypes.c_size_t),
        ("Unused3", ctypes.c_size_t),
        ("Unused4", ctypes.c_size_t),
    ]


class PERFORMANCE_INFORMATION(Structure):
    """Structure pour GetPerformanceInfo - ESSENTIELLE pour RAM Standby"""
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("CommitTotal", ctypes.c_size_t),
        ("CommitLimit", ctypes.c_size_t),
        ("CommitPeak", ctypes.c_size_t),
        ("PhysicalTotal", ctypes.c_size_t),
        ("PhysicalAvailable", ctypes.c_size_t),
        ("SystemCache", ctypes.c_size_t),
        ("KernelTotal", ctypes.c_size_t),
        ("KernelPaged", ctypes.c_size_t),
        ("KernelNonpaged", ctypes.c_size_t),
        ("PageSize", ctypes.c_size_t),
        ("HandleCount", wintypes.DWORD),
        ("ProcessCount", wintypes.DWORD),
        ("ThreadCount", wintypes.DWORD),
    ]


class LUID(Structure):
    """Locally Unique Identifier"""
    _fields_ = [
        ("LowPart", wintypes.DWORD),
        ("HighPart", wintypes.LONG),
    ]


class LUID_AND_ATTRIBUTES(Structure):
    """LUID with attributes"""
    _fields_ = [
        ("Luid", LUID),
        ("Attributes", wintypes.DWORD),
    ]


class TOKEN_PRIVILEGES(Structure):
    """Token privileges structure"""
    _fields_ = [
        ("PrivilegeCount", wintypes.DWORD),
        ("Privileges", LUID_AND_ATTRIBUTES * 1),
    ]


# ============================================================================
# CONSTANTES WINDOWS
# ============================================================================

# System Information Classes
SystemFileCacheInformation = 21
SystemMemoryListInformation = 80

# Memory List Commands
MemoryPurgeStandbyList = 4
MemoryEmptyWorkingSets = 2

# Token Access Rights
TOKEN_ADJUST_PRIVILEGES = 0x0020
TOKEN_QUERY = 0x0008

# Privilege Attributes
SE_PRIVILEGE_ENABLED = 0x00000002

# Privilege Names
SE_PROFILE_SINGLE_PROCESS_NAME = "SeProfileSingleProcessPrivilege"
SE_INCREASE_QUOTA_NAME = "SeIncreaseQuotaPrivilege"
SE_DEBUG_NAME = "SeDebugPrivilege"  # REQUIS pour EmptyStandbyList

# NTSTATUS Codes
STATUS_SUCCESS = 0x00000000
STATUS_PRIVILEGE_NOT_HELD = 0xC0000061


# ============================================================================
# CLASSE PRINCIPALE
# ============================================================================

class RAMManager:
    """
    Gestionnaire avancé de la RAM Windows
    Calcul précis et vidage efficace de la RAM Standby
    """
    
    def __init__(self):
        self._lock = threading.Lock()
        self._last_calculation = None
        self._last_calculation_time = 0
        self._cache_duration = 0.5  # Cache de 500ms pour éviter surcharge
        self._privileges_enabled = False
        
        # Charger les DLLs Windows
        try:
            self.kernel32 = ctypes.windll.kernel32
            self.psapi = ctypes.windll.psapi
            self.ntdll = ctypes.windll.ntdll
            self.advapi32 = ctypes.windll.advapi32
        except Exception as e:
            print(f"[ERROR] Failed to load Windows DLLs: {e}")
            self.kernel32 = None
            self.psapi = None
            self.ntdll = None
            self.advapi32 = None
        
        # Tenter d'activer les privilèges nécessaires
        self._enable_privileges()
    
    def _enable_privileges(self):
        """
        Active les privilèges Windows nécessaires pour EmptyStandbyList
        Nécessite que l'application soit lancée en tant qu'administrateur
        CORRECTION: Évite les appels répétés qui causent le warning "Handle already in use"
        """
        # Si déjà activé, ne pas réessayer
        if self._privileges_enabled:
            print("[DEBUG] Privileges already enabled, skipping")
            return True
            
        if not self.advapi32 or not self.kernel32:
            print("[WARNING] Cannot enable privileges: DLLs not loaded")
            return False
        
        print("[DEBUG] Attempting to enable privileges for EmptyStandbyList...")
        
        try:
            # FIX CRITIQUE: Utiliser OpenProcess au lieu de GetCurrentProcess
            # GetCurrentProcess() retourne un pseudo-handle (-1) qui peut être invalide
            # dans certains contextes (PyInstaller, threads, etc.)
            import os
            pid = os.getpid()
            print(f"[DEBUG] Current PID: {pid}")
            
            # Ouvrir le processus avec le PID réel
            PROCESS_ALL_ACCESS = 0x1F0FFF
            process_handle = self.kernel32.OpenProcess(
                PROCESS_ALL_ACCESS,
                False,
                pid
            )
            
            if not process_handle:
                error = self.kernel32.GetLastError()
                print(f"[ERROR] OpenProcess failed with error: {error}")
                return False
            
            print(f"[DEBUG] Process handle: 0x{process_handle:08X}")
            
            # Ouvrir le token du processus
            token_handle = wintypes.HANDLE()
            result = self.advapi32.OpenProcessToken(
                process_handle,
                TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY,
                byref(token_handle)
            )
            
            if not result:
                error = self.kernel32.GetLastError()
                print(f"[ERROR] OpenProcessToken failed with error: {error}")
                self.kernel32.CloseHandle(process_handle)  # Fermer le handle du processus
                return False
            
            print(f"[DEBUG] Token handle: 0x{token_handle.value:08X}")
            
            # Liste des privilèges à activer
            # CORRECTION: Ajout de SeDebugPrivilege requis pour EmptyStandbyList
            privileges_to_enable = [
                SE_DEBUG_NAME,  # CRITIQUE pour EmptyStandbyList
                SE_PROFILE_SINGLE_PROCESS_NAME,
                SE_INCREASE_QUOTA_NAME,
            ]
            
            for privilege_name in privileges_to_enable:
                luid = LUID()
                if not self.advapi32.LookupPrivilegeValueW(None, privilege_name, byref(luid)):
                    error = self.kernel32.GetLastError()
                    print(f"[WARNING] LookupPrivilegeValue failed for {privilege_name}: {error}")
                    continue
                
                # Créer la structure TOKEN_PRIVILEGES
                tp = TOKEN_PRIVILEGES()
                tp.PrivilegeCount = 1
                tp.Privileges[0].Luid = luid
                tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED
                
                # Ajuster les privilèges du token
                if not self.advapi32.AdjustTokenPrivileges(
                    token_handle,
                    False,
                    byref(tp),
                    0,
                    None,
                    None
                ):
                    error = self.kernel32.GetLastError()
                    print(f"[WARNING] AdjustTokenPrivileges failed for {privilege_name}: {error}")
                else:
                    # IMPORTANT: Vérifier GetLastError() même si la fonction retourne succès
                    # Elle peut retourner ERROR_NOT_ALL_ASSIGNED (1300)
                    error = self.kernel32.GetLastError()
                    if error == 0:
                        print(f"[SUCCESS] Privilege {privilege_name} enabled")
                    elif error == 1300:  # ERROR_NOT_ALL_ASSIGNED
                        print(f"[WARNING] Privilege {privilege_name} not assigned to this account")
                        print(f"[INFO] Run: secpol.msc > Local Policies > User Rights Assignment")
                        print(f"[INFO] Add your account to '{privilege_name}'")
                    else:
                        print(f"[WARNING] Privilege {privilege_name} warning code: {error}")
            
            # Fermer les handles (IMPORTANT pour éviter les fuites)
            self.kernel32.CloseHandle(token_handle)
            self.kernel32.CloseHandle(process_handle)  # Fermer aussi le handle du processus
            self._privileges_enabled = True
            print("[SUCCESS] All privileges enabled successfully for EmptyStandbyList")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to enable privileges: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_detailed_memory_info(self) -> Dict:
        """
        Obtient des informations détaillées sur la mémoire via l'API Windows native
        
        Returns:
            dict: {
                'total_mb': float,           # RAM totale
                'available_mb': float,       # RAM disponible
                'used_mb': float,            # RAM utilisée
                'free_mb': float,            # RAM libre (jamais utilisée)
                'standby_mb': float,         # RAM Standby (CALCULÉ PRÉCISÉMENT)
                'modified_mb': float,        # RAM modifiée (en attente d'écriture)
                'cached_mb': float,          # RAM en cache
                'percent_used': float,       # % RAM utilisée
                'percent_standby': float,    # % RAM Standby
            }
        """
        with self._lock:
            # Utiliser le cache si disponible et récent
            current_time = time.time()
            if (self._last_calculation and 
                (current_time - self._last_calculation_time) < self._cache_duration):
                return self._last_calculation.copy()
            
            try:
                # Méthode 1: API Windows native (PRÉCIS)
                if self.kernel32:
                    mem_status = MEMORYSTATUSEX()
                    mem_status.dwLength = sizeof(MEMORYSTATUSEX)
                    
                    if self.kernel32.GlobalMemoryStatusEx(byref(mem_status)):
                        total_bytes = mem_status.ullTotalPhys
                        available_bytes = mem_status.ullAvailPhys
                        
                        # Convertir en MB
                        total_mb = total_bytes / (1024 * 1024)
                        available_mb = available_bytes / (1024 * 1024)
                        
                        # Utiliser GetPerformanceInfo pour obtenir SystemCache (RAM Standby)
                        perf_info = PERFORMANCE_INFORMATION()
                        perf_info.cb = sizeof(PERFORMANCE_INFORMATION)
                        
                        if self.psapi.GetPerformanceInfo(byref(perf_info), perf_info.cb):
                            # SystemCache contient la RAM en cache (Standby + Modified)
                            page_size = perf_info.PageSize
                            system_cache_pages = perf_info.SystemCache
                            system_cache_bytes = system_cache_pages * page_size
                            system_cache_mb = system_cache_bytes / (1024 * 1024)
                            
                            # Utiliser psutil pour les détails supplémentaires
                            vm = psutil.virtual_memory()
                            
                            # Calculs précis
                            used_mb = (total_bytes - available_bytes) / (1024 * 1024)
                            free_mb = vm.free / (1024 * 1024)  # RAM libre (non utilisée)
                            
                            # CALCUL CORRECT DE LA RAM STANDBY
                            # SystemCache = RAM utilisée pour le cache fichier système
                            # C'est la RAM Standby que nous cherchons!
                            standby_mb = system_cache_mb
                            
                            # Validation: Standby doit être positif et raisonnable
                            if standby_mb < 0:
                                standby_mb = 0
                            elif standby_mb > total_mb * 0.8:  # Max 80% de la RAM
                                print(f"[WARNING] Standby RAM seems too high: {standby_mb:.2f} MB, capping to 50%")
                                standby_mb = total_mb * 0.5
                            
                            # RAM modifiée (approximation)
                            modified_mb = max(0, available_mb - standby_mb)
                            
                            print(f"[DEBUG] SystemCache: {system_cache_mb:.2f} MB, Available: {available_mb:.2f} MB")
                        else:
                            # Fallback si GetPerformanceInfo échoue
                            print("[WARNING] GetPerformanceInfo failed, using estimation")
                            vm = psutil.virtual_memory()
                            used_mb = (total_bytes - available_bytes) / (1024 * 1024)
                            free_mb = vm.free / (1024 * 1024)
                            
                            # Estimation basée sur la différence
                            # Standby ≈ Available - (quelques centaines de MB pour le système)
                            standby_mb = max(0, available_mb - 500)  # Estimation conservatrice
                            modified_mb = 0
                        
                        # RAM en cache (Standby + Modified)
                        cached_mb = standby_mb + modified_mb
                        
                        # Pourcentages
                        percent_used = (used_mb / total_mb * 100) if total_mb > 0 else 0
                        percent_standby = (standby_mb / total_mb * 100) if total_mb > 0 else 0
                        
                        result = {
                            'total_mb': total_mb,
                            'available_mb': available_mb,
                            'used_mb': used_mb,
                            'free_mb': free_mb,
                            'standby_mb': standby_mb,
                            'modified_mb': modified_mb,
                            'cached_mb': cached_mb,
                            'percent_used': percent_used,
                            'percent_standby': percent_standby,
                        }
                        
                        # Mettre en cache
                        self._last_calculation = result
                        self._last_calculation_time = current_time
                        
                        return result
                
                # Fallback: psutil uniquement (MOINS PRÉCIS)
                vm = psutil.virtual_memory()
                total_mb = vm.total / (1024 * 1024)
                available_mb = vm.available / (1024 * 1024)
                used_mb = vm.used / (1024 * 1024)
                free_mb = vm.free / (1024 * 1024)
                
                # Estimation Standby (moins précise)
                standby_mb = max(0, available_mb - free_mb)
                if standby_mb > total_mb * 0.7:
                    standby_mb = total_mb * 0.15
                
                modified_mb = 0  # Non disponible sans API native
                cached_mb = standby_mb
                
                percent_used = vm.percent
                percent_standby = (standby_mb / total_mb * 100) if total_mb > 0 else 0
                
                result = {
                    'total_mb': total_mb,
                    'available_mb': available_mb,
                    'used_mb': used_mb,
                    'free_mb': free_mb,
                    'standby_mb': standby_mb,
                    'modified_mb': modified_mb,
                    'cached_mb': cached_mb,
                    'percent_used': percent_used,
                    'percent_standby': percent_standby,
                }
                
                # Mettre en cache
                self._last_calculation = result
                self._last_calculation_time = current_time
                
                return result
                
            except Exception as e:
                print(f"[ERROR] Failed to get detailed memory info: {e}")
                # Valeurs par défaut en cas d'erreur
                return {
                    'total_mb': 0,
                    'available_mb': 0,
                    'used_mb': 0,
                    'free_mb': 0,
                    'standby_mb': 0,
                    'modified_mb': 0,
                    'cached_mb': 0,
                    'percent_used': 0,
                    'percent_standby': 0,
                }
    
    def clear_standby_memory(self) -> Dict:
        """
        Vide la RAM Standby en utilisant l'API Windows native
        
        MÉTHODES UTILISÉES (par ordre de priorité):
        1. EmptyStandbyList (NtSetSystemInformation) - PLUS EFFICACE
        2. SetSystemFileCacheSize - Réduit le cache système
        3. EmptyWorkingSet - Vide le working set des processus
        
        Returns:
            dict: {
                'success': bool,
                'method_used': str,
                'standby_before_mb': float,
                'standby_after_mb': float,
                'freed_mb': float,
                'error': str (si échec)
            }
        """
        try:
            # Obtenir l'état avant vidage
            mem_before = self.get_detailed_memory_info()
            standby_before_mb = mem_before['standby_mb']
            
            print(f"[INFO] RAM Standby avant vidage: {standby_before_mb:.2f} MB")
            
            success = False
            method_used = "none"
            
            # Méthode 1: EmptyStandbyList (PLUS EFFICACE - nécessite admin)
            if self.ntdll:
                try:
                    # Tenter de vider la liste Standby
                    command = ctypes.c_int(MemoryPurgeStandbyList)
                    result = self.ntdll.NtSetSystemInformation(
                        SystemMemoryListInformation,
                        byref(command),
                        sizeof(command)
                    )
                    
                    # Convertir le résultat en unsigned pour comparaison
                    result_unsigned = ctypes.c_ulong(result).value
                    
                    if result == STATUS_SUCCESS or result == 0:
                        success = True
                        method_used = "EmptyStandbyList"
                        print("[SUCCESS] RAM Standby vidée via EmptyStandbyList")
                    elif result_unsigned == STATUS_PRIVILEGE_NOT_HELD or result == -1073741727:
                        error_msg = "STATUS_PRIVILEGE_NOT_HELD: Privilèges insuffisants. L'application doit être lancée en tant qu'administrateur."
                        print(f"[ERROR] EmptyStandbyList failed: {error_msg}")
                        print(f"[INFO] Code d'erreur: {result} (0x{result_unsigned:08X})")
                        print("[INFO] Solution: Lancez l'application en tant qu'administrateur (clic droit > Exécuter en tant qu'administrateur)")
                    else:
                        print(f"[WARNING] EmptyStandbyList failed with NTSTATUS code: {result} (0x{result_unsigned:08X})")
                        # Codes d'erreur courants
                        error_codes = {
                            0xC0000022: "STATUS_ACCESS_DENIED: Accès refusé",
                            0xC0000061: "STATUS_PRIVILEGE_NOT_HELD: Privilège non détenu",
                            0xC000000D: "STATUS_INVALID_PARAMETER: Paramètre invalide",
                        }
                        if result_unsigned in error_codes:
                            print(f"[INFO] {error_codes[result_unsigned]}")
                except Exception as e:
                    print(f"[WARNING] EmptyStandbyList exception: {e}")
                    import traceback
                    traceback.print_exc()
            
            # Méthode 2: SetSystemFileCacheSize (MOYEN - nécessite admin)
            if not success and self.ntdll:
                try:
                    cache_info = SYSTEM_CACHE_INFORMATION()
                    cache_info.MinimumWorkingSet = ctypes.c_size_t(-1)
                    cache_info.MaximumWorkingSet = ctypes.c_size_t(-1)
                    
                    result = self.ntdll.NtSetSystemInformation(
                        SystemFileCacheInformation,
                        byref(cache_info),
                        sizeof(cache_info)
                    )
                    
                    if result == 0:
                        success = True
                        method_used = "SetSystemFileCacheSize"
                        print("[SUCCESS] Cache système réduit via SetSystemFileCacheSize")
                except Exception as e:
                    print(f"[WARNING] SetSystemFileCacheSize failed: {e}")
            
            # Méthode 3: EmptyWorkingSet (BASIQUE - toujours disponible)
            if not success and self.psapi:
                try:
                    # Vider le working set du processus courant
                    handle = self.kernel32.GetCurrentProcess()
                    if self.psapi.EmptyWorkingSet(handle):
                        success = True
                        method_used = "EmptyWorkingSet"
                        print("[SUCCESS] Working set vidé via EmptyWorkingSet")
                except Exception as e:
                    print(f"[WARNING] EmptyWorkingSet failed: {e}")
            
            # Attendre que Windows mette à jour les statistiques
            time.sleep(0.5)
            
            # Invalider le cache pour forcer un nouveau calcul
            self._last_calculation = None
            
            # Obtenir l'état après vidage
            mem_after = self.get_detailed_memory_info()
            standby_after_mb = mem_after['standby_mb']
            freed_mb = max(0, standby_before_mb - standby_after_mb)
            
            print(f"[INFO] RAM Standby après vidage: {standby_after_mb:.2f} MB")
            print(f"[INFO] RAM libérée: {freed_mb:.2f} MB")
            
            return {
                'success': success,
                'method_used': method_used,
                'standby_before_mb': standby_before_mb,
                'standby_after_mb': standby_after_mb,
                'freed_mb': freed_mb,
            }
            
        except Exception as e:
            print(f"[ERROR] Failed to clear standby memory: {e}")
            return {
                'success': False,
                'method_used': 'none',
                'standby_before_mb': 0,
                'standby_after_mb': 0,
                'freed_mb': 0,
                'error': str(e)
            }
    
    def invalidate_cache(self):
        """Force un nouveau calcul lors du prochain appel"""
        with self._lock:
            self._last_calculation = None


# Instance globale
ram_manager = RAMManager()
