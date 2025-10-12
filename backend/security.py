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
            for service in critical_services:
                result = subprocess.run(
                    ['sc', 'query', service],
                    capture_output=True,
                    timeout=5
                )
                if result.returncode != 0:
                    self.warnings.append(f"Service {service} not available")
        except:
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
            backup_path = os.path.join(
                os.getenv('TEMP'),
                f"5ghz_cleaner_registry_backup_{key_path.replace('\\', '_')}.reg"
            )
            
            subprocess.run(
                ['reg', 'export', key_path, backup_path, '/y'],
                capture_output=True,
                timeout=10
            )
            
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
        """Vérifie la signature numérique d'un fichier"""
        try:
            result = subprocess.run(
                ['powershell', '-Command', 
                 f'(Get-AuthenticodeSignature "{filepath}").Status'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            return result.stdout.strip()
        except:
            return "Unknown"


# Instance globale du gestionnaire de sécurité
security_manager = SecurityManager()
