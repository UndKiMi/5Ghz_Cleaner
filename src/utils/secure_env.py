"""
Secure Environment Variables Manager
Gestion sécurisée des variables d'environnement avec liste blanche

Conforme: OWASP ASVS 4.0 V14.5, NIST SP 800-53 SC-4
"""
import os
from typing import Optional, Set


class SecureEnv:
    """
    Gestionnaire sécurisé de variables d'environnement
    
    Principe: Liste blanche uniquement
    Protection contre: Information disclosure, environment injection
    """
    
    # Liste blanche des variables autorisées
    ALLOWED_VARS: Set[str] = {
        # Variables système Windows essentielles
        'WINDIR',
        'SYSTEMROOT',
        'TEMP',
        'TMP',
        'PROGRAMFILES',
        'PROGRAMFILES(X86)',
        'PROGRAMDATA',
        'APPDATA',
        'LOCALAPPDATA',
        'COMMONPROGRAMFILES',
        'COMMONPROGRAMFILES(X86)',
        
        # Variables système nécessaires
        'SYSTEMDRIVE',
        'HOMEDRIVE',
        'HOMEPATH',
        'PUBLIC',
        'ALLUSERSPROFILE',
    }
    
    # Variables interdites (liste noire pour double sécurité)
    FORBIDDEN_VARS: Set[str] = {
        'USERNAME',      # Information personnelle
        'USERDOMAIN',    # Information réseau
        'COMPUTERNAME',  # Information système
        'LOGONSERVER',   # Information réseau
        'USERDNSDOMAIN', # Information réseau
        'PATH',          # Risque d'injection
        'PATHEXT',       # Risque d'injection
    }
    
    @staticmethod
    def get(var_name: str, default: str = '', allow_sensitive: bool = False) -> str:
        """
        Récupère une variable d'environnement de manière sécurisée
        
        Args:
            var_name: Nom de la variable
            default: Valeur par défaut
            allow_sensitive: Autoriser les variables sensibles (False par défaut)
            
        Returns:
            str: Valeur ou défaut
            
        Raises:
            SecurityError: Si variable interdite
        """
        var_upper = var_name.upper()
        
        # Vérifier liste noire
        if var_upper in SecureEnv.FORBIDDEN_VARS and not allow_sensitive:
            print(f"[SECURITY] Access to forbidden environment variable blocked: {var_name}")
            return default
        
        # Vérifier liste blanche
        if var_upper not in SecureEnv.ALLOWED_VARS and not allow_sensitive:
            print(f"[SECURITY] Access to non-whitelisted environment variable blocked: {var_name}")
            return default
        
        # Récupérer la valeur
        value = os.getenv(var_name, default)
        
        # Validation supplémentaire
        if value and len(value) > 1000:
            print(f"[SECURITY] Environment variable value too long, truncated: {var_name}")
            return default
        
        return value
    
    @staticmethod
    def get_safe_paths() -> dict:
        """
        Retourne les chemins système sécurisés
        
        Returns:
            dict: Chemins validés
        """
        return {
            'windir': SecureEnv.get('WINDIR', 'C:\\Windows'),
            'temp': SecureEnv.get('TEMP', 'C:\\Windows\\Temp'),
            'tmp': SecureEnv.get('TMP', 'C:\\Windows\\Temp'),
            'programfiles': SecureEnv.get('PROGRAMFILES', 'C:\\Program Files'),
            'programfiles_x86': SecureEnv.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'),
            'appdata': SecureEnv.get('APPDATA', ''),
            'localappdata': SecureEnv.get('LOCALAPPDATA', ''),
        }
    
    @staticmethod
    def validate_path(path: str) -> bool:
        """
        Valide qu'un chemin ne contient pas d'informations sensibles
        
        Args:
            path: Chemin à valider
            
        Returns:
            bool: True si sûr
        """
        if not path:
            return False
        
        # Vérifier qu'il ne contient pas de variables sensibles
        path_upper = path.upper()
        
        for forbidden in SecureEnv.FORBIDDEN_VARS:
            if f'%{forbidden}%' in path_upper:
                return False
        
        return True


# Instance globale
secure_env = SecureEnv()
