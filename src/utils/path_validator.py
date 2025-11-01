"""
Module de validation avancée des chemins
Gère les liens symboliques, hard links et junction points Windows
"""
import os
import ctypes
from ctypes import wintypes
from pathlib import Path


class PathValidator:
    """Validateur avancé de chemins avec support des liens"""
    
    # Constantes Windows pour les attributs de fichiers
    FILE_ATTRIBUTE_REPARSE_POINT = 0x400
    FILE_ATTRIBUTE_DIRECTORY = 0x10
    
    @staticmethod
    def is_junction_point(path: str) -> bool:
        """
        Vérifie si un chemin est un junction point Windows
        
        Args:
            path: Chemin à vérifier
            
        Returns:
            bool: True si c'est un junction point
        """
        try:
            attrs = ctypes.windll.kernel32.GetFileAttributesW(path)
            
            # Vérifier si le fichier existe
            if attrs == -1:
                return False
            
            # Vérifier si c'est un reparse point (junction, symlink, etc.)
            is_reparse = (attrs & PathValidator.FILE_ATTRIBUTE_REPARSE_POINT) != 0
            is_dir = (attrs & PathValidator.FILE_ATTRIBUTE_DIRECTORY) != 0
            
            # Un junction point est un reparse point qui est aussi un dossier
            return is_reparse and is_dir
            
        except Exception as e:
            print(f"[WARNING] Failed to check junction point: {e}")
            return False
    
    @staticmethod
    def is_hard_link(path: str) -> bool:
        """
        Vérifie si un fichier est un hard link (nlink > 1)
        
        Args:
            path: Chemin du fichier
            
        Returns:
            bool: True si c'est un hard link
        """
        try:
            stat_info = os.stat(path)
            # Un fichier avec nlink > 1 a plusieurs hard links
            return stat_info.st_nlink > 1
        except Exception as e:
            print(f"[WARNING] Failed to check hard link: {e}")
            return False
    
    @staticmethod
    def resolve_symlink_safe(path: str, allowed_paths: list) -> tuple[bool, str]:
        """
        Résout un lien symbolique et vérifie qu'il pointe vers un chemin autorisé
        
        Args:
            path: Chemin du lien symbolique
            allowed_paths: Liste des chemins autorisés
            
        Returns:
            tuple: (is_safe, resolved_path or reason)
        """
        try:
            # Résoudre le lien symbolique
            real_path = os.path.realpath(path)
            
            # Normaliser le chemin résolu
            real_path_normalized = os.path.normpath(os.path.abspath(real_path))
            
            # Vérifier que le chemin résolu est dans un dossier autorisé
            for allowed in allowed_paths:
                allowed_normalized = os.path.normpath(os.path.abspath(allowed))
                if real_path_normalized.lower().startswith(allowed_normalized.lower()):
                    return True, real_path_normalized
            
            return False, f"Symlink target outside allowed paths: {real_path_normalized}"
            
        except Exception as e:
            return False, f"Failed to resolve symlink: {e}"
    
    @staticmethod
    def validate_path_advanced(path: str, allowed_temp_dirs: list, is_directory: bool = False) -> tuple[bool, str]:
        """
        Validation avancée d'un chemin avec vérification des liens
        
        Args:
            path: Chemin à valider
            allowed_temp_dirs: Liste des dossiers temporaires autorisés
            is_directory: True si c'est un dossier
            
        Returns:
            tuple: (is_safe, reason)
        """
        # 1. Vérifier si c'est un junction point (dossiers uniquement)
        if is_directory and PathValidator.is_junction_point(path):
            return False, "Junction point detected - Skipped for safety"
        
        # 2. Vérifier si c'est un hard link (fichiers uniquement)
        if not is_directory and os.path.isfile(path):
            if PathValidator.is_hard_link(path):
                return False, "Hard link detected - Skipped for safety"
        
        # 3. Vérifier si c'est un lien symbolique
        if os.path.islink(path):
            is_safe, result = PathValidator.resolve_symlink_safe(path, allowed_temp_dirs)
            if not is_safe:
                return False, f"Unsafe symlink: {result}"
            # Le lien symbolique pointe vers un chemin autorisé
            print(f"[INFO] Symlink validated: {path} -> {result}")
        
        return True, "Path validated"
    
    @staticmethod
    def get_link_info(path: str) -> dict:
        """
        Obtient des informations détaillées sur un chemin (liens, etc.)
        
        Args:
            path: Chemin à analyser
            
        Returns:
            dict: Informations sur le chemin
        """
        info = {
            'path': path,
            'exists': os.path.exists(path),
            'is_symlink': os.path.islink(path),
            'is_junction': False,
            'is_hardlink': False,
            'nlinks': 0,
            'real_path': None
        }
        
        if not info['exists']:
            return info
        
        try:
            # Vérifier junction point
            if os.path.isdir(path):
                info['is_junction'] = PathValidator.is_junction_point(path)
            
            # Vérifier hard link
            if os.path.isfile(path):
                stat_info = os.stat(path)
                info['nlinks'] = stat_info.st_nlink
                info['is_hardlink'] = stat_info.st_nlink > 1
            
            # Résoudre le chemin réel
            if info['is_symlink'] or info['is_junction']:
                info['real_path'] = os.path.realpath(path)
                
        except Exception as e:
            info['error'] = str(e)
        
        return info


# Fonction helper pour intégration facile
def validate_before_delete(path: str, allowed_temp_dirs: list, is_directory: bool = False) -> tuple[bool, str]:
    """
    Fonction helper pour valider un chemin avant suppression
    
    Args:
        path: Chemin à valider
        allowed_temp_dirs: Liste des dossiers temporaires autorisés
        is_directory: True si c'est un dossier
        
    Returns:
        tuple: (is_safe, reason)
    """
    return PathValidator.validate_path_advanced(path, allowed_temp_dirs, is_directory)


if __name__ == "__main__":
    # Test du module
    print("=== Path Validator Test ===\n")
    
    # Test avec un chemin normal
    test_path = r"C:\Windows\Temp\test.txt"
    info = PathValidator.get_link_info(test_path)
    print(f"Path: {test_path}")
    print(f"  Symlink: {info['is_symlink']}")
    print(f"  Junction: {info['is_junction']}")
    print(f"  Hard link: {info['is_hardlink']}")
    print(f"  N-links: {info['nlinks']}")
