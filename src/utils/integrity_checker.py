"""
Module de vérification d'intégrité des fichiers critiques
Vérifie les hash SHA256 des DLL et exécutables externes
"""
import hashlib
import os
from pathlib import Path


class IntegrityChecker:
    """Vérificateur d'intégrité des fichiers critiques"""
    
    # Hash SHA256 attendus pour les DLL critiques
    # Mis à jour: 1er novembre 2025
    EXPECTED_HASHES = {
        'LibreHardwareMonitorLib.dll': {
            'sha256': 'a24c7cbb3d6ca12950e570fbad82778a87c87311cde6218914a283a2c0a04e19',
            'version': '0.9.3',
            'critical': True
        },
        'HidSharp.dll': {
            'sha256': None,  # Non critique - vérification optionnelle
            'version': 'latest',
            'critical': False
        },
        'LibreHardwareMonitorLib.sys': {
            'sha256': None,  # Généré dynamiquement - vérification optionnelle
            'version': '0.9.3',
            'critical': False
        }
    }
    
    @staticmethod
    def calculate_sha256(file_path: str) -> str:
        """
        Calcule le hash SHA256 d'un fichier
        
        Args:
            file_path: Chemin du fichier
            
        Returns:
            str: Hash SHA256 en hexadécimal
        """
        sha256_hash = hashlib.sha256()
        
        try:
            with open(file_path, 'rb') as f:
                # Lire par blocs de 4K pour économiser la mémoire
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            
            return sha256_hash.hexdigest()
        except Exception as e:
            print(f"[ERROR] Failed to calculate hash for {file_path}: {e}")
            return None
    
    @staticmethod
    def verify_file_integrity(file_path: str, expected_hash: str = None) -> tuple[bool, str]:
        """
        Vérifie l'intégrité d'un fichier
        
        Args:
            file_path: Chemin du fichier
            expected_hash: Hash SHA256 attendu (optionnel si dans EXPECTED_HASHES)
            
        Returns:
            tuple: (is_valid, message)
        """
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}"
        
        filename = os.path.basename(file_path)
        
        # Calculer le hash actuel
        actual_hash = IntegrityChecker.calculate_sha256(file_path)
        if actual_hash is None:
            return False, "Failed to calculate file hash"
        
        # Vérifier contre le hash attendu
        if expected_hash:
            if actual_hash == expected_hash:
                return True, "File integrity verified"
            else:
                return False, f"Hash mismatch: expected {expected_hash}, got {actual_hash}"
        
        # Vérifier contre la base de données
        if filename in IntegrityChecker.EXPECTED_HASHES:
            file_info = IntegrityChecker.EXPECTED_HASHES[filename]
            expected = file_info['sha256']
            
            # Si le hash n'est pas défini, générer un avertissement mais autoriser
            if expected is None:
                print(f"[WARNING] No expected hash defined for {filename}")
                print(f"[INFO] Current hash: {actual_hash}")
                return True, "No hash defined (first run)"
            
            if actual_hash == expected:
                return True, f"File integrity verified ({file_info['version']})"
            else:
                is_critical = file_info.get('critical', False)
                if is_critical:
                    return False, f"CRITICAL: Hash mismatch for {filename}"
                else:
                    print(f"[WARNING] Hash mismatch for {filename} (non-critical)")
                    return True, "Hash mismatch (non-critical file)"
        
        # Fichier non dans la base de données
        print(f"[INFO] File {filename} not in integrity database")
        print(f"[INFO] Hash: {actual_hash}")
        return True, "File not in database"
    
    @staticmethod
    def verify_libs_directory(libs_dir: str = None) -> dict:
        """
        Vérifie l'intégrité de tous les fichiers du dossier libs/
        
        Args:
            libs_dir: Chemin du dossier libs (auto-détecté si None)
            
        Returns:
            dict: Résultats de vérification par fichier
        """
        if libs_dir is None:
            # Auto-détecter le dossier libs
            root = Path(__file__).parent.parent.parent
            libs_dir = root / "libs"
        
        results = {}
        
        if not os.path.exists(libs_dir):
            return {'error': f"Libs directory not found: {libs_dir}"}
        
        # Vérifier chaque fichier critique
        for filename in IntegrityChecker.EXPECTED_HASHES.keys():
            file_path = os.path.join(libs_dir, filename)
            
            if os.path.exists(file_path):
                is_valid, message = IntegrityChecker.verify_file_integrity(file_path)
                results[filename] = {
                    'valid': is_valid,
                    'message': message,
                    'path': file_path
                }
            else:
                results[filename] = {
                    'valid': False,
                    'message': 'File not found',
                    'path': file_path
                }
        
        return results
    
    @staticmethod
    def generate_hash_for_file(file_path: str):
        """
        Génère et affiche le hash SHA256 d'un fichier
        Utile pour mettre à jour EXPECTED_HASHES
        
        Args:
            file_path: Chemin du fichier
        """
        if not os.path.exists(file_path):
            print(f"[ERROR] File not found: {file_path}")
            return
        
        filename = os.path.basename(file_path)
        file_hash = IntegrityChecker.calculate_sha256(file_path)
        
        if file_hash:
            print(f"\n[INFO] Hash for {filename}:")
            print(f"SHA256: {file_hash}")
            print(f"\nAdd to EXPECTED_HASHES:")
            print(f"'{filename}': {{")
            print(f"    'sha256': '{file_hash}',")
            print(f"    'version': 'x.x.x',")
            print(f"    'critical': True")
            print(f"}},\n")


# Exception personnalisée pour les erreurs d'intégrité
class IntegrityError(Exception):
    """Exception levée quand l'intégrité d'un fichier est compromise"""
    pass


# Fonction helper pour vérifier rapidement
def verify_dll_integrity(dll_path: str) -> bool:
    """
    Fonction helper pour vérifier rapidement l'intégrité d'une DLL
    
    Args:
        dll_path: Chemin de la DLL
        
    Returns:
        bool: True si intègre, False sinon
        
    Raises:
        IntegrityError: Si la DLL est critique et corrompue
    """
    is_valid, message = IntegrityChecker.verify_file_integrity(dll_path)
    
    if not is_valid:
        filename = os.path.basename(dll_path)
        if filename in IntegrityChecker.EXPECTED_HASHES:
            if IntegrityChecker.EXPECTED_HASHES[filename].get('critical', False):
                raise IntegrityError(f"Critical DLL integrity check failed: {message}")
        
        print(f"[WARNING] DLL integrity check failed: {message}")
        return False
    
    return True


if __name__ == "__main__":
    # Test du module
    print("=== Integrity Checker Test ===\n")
    
    # Vérifier le dossier libs
    results = IntegrityChecker.verify_libs_directory()
    
    for filename, result in results.items():
        status = "✓" if result['valid'] else "✗"
        print(f"{status} {filename}: {result['message']}")
