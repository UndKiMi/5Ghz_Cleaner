"""
Script pour télécharger automatiquement LibreHardwareMonitor
SÉCURITÉ: Validation SSL et vérification des URLs
"""
import os
import sys
import urllib.request
import ssl
import zipfile
import shutil
from pathlib import Path
from urllib.parse import urlparse

def download_librehardwaremonitor(silent=False):
    """
    Télécharge et installe LibreHardwareMonitor
    SÉCURITÉ: Validation SSL stricte et vérification de l'URL
    """
    
    if not silent:
        print("="*70)
        print("Telechargement de LibreHardwareMonitor")
        print("="*70)
        print()
    
    # URL de la dernière version
    # Note: Cette URL pointe vers la version 0.9.3 (dernière stable)
    download_url = "https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases/download/v0.9.3/LibreHardwareMonitor-net472.zip"
    
    # SÉCURITÉ: Valider l'URL
    try:
        parsed_url = urlparse(download_url)
        if parsed_url.scheme != 'https':
            print("[SECURITY ERROR] Only HTTPS URLs are allowed")
            return False
        if parsed_url.netloc != 'github.com':
            print("[SECURITY ERROR] Only github.com domain is allowed")
            return False
    except Exception as e:
        print(f"[SECURITY ERROR] Invalid URL: {e}")
        return False
    
    # Chemins
    script_dir = Path(__file__).parent
    libs_dir = script_dir / "libs"
    temp_zip = libs_dir / "temp_librehardwaremonitor.zip"
    temp_extract = libs_dir / "temp_extract"
    
    # Créer le dossier libs s'il n'existe pas
    libs_dir.mkdir(exist_ok=True)
    
    try:
        # Télécharger avec validation SSL stricte
        print(f"[1/4] Téléchargement depuis GitHub...")
        print(f"      URL: {download_url}")
        
        # SÉCURITÉ: Créer un contexte SSL strict
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = True
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        
        def show_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(100, (downloaded / total_size) * 100)
            bar_length = 40
            filled = int(bar_length * percent / 100)
            bar = '#' * filled + '-' * (bar_length - filled)
            print(f'\r      [{bar}] {percent:.1f}%', end='', flush=True)
        
        # SÉCURITÉ: Utiliser un opener avec contexte SSL
        opener = urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=ssl_context)
        )
        urllib.request.install_opener(opener)
        
        urllib.request.urlretrieve(download_url, temp_zip, show_progress)
        print()  # Nouvelle ligne après la barre de progression
        print(f"      [OK] Telechargement termine ({temp_zip.stat().st_size / 1024 / 1024:.2f} MB)")
        print()
        
        # Extraire
        print(f"[2/4] Extraction du fichier ZIP...")
        temp_extract.mkdir(exist_ok=True)
        
        with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
            zip_ref.extractall(temp_extract)
        
        print(f"      [OK] Extraction terminee")
        print()
        
        # Trouver et copier toutes les DLL nécessaires
        print(f"[3/4] Recherche des DLL necessaires...")
        
        required_dlls = [
            "LibreHardwareMonitorLib.dll",
            "HidSharp.dll",
        ]
        
        dlls_found = {}
        
        for root, dirs, files in os.walk(temp_extract):
            for file in files:
                if file in required_dlls:
                    source_dll = Path(root) / file
                    target_dll = libs_dir / file
                    
                    # Copier la DLL
                    shutil.copy2(source_dll, target_dll)
                    dlls_found[file] = target_dll
                    print(f"      [OK] {file} copiee")
        
        # Vérifier que LibreHardwareMonitorLib.dll a été trouvée
        if "LibreHardwareMonitorLib.dll" not in dlls_found:
            print(f"      [ERREUR] LibreHardwareMonitorLib.dll non trouvee dans l'archive")
            return False
        
        # HidSharp est optionnel mais recommandé
        if "HidSharp.dll" not in dlls_found:
            print(f"      [WARNING] HidSharp.dll non trouvee (optionnel)")
        
        print(f"      [OK] {len(dlls_found)} DLL(s) copiee(s) vers: {libs_dir}")
        
        print()
        
        # Nettoyage
        print(f"[4/4] Nettoyage des fichiers temporaires...")
        temp_zip.unlink()
        shutil.rmtree(temp_extract)
        print(f"      [OK] Nettoyage termine")
        print()
        
        # Succès
        print("="*70)
        print("[SUCCESS] LibreHardwareMonitor installe avec succes !")
        print("="*70)
        print()
        print("Vous pouvez maintenant relancer l'application:")
        print("  python main.py")
        print()
        print("Vous devriez voir:")
        print("  [SUCCESS] LibreHardwareMonitor initialized successfully")
        print()
        
        return True
        
    except Exception as e:
        print()
        print(f"[ERREUR] Lors du telechargement: {e}")
        print()
        print("Solution alternative:")
        print("1. Allez sur: https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases")
        print("2. Telechargez la derniere version (.zip)")
        print("3. Extrayez et copiez LibreHardwareMonitorLib.dll dans le dossier 'libs/'")
        print()
        
        # Nettoyage en cas d'erreur
        if temp_zip.exists():
            temp_zip.unlink()
        if temp_extract.exists():
            shutil.rmtree(temp_extract)
        
        return False


if __name__ == "__main__":
    success = download_librehardwaremonitor()
    sys.exit(0 if success else 1)
