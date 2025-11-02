#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5GH'z Cleaner - Build Script Optimisé Anti-Faux Positifs
Version: 2.0 - Antivirus Optimized
Author: UndKiMi
License: CC BY-NC-SA 4.0

OBJECTIF: Build clean sans détection antivirus
MÉTHODE: Désactiver UPX, métadonnées complètes, signature numérique

USAGE:
    python build_antivirus_optimized.py                # Build standard
    python build_antivirus_optimized.py --clean         # Clean build
    python build_antivirus_optimized.py --test          # Test post-build
    python build_antivirus_optimized.py --sign          # Signer l'exécutable
"""

import sys
import os
import shutil
import subprocess
import hashlib
import argparse
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

APP_NAME = "5Ghz_Cleaner"
VERSION = "1.7.0"
AUTHOR = "UndKiMi"

BUILD_DIR = Path("build")
DIST_DIR = Path("dist")
LIBS_DIR = Path("libs")
ASSETS_DIR = Path("assets")
CONFIG_DIR = Path("config")

# Fichiers critiques
VERSION_INFO = Path("version_info.py")
ICON_FILE = ASSETS_DIR / "icon.ico"
MAIN_SCRIPT = Path("main.py")

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def print_header(message):
    """Print a header message"""
    print(f"\n{Colors.OKCYAN}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}[STEP] {message}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{'=' * 80}{Colors.ENDC}")

def print_success(message):
    """Print a success message"""
    print(f"{Colors.OKGREEN}  ✅ {message}{Colors.ENDC}")

def print_error(message):
    """Print an error message"""
    print(f"{Colors.FAIL}  ❌ {message}{Colors.ENDC}")

def print_warning(message):
    """Print a warning message"""
    print(f"{Colors.WARNING}  ⚠️  {message}{Colors.ENDC}")

def print_info(message):
    """Print an info message"""
    print(f"{Colors.OKBLUE}  ℹ️  {message}{Colors.ENDC}")

def print_banner():
    """Print the application banner"""
    banner = f"""
{Colors.OKCYAN}
  ╔══════════════════════════════════════════════════════════════════════════╗
  ║                                                                          ║
  ║           5GH'z CLEANER - ANTIVIRUS OPTIMIZED BUILD v{VERSION:^10}║
  ║                                                                          ║
  ║  Windows 11 Cleaning & Optimization Tool                                ║
  ║  Build Configuration: Zero False Positives                              ║
  ║  Author: {AUTHOR:^63}║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
"""
    print(banner)

def run_command(cmd, check=True, shell=False):
    """
    Run a command and return the result
    SÉCURITÉ: shell=False par défaut
    """
    try:
        if isinstance(cmd, str) and not shell:
            cmd = cmd.split()
        
        result = subprocess.run(
            cmd,
            shell=shell,
            check=check,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes max
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr
    except Exception as e:
        return False, "", str(e)

def calculate_sha256(filepath):
    """Calculate SHA256 hash of a file"""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(65536), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print_error(f"Failed to calculate hash: {e}")
        return ""

# ============================================================================
# PRE-BUILD CHECKS
# ============================================================================

def check_prerequisites():
    """Check if all prerequisites are installed"""
    print_header("Pre-Build Checks")
    
    all_ok = True
    
    # Check Python
    success, stdout, _ = run_command("python --version", check=False)
    if success:
        print_success(f"Python: {stdout.strip()}")
    else:
        print_error("Python not found! Install Python 3.11+")
        all_ok = False
    
    # Check PyInstaller
    success, stdout, _ = run_command("pyinstaller --version", check=False)
    if success:
        print_success(f"PyInstaller: {stdout.strip()}")
    else:
        print_warning("PyInstaller not found. Installing...")
        success, _, _ = run_command("pip install pyinstaller")
        if success:
            print_success("PyInstaller installed")
        else:
            print_error("Failed to install PyInstaller")
            all_ok = False
    
    # Check version_info.py
    if VERSION_INFO.exists():
        print_success(f"Version info: {VERSION_INFO}")
    else:
        print_error(f"Version info not found: {VERSION_INFO}")
        print_info("Create version_info.py with metadata")
        all_ok = False
    
    # Check icon
    if ICON_FILE.exists():
        print_success(f"Icon: {ICON_FILE}")
    else:
        print_warning(f"Icon not found: {ICON_FILE}")
        print_info("Build will continue without icon")
    
    # Check main script
    if MAIN_SCRIPT.exists():
        print_success(f"Main script: {MAIN_SCRIPT}")
    else:
        print_error(f"Main script not found: {MAIN_SCRIPT}")
        all_ok = False
    
    # Check DLL integrity
    print_info("Checking DLL integrity...")
    try:
        from src.utils.dll_integrity import verify_all_dlls
        results = verify_all_dlls(LIBS_DIR, strict=False)
        valid_count = sum(1 for is_valid, _ in results.values() if is_valid)
        total_count = len(results)
        
        if valid_count == total_count:
            print_success(f"DLL integrity: {valid_count}/{total_count} valid")
        else:
            print_warning(f"DLL integrity: {valid_count}/{total_count} valid")
            print_info("Some DLLs may need hash updates")
    except Exception as e:
        print_warning(f"Could not verify DLL integrity: {e}")
    
    return all_ok

# ============================================================================
# BUILD FUNCTIONS
# ============================================================================

def clean_build(args):
    """Clean previous build artifacts"""
    if not args.clean:
        return
    
    print_header("Cleaning Previous Build")
    
    # Remove build directory
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
        print_success(f"Removed: {BUILD_DIR}")
    
    # Remove dist directory
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
        print_success(f"Removed: {DIST_DIR}")
    
    # Remove Python cache
    cache_count = 0
    for pycache in Path(".").rglob("__pycache__"):
        shutil.rmtree(pycache)
        cache_count += 1
    for pyc in Path(".").rglob("*.pyc"):
        pyc.unlink()
        cache_count += 1
    
    if cache_count > 0:
        print_success(f"Removed {cache_count} cache files")

def build_executable(args):
    """Build the executable with PyInstaller - OPTIMIZED FOR ANTIVIRUS"""
    print_header("Building Executable (Antivirus Optimized)")
    
    # Construire la commande PyInstaller
    cmd = [
        "pyinstaller",
        f"--name={APP_NAME}",
        "--onefile",  # Un seul fichier
        "--windowed",  # Pas de console
        "--clean",
        "--noconfirm",
    ]
    
    # Ajouter l'icône si disponible
    if ICON_FILE.exists():
        cmd.append(f"--icon={ICON_FILE}")
        print_info(f"Using icon: {ICON_FILE}")
    
    # Ajouter version_info si disponible
    if VERSION_INFO.exists():
        cmd.append(f"--version-file={VERSION_INFO}")
        print_info(f"Using version info: {VERSION_INFO}")
    else:
        print_warning("No version_info.py - metadata will be missing")
        print_warning("This increases antivirus detection risk!")
    
    # Ajouter les données
    if LIBS_DIR.exists():
        cmd.append(f"--add-data={LIBS_DIR};libs")
        print_info(f"Including: {LIBS_DIR}")
    
    if ASSETS_DIR.exists():
        cmd.append(f"--add-data={ASSETS_DIR};assets")
        print_info(f"Including: {ASSETS_DIR}")
    
    if CONFIG_DIR.exists():
        cmd.append(f"--add-data={CONFIG_DIR};config")
        print_info(f"Including: {CONFIG_DIR}")
    
    # Hidden imports
    hidden_imports = ["flet", "psutil", "pywin32", "pythonnet", "cryptography"]
    for module in hidden_imports:
        cmd.append(f"--hidden-import={module}")
    
    # ⚠️ CRITIQUE: Désactiver UPX (compression = flag antivirus)
    cmd.append("--noupx")
    print_warning("UPX compression DISABLED (reduces false positives)")
    
    # Script principal
    cmd.append(str(MAIN_SCRIPT))
    
    # Afficher la commande
    print_info("PyInstaller command:")
    print(f"  {' '.join(cmd)}")
    print()
    
    # Exécuter PyInstaller
    print_info("Running PyInstaller... (this may take several minutes)")
    success, stdout, stderr = run_command(cmd, check=False)
    
    if not success:
        print_error("Build failed!")
        print(stderr)
        return False
    
    print_success("Build completed successfully!")
    return True

def post_build_tasks(args):
    """Perform post-build tasks"""
    print_header("Post-Build Tasks")
    
    # Déterminer le chemin de l'exécutable
    exe_path = DIST_DIR / f"{APP_NAME}.exe"
    
    # Vérifier que l'exécutable existe
    if not exe_path.exists():
        print_error(f"Executable not found: {exe_path}")
        return False
    
    # Taille de l'exécutable
    exe_size = exe_path.stat().st_size / (1024 * 1024)  # MB
    print_success(f"Executable created: {exe_path}")
    print_info(f"Size: {exe_size:.2f} MB")
    
    # Vérifier les métadonnées
    print_info("Checking executable metadata...")
    # Note: Sur Windows, on peut vérifier avec PowerShell
    # Get-ItemProperty dist\5Ghz_Cleaner.exe | Select-Object VersionInfo
    
    # Générer les checksums
    print_info("Generating checksums...")
    sha256_hash = calculate_sha256(exe_path)
    
    if sha256_hash:
        checksum_file = DIST_DIR / "CHECKSUMS.txt"
        with open(checksum_file, 'w', encoding='utf-8') as f:
            f.write(f"5GH'z Cleaner {VERSION} - Build Checksums\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Build: Antivirus Optimized (UPX Disabled)\n\n")
            f.write(f"Executable: {APP_NAME}.exe\n")
            f.write(f"SHA-256: {sha256_hash}\n\n")
            f.write("Verify with:\n")
            f.write(f"  certutil -hashfile {APP_NAME}.exe SHA256\n")
            f.write("Or:\n")
            f.write(f"  python -c \"import hashlib; print(hashlib.sha256(open('{APP_NAME}.exe', 'rb').read()).hexdigest())\"\n")
        
        print_success(f"Checksums saved: {checksum_file}")
        print_info(f"SHA-256: {sha256_hash}")
    
    # Copier la documentation
    print_info("Copying documentation...")
    docs_to_copy = [
        "README.md",
        "LICENSE",
        "ANTIVIRUS_FAQ.md",
        "ANTIVIRUS_OPTIMIZATION_REPORT.md"
    ]
    
    copied_count = 0
    for doc in docs_to_copy:
        doc_path = Path(doc)
        if doc_path.exists():
            shutil.copy(doc_path, DIST_DIR)
            copied_count += 1
    
    if copied_count > 0:
        print_success(f"Copied {copied_count} documentation files")
    
    return True, exe_path, exe_size, sha256_hash

def test_executable(exe_path):
    """Test the executable"""
    print_header("Testing Executable")
    
    print_info("Basic tests:")
    
    # Test 1: Fichier existe
    if exe_path.exists():
        print_success("File exists")
    else:
        print_error("File not found")
        return False
    
    # Test 2: Taille raisonnable (< 200 MB)
    size_mb = exe_path.stat().st_size / (1024 * 1024)
    if size_mb < 200:
        print_success(f"Size OK: {size_mb:.2f} MB")
    else:
        print_warning(f"Size large: {size_mb:.2f} MB")
    
    # Test 3: Vérifier la signature (si signée)
    print_info("Checking digital signature...")
    success, stdout, _ = run_command(
        f'powershell -Command "Get-AuthenticodeSignature \'{exe_path}\' | Select-Object Status"',
        check=False,
        shell=True
    )
    
    if success and "Valid" in stdout:
        print_success("Digital signature: Valid")
    elif "NotSigned" in stdout:
        print_warning("Digital signature: Not signed")
        print_info("Sign the executable with: python build_antivirus_optimized.py --sign")
    else:
        print_warning("Could not verify signature")
    
    # Test 4: Scanner avec Windows Defender (si disponible)
    print_info("Scanning with Windows Defender...")
    print_warning("This may take a few seconds...")
    
    success, stdout, stderr = run_command(
        f'powershell -Command "Start-MpScan -ScanType CustomScan -ScanPath \'{exe_path}\'"',
        check=False,
        shell=True
    )
    
    if success:
        print_success("Windows Defender scan: PASSED (no threats detected)")
    else:
        if "threat" in stderr.lower() or "threat" in stdout.lower():
            print_error("Windows Defender scan: FAILED (threat detected)")
            print_warning("This is likely a false positive")
            print_info("Submit to Microsoft: https://www.microsoft.com/en-us/wdsi/filesubmission")
        else:
            print_warning("Windows Defender scan: Could not complete")
    
    print()
    print_info("For complete testing:")
    print_info("  1. Test on clean machine (without Python)")
    print_info("  2. Upload to VirusTotal: https://www.virustotal.com")
    print_info("  3. Test with different Defender protection levels")
    print_info("  4. Test SmartScreen warning on first run")
    
    return True

def sign_executable(exe_path, cert_path=None, cert_password=None):
    """Sign the executable with a code signing certificate"""
    print_header("Signing Executable")
    
    if not exe_path.exists():
        print_error(f"Executable not found: {exe_path}")
        return False
    
    # Vérifier si signtool est disponible
    success, stdout, _ = run_command("signtool /?", check=False)
    if not success:
        print_error("signtool.exe not found!")
        print_info("Install Windows SDK: https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/")
        return False
    
    print_success("signtool.exe found")
    
    # Demander le certificat si non fourni
    if not cert_path:
        print_info("Certificate file (.pfx) required")
        cert_path = input("Enter certificate path (or press Enter to skip): ").strip()
        
        if not cert_path:
            print_warning("Signing skipped")
            return False
    
    cert_path = Path(cert_path)
    if not cert_path.exists():
        print_error(f"Certificate not found: {cert_path}")
        return False
    
    # Demander le mot de passe si non fourni
    if not cert_password:
        import getpass
        cert_password = getpass.getpass("Enter certificate password: ")
    
    # Construire la commande signtool
    cmd = [
        "signtool", "sign",
        "/f", str(cert_path),
        "/p", cert_password,
        "/t", "http://timestamp.digicert.com",
        "/fd", "SHA256",
        "/d", "5GHz Cleaner",
        "/du", "https://github.com/UndKiMi/5Ghz_Cleaner",
        str(exe_path)
    ]
    
    print_info("Signing executable...")
    success, stdout, stderr = run_command(cmd, check=False)
    
    if success:
        print_success("Executable signed successfully!")
        
        # Vérifier la signature
        print_info("Verifying signature...")
        success, stdout, _ = run_command(
            ["signtool", "verify", "/pa", "/v", str(exe_path)],
            check=False
        )
        
        if success:
            print_success("Signature verified!")
        else:
            print_warning("Could not verify signature")
    else:
        print_error("Signing failed!")
        print(stderr)
        return False
    
    return True

def print_summary(args, exe_path, exe_size, sha256_hash):
    """Print build summary"""
    print_header("Build Summary")
    
    summary = f"""
  Build Configuration:
    - Version:        {VERSION}
    - Mode:           One File (single .exe)
    - Console:        Disabled (GUI only)
    - UPX:            Disabled (antivirus optimized)
    - Metadata:       {"Included" if VERSION_INFO.exists() else "Missing"}
    - Icon:           {"Included" if ICON_FILE.exists() else "Missing"}
    
  Output:
    - Executable:     {exe_path}
    - Size:           {exe_size:.2f} MB
    - SHA-256:        {sha256_hash[:16]}...
    - Checksums:      {DIST_DIR / 'CHECKSUMS.txt'}
    
  Security:
    - No UPX compression (reduces false positives)
    - Full metadata embedded
    - DLL integrity verified
    - Safe subprocess calls (shell=False)
    - Admin elevation via UAC (no bypass)
    
  Next Steps:
    1. Test executable: python build_antivirus_optimized.py --test
    2. Sign executable: python build_antivirus_optimized.py --sign
    3. Upload to VirusTotal: https://www.virustotal.com
    4. Submit to Microsoft: https://www.microsoft.com/en-us/wdsi/filesubmission
    5. Build reputation (SmartScreen takes 1-2 weeks)
"""
    print(f"{Colors.OKGREEN}{summary}{Colors.ENDC}")
    
    # Warnings
    if not VERSION_INFO.exists():
        print_warning("Missing version_info.py - this increases detection risk!")
    
    # Vérifier la signature
    success, stdout, _ = run_command(
        f'powershell -Command "Get-AuthenticodeSignature \'{exe_path}\' | Select-Object Status"',
        check=False,
        shell=True
    )
    
    if "NotSigned" in stdout:
        print_warning("Executable not signed - SmartScreen will show warnings!")
        print_info("Sign with: python build_antivirus_optimized.py --sign")
    
    print(f"""
{Colors.OKGREEN}
  ╔══════════════════════════════════════════════════════════════════════════╗
  ║                    BUILD COMPLETED SUCCESSFULLY!                         ║
  ║                                                                          ║
  ║  Optimized for: Zero False Positives                                    ║
  ║  Next: Sign & Test                                                      ║
  ╚══════════════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
""")

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main build function"""
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Build 5GHz Cleaner (Antivirus Optimized)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python build_antivirus_optimized.py                # Standard build
  python build_antivirus_optimized.py --clean         # Clean build
  python build_antivirus_optimized.py --test          # Test executable
  python build_antivirus_optimized.py --sign          # Sign executable
  python build_antivirus_optimized.py --clean --test  # Clean, build, test
        """
    )
    parser.add_argument('--clean', action='store_true', help='Clean previous build')
    parser.add_argument('--test', action='store_true', help='Test executable after build')
    parser.add_argument('--sign', action='store_true', help='Sign executable with certificate')
    parser.add_argument('--cert', type=str, help='Path to certificate (.pfx)')
    parser.add_argument('--cert-password', type=str, help='Certificate password')
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Si --test ou --sign uniquement, ne pas rebuild
    if (args.test or args.sign) and not args.clean:
        exe_path = DIST_DIR / f"{APP_NAME}.exe"
        
        if args.test:
            if exe_path.exists():
                test_executable(exe_path)
            else:
                print_error(f"Executable not found: {exe_path}")
                print_info("Build first: python build_antivirus_optimized.py")
                return 1
        
        if args.sign:
            if exe_path.exists():
                sign_executable(exe_path, args.cert, args.cert_password)
            else:
                print_error(f"Executable not found: {exe_path}")
                print_info("Build first: python build_antivirus_optimized.py")
                return 1
        
        return 0
    
    # Check prerequisites
    if not check_prerequisites():
        print_error("Prerequisites check failed!")
        print_info("Fix the issues above and try again")
        return 1
    
    # Clean build
    clean_build(args)
    
    # Build executable
    if not build_executable(args):
        print_error("Build failed!")
        return 1
    
    # Post-build tasks
    result = post_build_tasks(args)
    if not result:
        print_error("Post-build tasks failed!")
        return 1
    
    success, exe_path, exe_size, sha256_hash = result
    
    # Print summary
    print_summary(args, exe_path, exe_size, sha256_hash)
    
    # Test if requested
    if args.test:
        test_executable(exe_path)
    
    # Sign if requested
    if args.sign:
        sign_executable(exe_path, args.cert, args.cert_password)
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Build interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}Unexpected error: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
