"""
Module de sanitization des logs
Masque les informations sensibles dans les logs
"""
import re
import os
from typing import Optional


class LogSanitizer:
    """Sanitizer pour les logs - Masque les informations sensibles"""
    
    # Patterns de détection
    PATTERNS = {
        # Chemins utilisateurs Windows
        'user_path': re.compile(r'C:\\Users\\[^\\]+', re.IGNORECASE),
        'user_path_forward': re.compile(r'C:/Users/[^/]+', re.IGNORECASE),
        
        # Adresses IP
        'ipv4': re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
        'ipv6': re.compile(r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b'),
        
        # Adresses email
        'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
        
        # Clés API / Tokens (patterns génériques)
        'api_key': re.compile(r'\b[A-Za-z0-9]{32,}\b'),  # 32+ caractères alphanumériques
        
        # Mots de passe dans les commandes
        'password': re.compile(r'(password|passwd|pwd)[\s=:]+[^\s]+', re.IGNORECASE),
        
        # Noms d'utilisateur Windows
        'username': re.compile(r'\\Users\\([^\\]+)\\', re.IGNORECASE),
        
        # SID Windows
        'sid': re.compile(r'S-1-\d+-\d+-\d+-\d+-\d+-\d+'),
        
        # Chemins de profil
        'appdata': re.compile(r'C:\\Users\\[^\\]+\\AppData', re.IGNORECASE),
        'localappdata': re.compile(r'C:\\Users\\[^\\]+\\AppData\\Local', re.IGNORECASE),
        'roaming': re.compile(r'C:\\Users\\[^\\]+\\AppData\\Roaming', re.IGNORECASE),
    }
    
    # Remplacements
    REPLACEMENTS = {
        'user_path': r'C:\\Users\\***',
        'user_path_forward': r'C:/Users/***',
        'ipv4': '[IP_MASKED]',
        'ipv6': '[IP_MASKED]',
        'email': '[EMAIL_MASKED]',
        'api_key': '[KEY_MASKED]',
        'password': r'\1 [PASSWORD_MASKED]',
        'username': r'\\Users\\[USER]\\',
        'sid': '[SID_MASKED]',
        'appdata': r'C:\\Users\\***\\AppData',
        'localappdata': r'C:\\Users\\***\\AppData\\Local',
        'roaming': r'C:\\Users\\***\\AppData\\Roaming',
    }
    
    @staticmethod
    def sanitize(text: str, aggressive: bool = False) -> str:
        """
        Sanitize un texte en masquant les informations sensibles
        
        Args:
            text: Texte à sanitizer
            aggressive: Si True, masque plus d'informations
            
        Returns:
            str: Texte sanitizé
        """
        if not text:
            return text
        
        sanitized = text
        
        # Appliquer tous les patterns
        for pattern_name, pattern in LogSanitizer.PATTERNS.items():
            replacement = LogSanitizer.REPLACEMENTS.get(pattern_name, '[MASKED]')
            sanitized = pattern.sub(replacement, sanitized)
        
        # Mode agressif : masquer aussi les noms de fichiers
        if aggressive:
            # Masquer les extensions de fichiers sensibles
            sanitized = re.sub(r'\b\w+\.(key|pem|p12|pfx|cer|crt)\b', '[CERT_FILE]', sanitized, flags=re.IGNORECASE)
            
            # Masquer les chemins complets (garder seulement le nom de fichier)
            sanitized = re.sub(r'[A-Z]:\\(?:[^\\]+\\)+([^\\]+)', r'...\\\1', sanitized)
        
        return sanitized
    
    @staticmethod
    def sanitize_path(path: str) -> str:
        """
        Sanitize un chemin de fichier
        
        Args:
            path: Chemin à sanitizer
            
        Returns:
            str: Chemin sanitizé
        """
        if not path:
            return path
        
        # Masquer le nom d'utilisateur dans les chemins
        sanitized = re.sub(r'C:\\Users\\[^\\]+', r'C:\Users\***', path, flags=re.IGNORECASE)
        sanitized = re.sub(r'C:/Users/[^/]+', r'C:/Users/***', sanitized, flags=re.IGNORECASE)
        
        return sanitized
    
    @staticmethod
    def sanitize_command(command: str) -> str:
        """
        Sanitize une commande système
        
        Args:
            command: Commande à sanitizer
            
        Returns:
            str: Commande sanitizée
        """
        if not command:
            return command
        
        sanitized = command
        
        # Masquer les mots de passe
        sanitized = re.sub(r'(password|passwd|pwd)[\s=:]+[^\s]+', r'\1 [MASKED]', sanitized, flags=re.IGNORECASE)
        
        # Masquer les tokens
        sanitized = re.sub(r'(token|key|secret)[\s=:]+[^\s]+', r'\1 [MASKED]', sanitized, flags=re.IGNORECASE)
        
        # Masquer les chemins utilisateurs
        sanitized = LogSanitizer.sanitize_path(sanitized)
        
        return sanitized
    
    @staticmethod
    def get_safe_username() -> str:
        """
        Obtient un nom d'utilisateur masqué
        
        Returns:
            str: Nom d'utilisateur masqué
        """
        try:
            username = os.getenv('USERNAME', 'Unknown')
            # Masquer partiellement : garder première et dernière lettre
            if len(username) > 2:
                return f"{username[0]}{'*' * (len(username) - 2)}{username[-1]}"
            else:
                return "***"
        except:
            return "***"
    
    @staticmethod
    def sanitize_error(error_message: str) -> str:
        """
        Sanitize un message d'erreur
        
        Args:
            error_message: Message d'erreur
            
        Returns:
            str: Message sanitizé
        """
        if not error_message:
            return error_message
        
        # Sanitizer le message complet
        sanitized = LogSanitizer.sanitize(error_message, aggressive=False)
        
        # Masquer les stack traces qui contiennent des chemins
        sanitized = re.sub(r'File "([^"]+)"', lambda m: f'File "{LogSanitizer.sanitize_path(m.group(1))}"', sanitized)
        
        return sanitized


# Fonction helper pour intégration facile
def sanitize_log(message: str, aggressive: bool = False) -> str:
    """
    Fonction helper pour sanitizer rapidement un message de log
    
    Args:
        message: Message à sanitizer
        aggressive: Mode agressif
        
    Returns:
        str: Message sanitizé
    """
    return LogSanitizer.sanitize(message, aggressive)


# Décorateur pour sanitizer automatiquement les logs
def sanitize_logs(func):
    """
    Décorateur pour sanitizer automatiquement les logs d'une fonction
    """
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            # Sanitizer le message d'erreur
            sanitized_error = LogSanitizer.sanitize_error(str(e))
            print(f"[ERROR] {sanitized_error}")
            raise
    return wrapper


if __name__ == "__main__":
    # Tests du module
    print("=== Log Sanitizer Test ===\n")
    
    # Test 1: Chemin utilisateur
    test1 = r"C:\Users\JohnDoe\Documents\file.txt"
    print(f"Original: {test1}")
    print(f"Sanitized: {LogSanitizer.sanitize(test1)}\n")
    
    # Test 2: Adresse IP
    test2 = "Connection to 192.168.1.100 failed"
    print(f"Original: {test2}")
    print(f"Sanitized: {LogSanitizer.sanitize(test2)}\n")
    
    # Test 3: Email
    test3 = "User email: john.doe@example.com"
    print(f"Original: {test3}")
    print(f"Sanitized: {LogSanitizer.sanitize(test3)}\n")
    
    # Test 4: Commande avec mot de passe
    test4 = "net user admin password=MySecretPass123"
    print(f"Original: {test4}")
    print(f"Sanitized: {LogSanitizer.sanitize_command(test4)}\n")
    
    # Test 5: Mode agressif
    test5 = r"C:\Users\JohnDoe\AppData\Local\Temp\secret.key"
    print(f"Original: {test5}")
    print(f"Sanitized (normal): {LogSanitizer.sanitize(test5, aggressive=False)}")
    print(f"Sanitized (aggressive): {LogSanitizer.sanitize(test5, aggressive=True)}\n")
