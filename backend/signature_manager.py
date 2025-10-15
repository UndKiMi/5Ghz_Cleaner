"""
Module de Gestion des Signatures Numériques
Système de signature et vérification pour garantir l'intégrité de l'application
"""
import os
import hashlib
import json
from datetime import datetime
from pathlib import Path

class SignatureManager:
    """Gestionnaire de signatures numériques pour l'application"""
    
    def __init__(self):
        self.app_root = Path(__file__).parent.parent
        self.signature_file = self.app_root / "docs" / "reports" / "SIGNATURE.json"
        self.checksums_file = self.app_root / "docs" / "reports" / "CHECKSUMS.txt"
        
        # Clé publique de vérification (simulée - en production, utiliser une vraie clé RSA)
        self.public_key_hash = "5GHZ_CLEANER_UNDKIMI_2025_OFFICIAL"
        
    def calculate_file_hash(self, filepath: str, algorithm: str = "sha256") -> str:
        """
        Calcule le hash d'un fichier
        
        Args:
            filepath: Chemin du fichier
            algorithm: Algorithme de hash (sha256, sha512)
            
        Returns:
            str: Hash hexadécimal du fichier
        """
        hash_obj = hashlib.new(algorithm)
        
        try:
            with open(filepath, 'rb') as f:
                while chunk := f.read(8192):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except Exception as e:
            print(f"[ERROR] Failed to hash {filepath}: {e}")
            return ""
    
    def generate_application_signature(self) -> dict:
        """
        Génère une signature complète de l'application
        
        Returns:
            dict: Signature avec tous les hashes des fichiers critiques
        """
        print("[INFO] Génération de la signature de l'application...")
        
        signature = {
            "version": "1.6.0",
            "author": "UndKiMi",
            "generated_at": datetime.now().isoformat(),
            "public_key_hash": self.public_key_hash,
            "files": {},
            "integrity": {}
        }
        
        # Fichiers critiques à signer
        critical_files = [
            "main.py",
            "backend/cleaner.py",
            "backend/security_core.py",
            "backend/security.py",
            "backend/elevation.py",
            "backend/dry_run.py",
            "backend/logger.py",
            "backend/telemetry_checker.py",
            "backend/hardware_monitor.py",
            "backend/system_commands.py",
            "backend/signature_manager.py",
            "frontend/app.py",
            "frontend/pages/main_page.py",
            "frontend/pages/preview_page.py",
            "config/settings.py",
            "config/constants.py",
            "requirements.txt",
        ]
        
        # Calculer les hashes
        for file_path in critical_files:
            full_path = self.app_root / file_path
            if full_path.exists():
                sha256_hash = self.calculate_file_hash(str(full_path), "sha256")
                sha512_hash = self.calculate_file_hash(str(full_path), "sha512")
                
                signature["files"][file_path] = {
                    "sha256": sha256_hash,
                    "sha512": sha512_hash,
                    "size": full_path.stat().st_size,
                    "modified": datetime.fromtimestamp(full_path.stat().st_mtime).isoformat()
                }
                
                print(f"  [OK] {file_path}: {sha256_hash[:16]}...")
        
        # Calculer le hash d'intégrité global
        all_hashes = "".join([
            f"{path}{data['sha256']}{data['sha512']}"
            for path, data in sorted(signature["files"].items())
        ])
        
        signature["integrity"]["global_sha256"] = hashlib.sha256(all_hashes.encode()).hexdigest()
        signature["integrity"]["global_sha512"] = hashlib.sha512(all_hashes.encode()).hexdigest()
        signature["integrity"]["file_count"] = len(signature["files"])
        
        print(f"\n[INFO] Signature globale: {signature['integrity']['global_sha256'][:32]}...")
        print(f"[INFO] {len(signature['files'])} fichiers signés")
        
        return signature
    
    def save_signature(self, signature: dict) -> bool:
        """
        Sauvegarde la signature dans un fichier JSON
        
        Args:
            signature: Dictionnaire de signature
            
        Returns:
            bool: True si succès
        """
        try:
            with open(self.signature_file, 'w', encoding='utf-8') as f:
                json.dump(signature, f, indent=2, ensure_ascii=False)
            
            print(f"\n[SUCCESS] Signature sauvegardée: {self.signature_file}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to save signature: {e}")
            return False
    
    def load_signature(self) -> dict:
        """
        Charge la signature depuis le fichier
        
        Returns:
            dict: Signature ou None si erreur
        """
        try:
            if not self.signature_file.exists():
                print(f"[WARNING] Fichier de signature introuvable: {self.signature_file}")
                return None
            
            with open(self.signature_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load signature: {e}")
            return None
    
    def verify_signature(self, signature: dict = None) -> tuple[bool, list]:
        """
        Vérifie l'intégrité de l'application avec la signature
        
        Args:
            signature: Signature à vérifier (ou charge depuis le fichier)
            
        Returns:
            tuple: (is_valid, errors_list)
        """
        if signature is None:
            signature = self.load_signature()
            if signature is None:
                return False, ["Signature file not found"]
        
        print("\n" + "="*80)
        print("VÉRIFICATION DE LA SIGNATURE NUMÉRIQUE")
        print("="*80)
        
        errors = []
        
        # Vérifier la clé publique
        if signature.get("public_key_hash") != self.public_key_hash:
            errors.append("Invalid public key hash")
            print("[FAIL] Cle publique invalide!")
        else:
            print("[OK] Cle publique valide")
        
        # Vérifier chaque fichier
        print("\nVérification des fichiers:")
        for file_path, file_data in signature.get("files", {}).items():
            full_path = self.app_root / file_path
            
            if not full_path.exists():
                errors.append(f"File missing: {file_path}")
                print(f"  [FAIL] {file_path}: FICHIER MANQUANT")
                continue
            
            # Vérifier SHA256
            current_sha256 = self.calculate_file_hash(str(full_path), "sha256")
            if current_sha256 != file_data.get("sha256"):
                errors.append(f"SHA256 mismatch: {file_path}")
                print(f"  [FAIL] {file_path}: HASH SHA256 INVALIDE")
                continue
            
            # Vérifier SHA512
            current_sha512 = self.calculate_file_hash(str(full_path), "sha512")
            if current_sha512 != file_data.get("sha512"):
                errors.append(f"SHA512 mismatch: {file_path}")
                print(f"  [FAIL] {file_path}: HASH SHA512 INVALIDE")
                continue
            
            print(f"  [OK] {file_path}: OK")
        
        # Vérifier l'intégrité globale
        print("\nVérification de l'intégrité globale:")
        all_hashes = "".join([
            f"{path}{data['sha256']}{data['sha512']}"
            for path, data in sorted(signature.get("files", {}).items())
        ])
        
        current_global_sha256 = hashlib.sha256(all_hashes.encode()).hexdigest()
        if current_global_sha256 != signature.get("integrity", {}).get("global_sha256"):
            errors.append("Global integrity check failed")
            print("  [FAIL] Integrite globale INVALIDE")
        else:
            print("  [OK] Integrite globale valide")
        
        # Résultat final
        print("\n" + "="*80)
        if not errors:
            print("SIGNATURE VALIDE - Application authentique et non modifiee")
            print("="*80)
            return True, []
        else:
            print("SIGNATURE INVALIDE - Application potentiellement compromise!")
            print(f"   {len(errors)} erreur(s) detectee(s)")
            for error in errors:
                print(f"   - {error}")
            print("="*80)
            return False, errors
    
    def generate_checksums_file(self, signature: dict = None):
        """
        Génère un fichier CHECKSUMS.txt lisible
        
        Args:
            signature: Signature à utiliser
        """
        if signature is None:
            signature = self.load_signature()
            if signature is None:
                print("[ERROR] No signature to generate checksums from")
                return
        
        try:
            with open(self.checksums_file, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write("5GHz Cleaner - Checksums de Vérification\n")
                f.write(f"Version: {signature.get('version', 'Unknown')}\n")
                f.write(f"Auteur: {signature.get('author', 'Unknown')}\n")
                f.write(f"Généré le: {signature.get('generated_at', 'Unknown')}\n")
                f.write("="*80 + "\n\n")
                
                f.write("INTÉGRITÉ GLOBALE:\n")
                f.write(f"SHA256: {signature.get('integrity', {}).get('global_sha256', 'N/A')}\n")
                f.write(f"SHA512: {signature.get('integrity', {}).get('global_sha512', 'N/A')}\n")
                f.write(f"Fichiers: {signature.get('integrity', {}).get('file_count', 0)}\n\n")
                
                f.write("="*80 + "\n")
                f.write("CHECKSUMS DES FICHIERS:\n")
                f.write("="*80 + "\n\n")
                
                for file_path, file_data in sorted(signature.get("files", {}).items()):
                    f.write(f"Fichier: {file_path}\n")
                    f.write(f"  SHA256: {file_data.get('sha256', 'N/A')}\n")
                    f.write(f"  SHA512: {file_data.get('sha512', 'N/A')}\n")
                    f.write(f"  Taille: {file_data.get('size', 0)} bytes\n")
                    f.write(f"  Modifié: {file_data.get('modified', 'N/A')}\n\n")
                
                f.write("="*80 + "\n")
                f.write("VÉRIFICATION:\n")
                f.write("="*80 + "\n")
                f.write("PowerShell:\n")
                f.write("  Get-FileHash -Algorithm SHA256 <fichier>\n\n")
                f.write("Python:\n")
                f.write("  py backend/signature_manager.py --verify\n\n")
            
            print(f"[SUCCESS] Checksums sauvegardés: {self.checksums_file}")
        except Exception as e:
            print(f"[ERROR] Failed to generate checksums file: {e}")


# Instance globale
signature_manager = SignatureManager()


def generate_signature():
    """Génère et sauvegarde la signature de l'application"""
    print("\n" + "="*80)
    print("GÉNÉRATION DE LA SIGNATURE NUMÉRIQUE")
    print("="*80 + "\n")
    
    signature = signature_manager.generate_application_signature()
    signature_manager.save_signature(signature)
    signature_manager.generate_checksums_file(signature)
    
    print("\n" + "="*80)
    print("SIGNATURE GENEREE AVEC SUCCES")
    print("="*80)


def verify_signature():
    """Vérifie la signature de l'application"""
    is_valid, errors = signature_manager.verify_signature()
    return is_valid


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        # Mode vérification
        is_valid = verify_signature()
        sys.exit(0 if is_valid else 1)
    else:
        # Mode génération
        generate_signature()
