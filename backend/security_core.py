"""
Module de Sécurité Principal - 5GHz Cleaner
Basé sur les recommandations officielles Microsoft
AUCUNE MODIFICATION UTILISATEUR AUTORISÉE
"""
import os
import re
from pathlib import Path

# ============================================================================
# BLOCKLIST SYSTÈME WINDOWS - PROTECTION MAXIMALE
# Basé sur: https://docs.microsoft.com/en-us/windows/win32/fileio/file-system-functionality-comparison
# ============================================================================

class WindowsSecurityCore:
    """Classe de sécurité immuable pour la protection du système Windows"""
    
    # Chemins système ABSOLUMENT INTERDITS
    CRITICAL_SYSTEM_PATHS = frozenset({
        # Noyau Windows
        r'C:\Windows\System32',
        r'C:\Windows\SysWOW64',
        r'C:\Windows\WinSxS',
        r'C:\Windows\servicing',
        
        # Boot et démarrage
        r'C:\Windows\Boot',
        r'C:\Windows\System',
        r'C:\Boot',
        r'C:\EFI',
        r'C:\Recovery',
        
        # Pilotes et matériel
        r'C:\Windows\System32\drivers',
        r'C:\Windows\System32\DriverStore',
        r'C:\Windows\inf',
        
        # Polices et ressources
        r'C:\Windows\Fonts',
        r'C:\Windows\Resources',
        r'C:\Windows\Cursors',
        
        # Assemblies et composants
        r'C:\Windows\assembly',
        r'C:\Windows\Microsoft.NET',
        
        # Configuration et registre
        r'C:\Windows\Registration',
        r'C:\Windows\PolicyDefinitions',
        r'C:\Windows\System32\config',
        
        # Applications système
        r'C:\Windows\SystemApps',
        r'C:\Windows\ImmersiveControlPanel',
        r'C:\Windows\ShellExperiences',
        r'C:\Windows\ShellComponents',
        
        # Programmes
        r'C:\Program Files',
        r'C:\Program Files (x86)',
        r'C:\ProgramData\Microsoft\Windows',
        
        # Utilisateurs système
        r'C:\Users\Default',
        r'C:\Users\Public',
        r'C:\Users\All Users',
        
        # Logs système critiques
        r'C:\Windows\Logs\CBS',
        r'C:\Windows\Logs\DISM',
        r'C:\Windows\Logs\DPX',
        r'C:\Windows\Logs\MoSetup',
        
        # Windows Update
        r'C:\Windows\SoftwareDistribution\DataStore',
        r'C:\Windows\SoftwareDistribution\SelfUpdate',
        
        # Sécurité Windows Defender
        r'C:\ProgramData\Microsoft\Windows Defender',
        r'C:\Program Files\Windows Defender',
        
        # Activation et licence
        r'C:\Windows\System32\spp',
        r'C:\Windows\ServiceProfiles',
    })
    
    # Dossiers protégés (noms uniquement)
    PROTECTED_FOLDER_NAMES = frozenset({
        'System32', 'SysWOW64', 'WinSxS', 'Boot', 'System', 'inf',
        'Fonts', 'assembly', 'Registration', 'servicing', 'PolicyDefinitions',
        'DriverStore', 'drivers', 'Microsoft.NET', 'SystemApps',
        'ImmersiveControlPanel', 'ShellExperiences', 'ShellComponents',
        'WindowsApps', 'Packages', 'AppReadiness', 'CSC', 'Installer',
        'rescache', 'Resources', 'Cursors', 'config', 'spp',
        'ServiceProfiles', 'NetworkService', 'LocalService',
    })
    
    # Fichiers système CRITIQUES - Ne JAMAIS supprimer
    CRITICAL_SYSTEM_FILES = frozenset({
        # Noyau Windows
        'ntoskrnl.exe', 'hal.dll', 'ntdll.dll', 'kernel32.dll',
        'kernelbase.dll', 'user32.dll', 'gdi32.dll', 'advapi32.dll',
        'shell32.dll', 'ole32.dll', 'oleaut32.dll', 'msvcrt.dll',
        
        # Processus système essentiels
        'explorer.exe', 'csrss.exe', 'services.exe', 'lsass.exe',
        'winlogon.exe', 'svchost.exe', 'dwm.exe', 'taskhost.exe',
        'taskhostw.exe', 'smss.exe', 'wininit.exe', 'fontdrvhost.exe',
        
        # Gestionnaire de session
        'conhost.exe', 'dllhost.exe', 'runtimebroker.exe',
        'sihost.exe', 'ctfmon.exe', 'searchindexer.exe',
        
        # Fichiers de boot
        'bootmgr', 'bootmgfw.efi', 'winload.exe', 'winload.efi',
        'winresume.exe', 'winresume.efi', 'memtest.exe',
        
        # Fichiers de configuration système
        'boot.ini', 'bootstat.dat', 'hiberfil.sys', 'pagefile.sys',
        'swapfile.sys', 'ntuser.dat', 'system.dat', 'usrclass.dat',
        
        # Registre Windows
        'sam', 'security', 'software', 'system', 'default',
        'ntuser.ini', 'ntuser.pol', 'system.ini', 'win.ini',
        
        # Windows Update
        'wuaueng.dll', 'wuapi.dll', 'wuauserv', 'wudriver.dll',
        'wups.dll', 'wups2.dll', 'wuwebv.dll', 'wucltux.dll',
        
        # Windows Defender
        'msmpeng.exe', 'msseces.exe', 'mpcmdrun.exe', 'mpsigstub.exe',
        'mpengine.dll', 'mpasbase.vdm', 'mpavbase.vdm',
        
        # Pilotes critiques
        'ntfs.sys', 'disk.sys', 'classpnp.sys', 'partmgr.sys',
        'volmgr.sys', 'volsnap.sys', 'mountmgr.sys', 'fltmgr.sys',
        
        # Logs système importants
        'setupapi.dev.log', 'setupapi.app.log', 'windowsupdate.log',
        'cbs.log', 'dism.log', 'panther.log',
    })
    
    # Extensions ABSOLUMENT PROTÉGÉES
    PROTECTED_EXTENSIONS = frozenset({
        # Exécutables et bibliothèques
        '.exe', '.dll', '.sys', '.drv', '.ocx', '.cpl', '.scr',
        
        # Pilotes et installation
        '.inf', '.cat', '.pnf', '.msi', '.msu', '.cab',
        
        # Manifestes et configuration
        '.manifest', '.mui', '.mof', '.mfl', '.mum',
        
        # Registre et politique
        '.pol', '.adm', '.admx', '.adml', '.reg',
        
        # Données système
        '.dat', '.ini', '.cfg', '.config', '.xml',
        
        # Sécurité
        '.p7b', '.cer', '.crt', '.pfx',
    })
    
    # Patterns de fichiers système (regex)
    SYSTEM_FILE_PATTERNS = [
        re.compile(r'^ntuser\..*', re.IGNORECASE),
        re.compile(r'^usrclass\..*', re.IGNORECASE),
        re.compile(r'^system\..*', re.IGNORECASE),
        re.compile(r'^sam\..*', re.IGNORECASE),
        re.compile(r'^security\..*', re.IGNORECASE),
        re.compile(r'^software\..*', re.IGNORECASE),
        re.compile(r'^default\..*', re.IGNORECASE),
        re.compile(r'^boot.*\.log$', re.IGNORECASE),
        re.compile(r'^setupapi\..*\.log$', re.IGNORECASE),
        re.compile(r'^.*\.sys$', re.IGNORECASE),
        re.compile(r'^.*\.drv$', re.IGNORECASE),
        re.compile(r'^.*\.inf$', re.IGNORECASE),
        re.compile(r'^.*\.cat$', re.IGNORECASE),
    ]
    
    # Dossiers temporaires AUTORISÉS UNIQUEMENT
    @staticmethod
    def get_allowed_temp_directories():
        """Retourne les dossiers temporaires autorisés"""
        allowed = set()
        
        # Temp utilisateur
        if os.getenv('TEMP'):
            allowed.add(os.path.normpath(os.getenv('TEMP')))
        if os.getenv('TMP'):
            allowed.add(os.path.normpath(os.getenv('TMP')))
        
        # Temp Windows (avec précaution)
        windir = os.getenv('WINDIR', 'C:\\Windows')
        windows_temp = os.path.join(windir, 'Temp')
        if os.path.exists(windows_temp):
            allowed.add(os.path.normpath(windows_temp))
        
        return frozenset(allowed)
    
    @staticmethod
    def is_path_safe(path: str) -> bool:
        """
        Vérifie si un chemin est sûr à manipuler
        
        Args:
            path: Chemin à vérifier
            
        Returns:
            bool: True si sûr, False sinon
        """
        if not path:
            return False
        
        try:
            # Normaliser le chemin
            normalized_path = os.path.normpath(os.path.abspath(path))
            
            # Vérifier les chemins critiques
            for critical_path in WindowsSecurityCore.CRITICAL_SYSTEM_PATHS:
                critical_normalized = os.path.normpath(critical_path)
                
                # Vérifier si le chemin est dans un répertoire critique
                if normalized_path.lower().startswith(critical_normalized.lower()):
                    return False
                
                # Vérifier si c'est exactement un chemin critique
                if normalized_path.lower() == critical_normalized.lower():
                    return False
            
            # Vérifier les dossiers protégés dans le chemin
            path_parts = Path(normalized_path).parts
            for part in path_parts:
                if part in WindowsSecurityCore.PROTECTED_FOLDER_NAMES:
                    return False
            
            # Vérifier si c'est un fichier système critique
            filename = os.path.basename(normalized_path).lower()
            if filename in {f.lower() for f in WindowsSecurityCore.CRITICAL_SYSTEM_FILES}:
                return False
            
            # Vérifier l'extension
            _, ext = os.path.splitext(normalized_path)
            if ext.lower() in WindowsSecurityCore.PROTECTED_EXTENSIONS:
                # Exception: fichiers .tmp dans les dossiers temp autorisés
                if ext.lower() == '.tmp':
                    parent_dir = os.path.dirname(normalized_path)
                    allowed_temps = WindowsSecurityCore.get_allowed_temp_directories()
                    if any(parent_dir.lower().startswith(allowed.lower()) for allowed in allowed_temps):
                        return True
                return False
            
            # Vérifier les patterns de fichiers système
            for pattern in WindowsSecurityCore.SYSTEM_FILE_PATTERNS:
                if pattern.match(filename):
                    return False
            
            return True
            
        except Exception as e:
            # En cas d'erreur, refuser par sécurité
            print(f"[SECURITY] Error checking path safety: {e}")
            return False
    
    @staticmethod
    def is_in_allowed_temp_directory(path: str) -> bool:
        """
        Vérifie si un chemin est dans un dossier temporaire autorisé
        
        Args:
            path: Chemin à vérifier
            
        Returns:
            bool: True si dans un dossier temp autorisé
        """
        if not path:
            return False
        
        try:
            normalized_path = os.path.normpath(os.path.abspath(path))
            allowed_temps = WindowsSecurityCore.get_allowed_temp_directories()
            
            for allowed_temp in allowed_temps:
                if normalized_path.lower().startswith(allowed_temp.lower()):
                    return True
            
            return False
            
        except Exception:
            return False
    
    @staticmethod
    def validate_operation(path: str, operation: str = "delete") -> tuple[bool, str]:
        """
        Valide une opération sur un fichier/dossier
        
        Args:
            path: Chemin du fichier/dossier
            operation: Type d'opération ("delete", "modify", "read")
            
        Returns:
            tuple: (is_safe, reason)
        """
        if not path:
            return False, "Chemin vide"
        
        # Vérifier la sécurité du chemin
        if not WindowsSecurityCore.is_path_safe(path):
            return False, "Chemin système protégé - Accès refusé"
        
        # Pour les opérations de suppression, vérifier qu'on est dans temp
        if operation == "delete":
            if not WindowsSecurityCore.is_in_allowed_temp_directory(path):
                return False, "Suppression autorisée uniquement dans les dossiers temporaires"
        
        return True, "Opération autorisée"


# Instance globale immuable
security_core = WindowsSecurityCore()
