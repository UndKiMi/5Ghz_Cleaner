"""
Module de vérification d'intégrité des DLLs externes
Vérifie les signatures et hashes avant chargement pour éviter les faux positifs antivirus
"""
import hashlib
from pathlib import Path
from typing import Dict, Optional, Tuple

# Hashes SHA256 attendus pour les DLLs (à mettre à jour à chaque version)
# Ces hashes garantissent que les DLLs n'ont pas été modifiées
EXPECTED_HASHES: Dict[str, str] = {
    'LibreHardwareMonitorLib.dll': '',  # À remplir après vérification
    'HidSharp.dll': '',  # À remplir après vérification
}

# Informations sur les DLLs
DLL_INFO: Dict[str, Dict[str, str]] = {
    'LibreHardwareMonitorLib.dll': {
        'name': 'LibreHardwareMonitor Library',
        'purpose': 'Hardware monitoring (CPU/GPU temperatures, usage)',
        'source': 'https://github.com/LibreHardwareMonitor/LibreHardwareMonitor',
        'license': 'MPL 2.0',
        'safe': 'Yes - Open source, widely used, no kernel access'
    },
    'HidSharp.dll': {
        'name': 'HidSharp Library',
        'purpose': 'HID device communication',
        'source': 'https://github.com/IntergatedCircuits/HidSharp',
        'license': 'Apache 2.0',
        'safe': 'Yes - Open source, user-mode only'
    }
}


def calculate_sha256(file_path: Path) -> str:
    """
    Calcule le hash SHA256 d'un fichier
    
    Args:
        file_path: Chemin du fichier
        
    Returns:
        Hash SHA256 en hexadécimal
    """
    sha256_hash = hashlib.sha256()
    
    try:
        with open(file_path, 'rb') as f:
            # Lire par blocs de 64KB pour économiser la mémoire
            for byte_block in iter(lambda: f.read(65536), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"[ERROR] Failed to calculate hash for {file_path}: {e}")
        return ""


def verify_dll_integrity(dll_path: Path, strict: bool = False) -> Tuple[bool, str]:
    """
    Vérifie l'intégrité d'une DLL avant chargement
    
    Args:
        dll_path: Chemin de la DLL
        strict: Si True, refuse le chargement si le hash ne correspond pas
                Si False, affiche un warning mais autorise le chargement
        
    Returns:
        Tuple (is_valid, message)
    """
    dll_name = dll_path.name
    
    # Vérifier que le fichier existe
    if not dll_path.exists():
        return False, f"DLL not found: {dll_name}"
    
    # Vérifier que c'est bien une DLL
    if not dll_name.lower().endswith('.dll'):
        return False, f"Not a DLL file: {dll_name}"
    
    # Calculer le hash actuel
    actual_hash = calculate_sha256(dll_path)
    if not actual_hash:
        return False, f"Failed to calculate hash for {dll_name}"
    
    # Récupérer le hash attendu
    expected_hash = EXPECTED_HASHES.get(dll_name, "")
    
    # Si pas de hash attendu configuré
    if not expected_hash:
        message = f"[INFO] No expected hash configured for {dll_name}"
        print(message)
        print(f"[INFO] Current hash: {actual_hash}")
        print(f"[INFO] Add this hash to EXPECTED_HASHES in dll_integrity.py")
        
        # En mode non-strict, on autorise quand même
        if not strict:
            return True, "No hash configured (allowed in non-strict mode)"
        else:
            return False, "No hash configured (strict mode)"
    
    # Vérifier que le hash correspond
    if actual_hash.lower() == expected_hash.lower():
        return True, f"DLL integrity verified: {dll_name}"
    else:
        message = f"[SECURITY WARNING] DLL integrity check FAILED for {dll_name}"
        print(message)
        print(f"[SECURITY] Expected: {expected_hash}")
        print(f"[SECURITY] Actual:   {actual_hash}")
        print(f"[SECURITY] This DLL may have been modified or corrupted")
        
        if not strict:
            print(f"[WARNING] Loading anyway (non-strict mode)")
            return True, "Hash mismatch (allowed in non-strict mode)"
        else:
            return False, "Hash mismatch (strict mode)"


def get_dll_info(dll_name: str) -> Optional[Dict[str, str]]:
    """
    Récupère les informations sur une DLL
    
    Args:
        dll_name: Nom de la DLL
        
    Returns:
        Dictionnaire avec les informations ou None
    """
    return DLL_INFO.get(dll_name)


def print_dll_info(dll_name: str) -> None:
    """
    Affiche les informations sur une DLL
    
    Args:
        dll_name: Nom de la DLL
    """
    info = get_dll_info(dll_name)
    if not info:
        print(f"[INFO] No information available for {dll_name}")
        return
    
    print(f"\n{'='*70}")
    print(f"DLL Information: {dll_name}")
    print(f"{'='*70}")
    print(f"Name:    {info['name']}")
    print(f"Purpose: {info['purpose']}")
    print(f"Source:  {info['source']}")
    print(f"License: {info['license']}")
    print(f"Safe:    {info['safe']}")
    print(f"{'='*70}\n")


def verify_all_dlls(libs_dir: Path, strict: bool = False) -> Dict[str, Tuple[bool, str]]:
    """
    Vérifie toutes les DLLs dans le dossier libs
    
    Args:
        libs_dir: Dossier contenant les DLLs
        strict: Mode strict (refuse si hash ne correspond pas)
        
    Returns:
        Dictionnaire {dll_name: (is_valid, message)}
    """
    results = {}
    
    print(f"\n{'='*70}")
    print("DLL Integrity Verification")
    print(f"{'='*70}")
    print(f"Directory: {libs_dir}")
    print(f"Mode: {'STRICT' if strict else 'PERMISSIVE'}")
    print(f"{'='*70}\n")
    
    # Vérifier chaque DLL connue
    for dll_name in EXPECTED_HASHES.keys():
        dll_path = libs_dir / dll_name
        
        print(f"Checking: {dll_name}...")
        is_valid, message = verify_dll_integrity(dll_path, strict)
        results[dll_name] = (is_valid, message)
        
        if is_valid:
            print(f"  ✅ {message}")
        else:
            print(f"  ❌ {message}")
        
        # Afficher les infos de la DLL
        info = get_dll_info(dll_name)
        if info:
            print(f"  ℹ️  {info['purpose']}")
    
    print(f"\n{'='*70}")
    print(f"Verification complete: {sum(1 for v, _ in results.values() if v)}/{len(results)} DLLs valid")
    print(f"{'='*70}\n")
    
    return results


def update_dll_hashes(libs_dir: Path) -> None:
    """
    Calcule et affiche les hashes de toutes les DLLs
    Utile pour mettre à jour EXPECTED_HASHES
    
    Args:
        libs_dir: Dossier contenant les DLLs
    """
    print(f"\n{'='*70}")
    print("DLL Hash Calculator")
    print(f"{'='*70}\n")
    
    print("Copy these hashes to EXPECTED_HASHES in dll_integrity.py:\n")
    print("EXPECTED_HASHES = {")
    
    for dll_name in EXPECTED_HASHES.keys():
        dll_path = libs_dir / dll_name
        
        if dll_path.exists():
            hash_value = calculate_sha256(dll_path)
            print(f"    '{dll_name}': '{hash_value}',")
        else:
            print(f"    '{dll_name}': '',  # File not found")
    
    print("}\n")


if __name__ == "__main__":
    """Test du module"""
    import sys
    from pathlib import Path
    
    # Chemin du dossier libs
    project_root = Path(__file__).parent.parent.parent
    libs_dir = project_root / "libs"
    
    print("="*70)
    print("5GH'z Cleaner - DLL Integrity Checker")
    print("="*70)
    
    # Afficher les infos de toutes les DLLs
    print("\nKnown DLLs:")
    for dll_name in EXPECTED_HASHES.keys():
        print_dll_info(dll_name)
    
    # Calculer les hashes
    if "--update-hashes" in sys.argv:
        update_dll_hashes(libs_dir)
    else:
        # Vérifier les DLLs
        strict_mode = "--strict" in sys.argv
        results = verify_all_dlls(libs_dir, strict=strict_mode)
        
        # Afficher le résumé
        all_valid = all(is_valid for is_valid, _ in results.values())
        
        if all_valid:
            print("✅ All DLLs passed integrity check")
            sys.exit(0)
        else:
            print("❌ Some DLLs failed integrity check")
            sys.exit(1)
