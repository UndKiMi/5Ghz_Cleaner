"""
Système de logging avancé pour 5GH'z Cleaner
Features: Rotation, couleurs console, stacktraces détaillés, mode debug
"""
import logging
import sys
import os
import traceback
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Optional

# Import conditionnel de colorama pour console colorée
try:
    from colorama import init, Fore, Style, Back
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    # Fallback sans couleurs
    class Fore:
        RED = GREEN = YELLOW = BLUE = CYAN = MAGENTA = WHITE = RESET = ''
    class Style:
        BRIGHT = DIM = RESET_ALL = ''
    class Back:
        RED = GREEN = YELLOW = BLUE = RESET = ''


class ColoredConsoleFormatter(logging.Formatter):
    """
    Formatter avec couleurs pour la console
    """
    
    # Couleurs par niveau de log
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT + Back.RED,
    }
    
    def format(self, record):
        """Formate le message avec couleurs"""
        # Couleur selon le niveau
        color = self.COLORS.get(record.levelname, '')
        
        # Format: [HH:MM:SS] LEVEL - Module - Message
        timestamp = datetime.fromtimestamp(record.created).strftime('%H:%M:%S')
        
        # Nom du module (sans le chemin complet)
        module = record.module if record.module != '__main__' else 'main'
        
        # Message formaté
        if COLORAMA_AVAILABLE:
            formatted = f"{Style.DIM}[{timestamp}]{Style.RESET_ALL} {color}{record.levelname:8}{Style.RESET_ALL} {Style.DIM}│{Style.RESET_ALL} {module:15} {Style.DIM}│{Style.RESET_ALL} {record.getMessage()}"
        else:
            formatted = f"[{timestamp}] {record.levelname:8} │ {module:15} │ {record.getMessage()}"
        
        # Ajouter exception si présente
        if record.exc_info:
            formatted += '\n' + self.formatException(record.exc_info)
        
        return formatted


class DetailedFileFormatter(logging.Formatter):
    """
    Formatter détaillé pour les fichiers de log
    """
    
    def format(self, record):
        """Formate le message avec détails complets"""
        # Format: YYYY-MM-DD HH:MM:SS,mmm | LEVEL | Module.Function:Line | Message
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
        
        # Informations de contexte
        module = record.module
        function = record.funcName
        line = record.lineno
        
        # Message de base
        formatted = f"{timestamp} | {record.levelname:8} | {module}.{function}:{line} | {record.getMessage()}"
        
        # Ajouter exception avec stacktrace complet si présente
        if record.exc_info:
            formatted += '\n' + '=' * 100
            formatted += '\n' + self.formatException(record.exc_info)
            formatted += '\n' + '=' * 100
        
        return formatted


class AdvancedLogger:
    """
    Logger avancé avec rotation, couleurs, stacktraces détaillés
    
    Features:
    - Rotation automatique des logs (10 MB max par fichier, 5 fichiers)
    - Console colorée (si colorama disponible)
    - Stacktraces détaillés avec contexte
    - Mode debug verbeux
    - Format différent console/fichier
    - Pas de pollution console en production
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialise le logger (une seule fois)"""
        if AdvancedLogger._initialized:
            return
        
        # Configuration depuis variables d'environnement
        self.debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
        log_level_str = os.getenv('LOG_LEVEL', 'INFO').upper()
        
        # Convertir le niveau de log
        log_level = getattr(logging, log_level_str, logging.INFO)
        
        # Créer le dossier de logs
        self.log_dir = Path.home() / "Documents" / "5GH'zCleaner-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Nom du fichier de log
        log_file = self.log_dir / "5ghz_cleaner.log"
        
        # Configuration du logger principal
        self.logger = logging.getLogger('5GHzCleaner')
        self.logger.setLevel(logging.DEBUG)  # Capturer tous les niveaux
        
        # Supprimer les handlers existants
        self.logger.handlers.clear()
        
        # === HANDLER FICHIER avec rotation ===
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,  # Garder 5 fichiers
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)  # Tout dans le fichier
        file_handler.setFormatter(DetailedFileFormatter())
        self.logger.addHandler(file_handler)
        
        # === HANDLER CONSOLE (seulement si debug ou pour erreurs) ===
        console_handler = logging.StreamHandler(sys.stdout)
        
        if self.debug_mode:
            # Mode debug: tout afficher avec couleurs
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(ColoredConsoleFormatter())
        else:
            # Mode production: seulement WARNING et plus
            console_handler.setLevel(logging.WARNING)
            console_handler.setFormatter(ColoredConsoleFormatter())
        
        self.logger.addHandler(console_handler)
        
        AdvancedLogger._initialized = True
        
        # Log initial
        self.logger.info("=" * 100)
        self.logger.info("5GH'z Cleaner - Application started")
        self.logger.info(f"Debug mode: {self.debug_mode}")
        self.logger.info(f"Log level: {log_level_str}")
        self.logger.info(f"Log file: {log_file}")
        self.logger.info(f"Colorama available: {COLORAMA_AVAILABLE}")
        self.logger.info("=" * 100)
    
    def info(self, message: str, module: Optional[str] = None):
        """Log niveau INFO"""
        self.logger.info(message, extra={'module': module} if module else {})
    
    def debug(self, message: str, module: Optional[str] = None):
        """Log niveau DEBUG (verbeux, seulement si debug_mode)"""
        self.logger.debug(message, extra={'module': module} if module else {})
    
    def warning(self, message: str, module: Optional[str] = None):
        """Log niveau WARNING"""
        self.logger.warning(message, extra={'module': module} if module else {})
    
    def error(self, message: str, exc_info: bool = False, module: Optional[str] = None):
        """
        Log niveau ERROR
        
        Args:
            message: Message d'erreur
            exc_info: Si True, inclut le stacktrace complet
            module: Nom du module (optionnel)
        """
        self.logger.error(message, exc_info=exc_info, extra={'module': module} if module else {})
    
    def critical(self, message: str, exc_info: bool = True, module: Optional[str] = None):
        """
        Log niveau CRITICAL (toujours avec stacktrace)
        
        Args:
            message: Message critique
            exc_info: Si True, inclut le stacktrace complet (défaut: True)
            module: Nom du module (optionnel)
        """
        self.logger.critical(message, exc_info=exc_info, extra={'module': module} if module else {})
    
    def exception(self, message: str, module: Optional[str] = None):
        """
        Log une exception avec stacktrace complet
        À utiliser dans un bloc except
        
        Args:
            message: Message décrivant l'exception
            module: Nom du module (optionnel)
        """
        self.logger.exception(message, extra={'module': module} if module else {})
    
    def success(self, message: str, module: Optional[str] = None):
        """Log succès (niveau INFO avec préfixe)"""
        self.logger.info(f"✓ {message}", extra={'module': module} if module else {})
    
    def security(self, message: str, module: Optional[str] = None):
        """Log sécurité (niveau WARNING avec préfixe)"""
        self.logger.warning(f"🔒 [SECURITY] {message}", extra={'module': module} if module else {})
    
    def get_log_dir(self) -> Path:
        """Retourne le répertoire des logs"""
        return self.log_dir
    
    def get_log_files(self) -> list:
        """Retourne la liste des fichiers de log"""
        return list(self.log_dir.glob("5ghz_cleaner.log*"))


# Instance globale (singleton)
logger = AdvancedLogger()


# Fonctions de compatibilité
def log_info(message: str):
    """Raccourci pour logger.info()"""
    logger.info(message)


def log_debug(message: str):
    """Raccourci pour logger.debug()"""
    logger.debug(message)


def log_warning(message: str):
    """Raccourci pour logger.warning()"""
    logger.warning(message)


def log_error(message: str, exc_info: bool = False):
    """Raccourci pour logger.error()"""
    logger.error(message, exc_info=exc_info)


def log_exception(message: str):
    """Raccourci pour logger.exception() - À utiliser dans un except"""
    logger.exception(message)


def log_success(message: str):
    """Raccourci pour logger.success()"""
    logger.success(message)


def log_security(message: str):
    """Raccourci pour logger.security()"""
    logger.security(message)


if __name__ == "__main__":
    # Test du logger
    print("\n" + "=" * 100)
    print("Testing AdvancedLogger...")
    print("=" * 100 + "\n")
    
    logger.info("This is an info message")
    logger.debug("This is a debug message (only visible if DEBUG=true)")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.success("This is a success message")
    logger.security("This is a security message")
    
    # Test exception
    try:
        result = 1 / 0
    except Exception as e:
        logger.exception("Division by zero error occurred")
    
    print("\n" + "=" * 100)
    print(f"Logger test completed. Check logs in: {logger.get_log_dir()}")
    print(f"Log files: {[f.name for f in logger.get_log_files()]}")
    print("=" * 100 + "\n")
