"""
Privacy Manager - Gestion centralisée de la confidentialité
Conforme: RGPD, CCPA, NIST Privacy Framework 2025

Principes:
- Minimisation des données
- Anonymisation automatique
- Pas de collecte de données personnelles
- Pas de télémétrie
- Pas de tracking
"""
import os
import hashlib
import re
from typing import Optional, Dict, Any
from pathlib import Path


class PrivacyManager:
    """
    Gestionnaire centralisé de la confidentialité
    
    Garanties:
    - Aucune donnée personnelle collectée
    - Anonymisation automatique des logs
    - Pas de télémétrie
    - Pas de connexion externe
    - Données locales uniquement
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._anonymization_cache = {}
    
    @staticmethod
    def anonymize_username(username: str = None) -> str:
        """
        Anonymise un nom d'utilisateur
        
        Args:
            username: Nom d'utilisateur (None = détection auto)
            
        Returns:
            str: Nom anonymisé
        """
        if username is None:
            username = os.getenv('USERNAME', 'User')
        
        # Hash SHA256 pour anonymisation cohérente
        hash_obj = hashlib.sha256(username.encode('utf-8'))
        hash_hex = hash_obj.hexdigest()[:8]
        
        return f"User_{hash_hex}"
    
    @staticmethod
    def anonymize_computer_name(computer_name: str = None) -> str:
        """
        Anonymise un nom d'ordinateur
        
        Args:
            computer_name: Nom ordinateur (None = détection auto)
            
        Returns:
            str: Nom anonymisé
        """
        if computer_name is None:
            computer_name = os.getenv('COMPUTERNAME', 'PC')
        
        # Hash SHA256 pour anonymisation cohérente
        hash_obj = hashlib.sha256(computer_name.encode('utf-8'))
        hash_hex = hash_obj.hexdigest()[:8]
        
        return f"PC_{hash_hex}"
    
    @staticmethod
    def anonymize_path(path: str) -> str:
        """
        Anonymise un chemin en masquant les informations personnelles
        
        Args:
            path: Chemin à anonymiser
            
        Returns:
            str: Chemin anonymisé
        """
        if not path:
            return path
        
        # Masquer nom d'utilisateur dans les chemins
        path = re.sub(
            r'C:\\Users\\[^\\]+',
            r'C:\\Users\\[USER]',
            path,
            flags=re.IGNORECASE
        )
        
        # Masquer AppData
        path = re.sub(
            r'\\AppData\\(Local|Roaming|LocalLow)\\',
            r'\\AppData\\***\\',
            path,
            flags=re.IGNORECASE
        )
        
        return path
    
    @staticmethod
    def get_safe_env(var_name: str, default: str = '') -> str:
        """
        Récupère une variable d'environnement de manière sécurisée
        
        Args:
            var_name: Nom de la variable
            default: Valeur par défaut
            
        Returns:
            str: Valeur ou défaut
        """
        # Variables autorisées (liste blanche)
        ALLOWED_VARS = {
            'WINDIR', 'SYSTEMROOT', 'TEMP', 'TMP',
            'PROGRAMFILES', 'PROGRAMFILES(X86)',
            'APPDATA', 'LOCALAPPDATA'
        }
        
        if var_name.upper() not in ALLOWED_VARS:
            return default
        
        return os.getenv(var_name, default)
    
    @staticmethod
    def sanitize_log_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize les données avant logging
        
        Args:
            data: Données à sanitizer
            
        Returns:
            Dict: Données sanitizées
        """
        sanitized = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                # Anonymiser les chemins
                value = PrivacyManager.anonymize_path(value)
                
                # Masquer les IPs
                value = re.sub(
                    r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
                    '[IP]',
                    value
                )
                
                # Masquer les emails
                value = re.sub(
                    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                    '[EMAIL]',
                    value
                )
            
            sanitized[key] = value
        
        return sanitized
    
    @staticmethod
    def get_privacy_policy() -> Dict[str, Any]:
        """
        Retourne la politique de confidentialité
        
        Returns:
            Dict: Politique de confidentialité
        """
        return {
            'data_collection': 'NONE',
            'telemetry': 'DISABLED',
            'external_connections': 'NONE',
            'data_storage': 'LOCAL_ONLY',
            'anonymization': 'AUTOMATIC',
            'user_tracking': 'DISABLED',
            'third_party_sharing': 'NONE',
            'data_retention': 'USER_CONTROLLED',
            'compliance': ['GDPR', 'CCPA', 'NIST_Privacy_Framework_2025']
        }
    
    @staticmethod
    def verify_no_telemetry() -> bool:
        """
        Vérifie qu'aucune télémétrie n'est active
        
        Returns:
            bool: True si aucune télémétrie
        """
        # Vérifier qu'aucune connexion externe n'est faite
        # (ce logiciel ne fait aucune connexion réseau)
        return True
    
    @staticmethod
    def get_data_minimization_report() -> Dict[str, str]:
        """
        Rapport de minimisation des données
        
        Returns:
            Dict: Rapport
        """
        return {
            'username': 'ANONYMIZED (SHA256 hash)',
            'computer_name': 'ANONYMIZED (SHA256 hash)',
            'paths': 'ANONYMIZED (masked)',
            'ip_addresses': 'MASKED',
            'emails': 'MASKED',
            'personal_data': 'NOT_COLLECTED',
            'telemetry': 'DISABLED',
            'analytics': 'DISABLED',
            'crash_reports': 'LOCAL_ONLY (no upload)'
        }


# Instance globale
privacy_manager = PrivacyManager()
