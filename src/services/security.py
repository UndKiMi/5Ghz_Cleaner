"""
Module de sécurité pour 5GH'z Cleaner
Fonctions de vérification et protection système
"""
import os
import sys
import ctypes
import subprocess
from pathlib import Path


class SecurityManager:
    """Gestionnaire de sécurité pour protéger le système"""
    
    def __init__(self):
        self.warnings = []
        self.errors = []
    
    def verify_system_integrity(self):
        """Vérifie l'intégrité du système avant toute opération"""
        checks = [
            ("Windows Version", self._check_windows_version),
            ("System Files", self._check_system_files),
            ("Disk Health", self._check_disk_health),
            ("Running Services", self._check_critical_services),
        ]
        
        all_passed = True
        for check_name, check_func in checks:
            try:
                result = check_func()
                status = "✓" if result else "✗"
                print(f"[SECURITY] {status} {check_name}")
                if not result:
                    all_passed = False
            except Exception as e:
                print(f"[SECURITY] ✗ {check_name}: {e}")
                self.warnings.append(f"{check_name} check failed: {e}")
        
        return all_passed
    
    def _check_windows_version(self):
        """Vérifie la version de Windows"""
        try:
            version = sys.getwindowsversion()
            return version.major >= 10
        except:
            return False
    
    def _check_system_files(self):
        """Vérifie que les fichiers système critiques existent"""
        critical_files = [
            os.path.join(os.getenv('WINDIR', 'C:\\Windows'), 'System32', 'kernel32.dll'),
            os.path.join(os.getenv('WINDIR', 'C:\\Windows'), 'System32', 'ntdll.dll'),
            os.path.join(os.getenv('WINDIR', 'C:\\Windows'), 'explorer.exe'),
        ]
        
        for file in critical_files:
            if not os.path.exists(file):
                self.errors.append(f"Critical file missing: {file}")
                return False
        
        return True
    
    def _check_disk_health(self):
        """Vérifie la santé du disque"""
        try:
            import shutil
            usage = shutil.disk_usage("C:\\")
            free_percent = (usage.free / usage.total) * 100
            
            if free_percent < 5:
                self.warnings.append(f"Very low disk space: {free_percent:.1f}% free")
                return False
            
            return True
        except:
            return True
    
    def _check_critical_services(self):
        """Vérifie que les services critiques fonctionnent"""
        critical_services = ['wuauserv', 'BITS', 'CryptSvc']
        
        try:
            from src.utils.system_commands import system_cmd
            for service in critical_services:
                result = system_cmd.run_sc(['query', service])
                if result.returncode != 0:
                    self.warnings.append(f"Service {service} not available")
        except Exception:
            pass
        
        return True
    
    def is_safe_to_proceed(self):
        """Détermine s'il est sûr de procéder au nettoyage"""
        # Vérifier qu'il n'y a pas d'erreurs critiques
        if self.errors:
            print("[SECURITY] Critical errors detected:")
            for error in self.errors:
                print(f"  - {error}")
            return False
        
        # Les warnings ne bloquent pas, mais informent
        if self.warnings:
            print("[SECURITY] Warnings detected:")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        return True
    
    @staticmethod
    def create_backup_registry_key(key_path):
        """Crée une sauvegarde d'une clé de registre avant modification"""
        try:
            # Remplacer les backslashes par des underscores pour le nom de fichier
            safe_key_name = key_path.replace('\\', '_')
            backup_path = os.path.join(
                os.getenv('TEMP'),
                f"5ghz_cleaner_registry_backup_{safe_key_name}.reg"
            )
            
            from src.utils.system_commands import system_cmd
            system_cmd.run_reg(['export', key_path, backup_path, '/y'])
            
            return backup_path
        except Exception as e:
            print(f"[WARNING] Could not backup registry key {key_path}: {e}")
            return None
    
    @staticmethod
    def verify_admin_rights():
        """Vérifie que l'application a les droits administrateur"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    
    @staticmethod
    def is_system_file(filepath):
        """Vérifie si un fichier est un fichier système Windows"""
        system_paths = [
            os.path.join(os.getenv('WINDIR', 'C:\\Windows'), 'System32'),
            os.path.join(os.getenv('WINDIR', 'C:\\Windows'), 'SysWOW64'),
            os.path.join(os.getenv('WINDIR', 'C:\\Windows'), 'WinSxS'),
        ]
        
        filepath_normalized = os.path.normpath(filepath).upper()
        
        for sys_path in system_paths:
            if filepath_normalized.startswith(os.path.normpath(sys_path).upper()):
                return True
        
        return False
    
    @staticmethod
    def get_file_signature(filepath):
        """
        Vérifie la signature numérique d'un fichier via API native Windows (WinVerifyTrust)
        SÉCURITÉ: Utilise ctypes pour appeler directement l'API Windows
        
        Note: Cette fonction est rarement utilisée et sert principalement à vérifier
        l'intégrité des fichiers système. Elle retourne "Unknown" en cas d'erreur
        pour ne pas bloquer l'application.
        """
        try:
            import ctypes
            from ctypes import wintypes
            import uuid
            
            # Constantes WinVerifyTrust
            WTD_UI_NONE = 2
            WTD_REVOKE_NONE = 0
            WTD_CHOICE_FILE = 1
            WTD_STATEACTION_VERIFY = 1
            WTD_STATEACTION_CLOSE = 2
            
            # GUID pour WINTRUST_ACTION_GENERIC_VERIFY_V2
            class GUID(ctypes.Structure):
                _fields_ = [
                    ("Data1", wintypes.DWORD),
                    ("Data2", wintypes.WORD),
                    ("Data3", wintypes.WORD),
                    ("Data4", wintypes.BYTE * 8)
                ]
            
            # Structures Windows
            class WINTRUST_FILE_INFO(ctypes.Structure):
                _fields_ = [
                    ("cbStruct", wintypes.DWORD),
                    ("pcwszFilePath", wintypes.LPCWSTR),
                    ("hFile", wintypes.HANDLE),
                    ("pgKnownSubject", ctypes.POINTER(GUID))
                ]
            
            class WINTRUST_DATA(ctypes.Structure):
                _fields_ = [
                    ("cbStruct", wintypes.DWORD),
                    ("pPolicyCallbackData", ctypes.c_void_p),
                    ("pSIPClientData", ctypes.c_void_p),
                    ("dwUIChoice", wintypes.DWORD),
                    ("fdwRevocationChecks", wintypes.DWORD),
                    ("dwUnionChoice", wintypes.DWORD),
                    ("pFile", ctypes.POINTER(WINTRUST_FILE_INFO)),
                    ("dwStateAction", wintypes.DWORD),
                    ("hWVTStateData", wintypes.HANDLE),
                    ("pwszURLReference", wintypes.LPCWSTR),
                    ("dwProvFlags", wintypes.DWORD),
                    ("dwUIContext", wintypes.DWORD)
                ]
            
            # Créer le GUID pour WINTRUST_ACTION_GENERIC_VERIFY_V2
            action_guid = GUID()
            action_guid.Data1 = 0x00AAC56B
            action_guid.Data2 = 0xCD44
            action_guid.Data3 = 0x11d0
            action_guid.Data4 = (wintypes.BYTE * 8)(0x8C, 0xC2, 0x00, 0xC0, 0x4F, 0xC2, 0x95, 0xEE)
            
            # Initialiser les structures
            file_info = WINTRUST_FILE_INFO()
            file_info.cbStruct = ctypes.sizeof(WINTRUST_FILE_INFO)
            file_info.pcwszFilePath = filepath
            file_info.hFile = None
            file_info.pgKnownSubject = None
            
            trust_data = WINTRUST_DATA()
            trust_data.cbStruct = ctypes.sizeof(WINTRUST_DATA)
            trust_data.pPolicyCallbackData = None
            trust_data.pSIPClientData = None
            trust_data.dwUIChoice = WTD_UI_NONE
            trust_data.fdwRevocationChecks = WTD_REVOKE_NONE
            trust_data.dwUnionChoice = WTD_CHOICE_FILE
            trust_data.pFile = ctypes.pointer(file_info)
            trust_data.dwStateAction = WTD_STATEACTION_VERIFY
            trust_data.hWVTStateData = None
            trust_data.pwszURLReference = None
            trust_data.dwProvFlags = 0
            trust_data.dwUIContext = 0
            
            # Appeler WinVerifyTrust
            wintrust = ctypes.windll.wintrust
            result = wintrust.WinVerifyTrust(
                None,
                ctypes.byref(action_guid),
                ctypes.byref(trust_data)
            )
            
            # Nettoyer (fermer le handle)
            trust_data.dwStateAction = WTD_STATEACTION_CLOSE
            wintrust.WinVerifyTrust(None, ctypes.byref(action_guid), ctypes.byref(trust_data))
            
            # Interpréter le résultat
            if result == 0:
                return "Valid"
            elif result == 0x800B0100:
                return "NotSigned"
            elif result == 0x800B0109:
                return "NotTrusted"
            elif result == 0x80096010:
                return "Invalid"
            else:
                return f"Error_{hex(result)}"
                
        except Exception as e:
            print(f"[WARNING] Signature verification failed: {e}")
            return "Unknown"


# Instance globale du gestionnaire de sécurité
security_manager = SecurityManager()
