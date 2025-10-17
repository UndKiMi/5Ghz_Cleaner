"""
Module de logging structuré pour production
SÉCURITÉ: Logs contrôlés, pas de pollution console, niveaux appropriés
"""
import logging
import sys
import os
from pathlib import Path
from datetime import datetime


class ProductionLogger:
    """
    Logger structuré pour production avec niveaux appropriés
    
    Features:
    - Logs dans fichier ET console (mode debug uniquement)
    - Rotation automatique des logs
    - Niveaux de log configurables
    - Format structuré avec timestamps
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
        if ProductionLogger._initialized:
            return
        
        # Configuration depuis variables d'environnement
        self.debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
        log_level_str = os.getenv('LOG_LEVEL', 'INFO').upper()
        
        # Convertir le niveau de log
        log_level = getattr(logging, log_level_str, logging.INFO)
        
        # Créer le dossier de logs
        log_dir = Path.home() / "Documents" / "5GH'zCleaner-logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Nom du fichier de log avec timestamp
        log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
        
        # Configuration du logger
        self.logger = logging.getLogger('5GHzCleaner')
        self.logger.setLevel(logging.DEBUG)  # Capturer tous les niveaux
        
        # Supprimer les handlers existants
        self.logger.handlers.clear()
        
        # Format des logs
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler fichier (toujours actif)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Handler console (seulement si debug)
        if self.debug_mode:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        ProductionLogger._initialized = True
        
        # Log initial
        self.logger.info("=" * 80)
        self.logger.info("5GH'z Cleaner - Application started")
        self.logger.info(f"Debug mode: {self.debug_mode}")
        self.logger.info(f"Log level: {log_level_str}")
        self.logger.info(f"Log file: {log_file}")
        self.logger.info("=" * 80)
    
    def info(self, message: str):
        """Log niveau INFO (toujours visible dans fichier)"""
        self.logger.info(message)
    
    def debug(self, message: str):
        """Log niveau DEBUG (seulement si debug_mode)"""
        self.logger.debug(message)
    
    def warning(self, message: str):
        """Log niveau WARNING"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log niveau ERROR"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log niveau CRITICAL"""
        self.logger.critical(message)
    
    def success(self, message: str):
        """Log succès (niveau INFO avec préfixe)"""
        self.logger.info(f"[SUCCESS] {message}")
    
    def security(self, message: str):
        """Log sécurité (niveau WARNING avec préfixe)"""
        self.logger.warning(f"[SECURITY] {message}")


# Instance globale (singleton)
logger = ProductionLogger()


# Fonctions de compatibilité pour faciliter le remplacement de print()
def log_info(message: str):
    """Raccourci pour logger.info()"""
    logger.info(message)


def log_debug(message: str):
    """Raccourci pour logger.debug()"""
    logger.debug(message)


def log_warning(message: str):
    """Raccourci pour logger.warning()"""
    logger.warning(message)


def log_error(message: str):
    """Raccourci pour logger.error()"""
    logger.error(message)


def log_success(message: str):
    """Raccourci pour logger.success()"""
    logger.success(message)


def log_security(message: str):
    """Raccourci pour logger.security()"""
    logger.security(message)


if __name__ == "__main__":
    # Test du logger
    print("Testing ProductionLogger...")
    
    logger.info("This is an info message")
    logger.debug("This is a debug message (only visible if DEBUG=true)")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.success("This is a success message")
    logger.security("This is a security message")
    
    print("\nLogger test completed. Check the log file in Documents/5GH'zCleaner-logs/")
