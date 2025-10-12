"""
Générateur de checksum SHA256 pour vérification d'intégrité
Génère automatiquement les checksums des fichiers de distribution
"""
import hashlib
import os
import json
from datetime import datetime
from pathlib import Path


def calculate_sha256(filepath):
    """Calcule le SHA256 d'un fichier"""
    sha256_hash = hashlib.sha256()
    
    try:
        with open(filepath, "rb") as f:
            # Lire par blocs pour les gros fichiers
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"[ERROR] Cannot calculate SHA256 for {filepath}: {e}")
        return None


def calculate_md5(filepath):
    """Calcule le MD5 d'un fichier (pour compatibilité)"""
    md5_hash = hashlib.md5()
    
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
        return md5_hash.hexdigest()
    except Exception as e:
        print(f"[ERROR] Cannot calculate MD5 for {filepath}: {e}")
        return None


def get_file_info(filepath):
    """Récupère les informations d'un fichier"""
    try:
        stat = os.stat(filepath)
        return {
            "size_bytes": stat.st_size,
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        }
    except Exception as e:
        print(f"[ERROR] Cannot get file info for {filepath}: {e}")
        return None


def generate_checksums_for_dist():
    """Génère les checksums pour tous les fichiers de distribution"""
    print("="*80)
    print("GÉNÉRATEUR DE CHECKSUM SHA256")
    print("="*80)
    print()
    
    dist_dir = Path(__file__).parent / "dist"
    
    if not dist_dir.exists():
        print("[ERROR] Distribution directory not found: dist/")
        print("[INFO] Please build the application first using: build.bat")
        return None
    
    checksums = {
        "generated_at": datetime.now().isoformat(),
        "generator_version": "1.0.0",
        "files": []
    }
    
    # Trouver tous les fichiers .exe dans dist/
    exe_files = list(dist_dir.glob("*.exe"))
    
    if not exe_files:
        print("[WARNING] No .exe files found in dist/")
        print("[INFO] Looking for other distribution files...")
        # Chercher d'autres fichiers
        exe_files = list(dist_dir.glob("*"))
        exe_files = [f for f in exe_files if f.is_file()]
    
    if not exe_files:
        print("[ERROR] No distribution files found")
        return None
    
    print(f"[INFO] Found {len(exe_files)} file(s) to process")
    print()
    
    for exe_file in exe_files:
        print(f"[INFO] Processing: {exe_file.name}")
        
        # Calculer SHA256
        print("      Calculating SHA256...", end=" ")
        sha256 = calculate_sha256(exe_file)
        if sha256:
            print(f"✓")
        else:
            print(f"✗")
            continue
        
        # Calculer MD5 (optionnel)
        print("      Calculating MD5...", end=" ")
        md5 = calculate_md5(exe_file)
        if md5:
            print(f"✓")
        else:
            print(f"✗")
        
        # Récupérer infos fichier
        file_info = get_file_info(exe_file)
        
        file_data = {
            "filename": exe_file.name,
            "sha256": sha256,
            "md5": md5,
            "size_bytes": file_info["size_bytes"] if file_info else 0,
            "size_mb": file_info["size_mb"] if file_info else 0,
            "modified": file_info["modified"] if file_info else None,
        }
        
        checksums["files"].append(file_data)
        print()
    
    # Sauvegarder en JSON
    checksum_file = dist_dir / "CHECKSUMS.json"
    try:
        with open(checksum_file, 'w', encoding='utf-8') as f:
            json.dump(checksums, f, indent=2, ensure_ascii=False)
        print(f"[SUCCESS] Checksums saved to: {checksum_file}")
    except Exception as e:
        print(f"[ERROR] Cannot save checksums: {e}")
        return None
    
    # Générer aussi un fichier texte lisible
    checksum_txt = dist_dir / "CHECKSUMS.txt"
    try:
        with open(checksum_txt, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("5GH'z CLEANER - CHECKSUMS DE VÉRIFICATION D'INTÉGRITÉ\n")
            f.write("="*80 + "\n\n")
            f.write(f"Généré le: {checksums['generated_at']}\n\n")
            
            for file_data in checksums["files"]:
                f.write(f"Fichier: {file_data['filename']}\n")
                f.write(f"Taille:  {file_data['size_mb']} MB ({file_data['size_bytes']:,} bytes)\n")
                f.write(f"SHA256:  {file_data['sha256']}\n")
                f.write(f"MD5:     {file_data['md5']}\n")
                f.write(f"Modifié: {file_data['modified']}\n")
                f.write("\n" + "-"*80 + "\n\n")
            
            f.write("="*80 + "\n")
            f.write("INSTRUCTIONS DE VÉRIFICATION\n")
            f.write("="*80 + "\n\n")
            f.write("Pour vérifier l'intégrité du fichier téléchargé:\n\n")
            f.write("1. Windows PowerShell:\n")
            f.write("   Get-FileHash -Algorithm SHA256 <fichier.exe>\n\n")
            f.write("2. Linux/Mac:\n")
            f.write("   shasum -a 256 <fichier.exe>\n\n")
            f.write("3. Comparez le hash obtenu avec celui ci-dessus\n")
            f.write("   ✓ Si identique: fichier authentique et non modifié\n")
            f.write("   ✗ Si différent: fichier corrompu ou compromis\n\n")
            f.write("="*80 + "\n")
        
        print(f"[SUCCESS] Readable checksums saved to: {checksum_txt}")
    except Exception as e:
        print(f"[ERROR] Cannot save readable checksums: {e}")
    
    print()
    print("="*80)
    print("RÉSUMÉ")
    print("="*80)
    
    for file_data in checksums["files"]:
        print(f"\n{file_data['filename']}:")
        print(f"  SHA256: {file_data['sha256']}")
        print(f"  Taille: {file_data['size_mb']} MB")
    
    print()
    print("="*80)
    print()
    
    return checksums


def verify_file_integrity(filepath, expected_sha256):
    """Vérifie l'intégrité d'un fichier"""
    print(f"[INFO] Verifying integrity of: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return False
    
    print("[INFO] Calculating SHA256...", end=" ")
    actual_sha256 = calculate_sha256(filepath)
    
    if not actual_sha256:
        print("✗")
        return False
    
    print("✓")
    print(f"[INFO] Expected: {expected_sha256}")
    print(f"[INFO] Actual:   {actual_sha256}")
    
    if actual_sha256.lower() == expected_sha256.lower():
        print("[SUCCESS] ✓ File integrity verified - Authentic file")
        return True
    else:
        print("[ERROR] ✗ File integrity check FAILED - File may be corrupted or compromised")
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Mode vérification
        if sys.argv[1] == "verify" and len(sys.argv) == 4:
            filepath = sys.argv[2]
            expected_hash = sys.argv[3]
            result = verify_file_integrity(filepath, expected_hash)
            sys.exit(0 if result else 1)
    else:
        # Mode génération
        result = generate_checksums_for_dist()
        sys.exit(0 if result else 1)
