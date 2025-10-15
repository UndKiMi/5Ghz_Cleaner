#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5GH'z Cleaner - Automated Build Script (Python)
Version: MAJOR UPDATE
Author: UndKiMi
License: CC BY-NC-SA 4.0

USAGE:
    python build.py                 # Build standard
    python build.py --clean         # Clean build
    python build.py --debug         # Debug mode (console visible)
    python build.py --onedir        # One directory mode
    python build.py --no-upx        # Disable UPX compression
    python build.py --skip-tests    # Skip pre-build tests
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
VERSION = "MAJOR UPDATE"
AUTHOR = "UndKiMi"

BUILD_DIR = Path("build")
DIST_DIR = Path("dist")
SPEC_FILE = Path(f"{APP_NAME}.spec")
SPEC_TEMPLATE = Path(f"{APP_NAME}.spec.template")

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
    print(f"\n{Colors.OKCYAN}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}[STEP] {message}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{'=' * 70}{Colors.ENDC}")

def print_success(message):
    """Print a success message"""
    print(f"{Colors.OKGREEN}  [OK] {message}{Colors.ENDC}")

def print_error(message):
    """Print an error message"""
    print(f"{Colors.FAIL}  [ERROR] {message}{Colors.ENDC}")

def print_warning(message):
    """Print a warning message"""
    print(f"{Colors.WARNING}  [!] {message}{Colors.ENDC}")

def print_banner():
    """Print the application banner"""
    banner = f"""
{Colors.OKCYAN}
  ╔═══════════════════════════════════════════════════════════════════╗
  ║                                                                   ║
  ║              5GH'z CLEANER - BUILD SCRIPT v{VERSION:^15}║
  ║                                                                   ║
  ║  Windows 11 Cleaning & Optimization Tool                         ║
  ║  Author: {AUTHOR:^56}║
  ║                                                                   ║
  ╚═══════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
"""
    print(banner)

def run_command(cmd, check=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def calculate_sha256(filepath):
    """Calculate SHA256 hash of a file"""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# ============================================================================
# BUILD FUNCTIONS
# ============================================================================

def check_prerequisites():
    """Check if all prerequisites are installed"""
    print_header("Pre-Build Checks")
    
    # Check Python
    success, stdout, _ = run_command("python --version", check=False)
    if success:
        print_success(f"Python found: {stdout.strip()}")
    else:
        print_error("Python not found! Install Python 3.11+")
        return False
    
    # Check PyInstaller
    success, stdout, _ = run_command("pyinstaller --version", check=False)
    if success:
        print_success(f"PyInstaller found: {stdout.strip()}")
    else:
        print_warning("PyInstaller not found. Installing...")
        success, _, _ = run_command("pip install pyinstaller")
        if not success:
            print_error("Failed to install PyInstaller")
            return False
        print_success("PyInstaller installed")
    
    # Check spec template
    if not SPEC_TEMPLATE.exists():
        print_error(f"Spec template not found: {SPEC_TEMPLATE}")
        return False
    print_success(f"Spec template found: {SPEC_TEMPLATE}")
    
    return True

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
    
    # Remove spec file
    if SPEC_FILE.exists():
        SPEC_FILE.unlink()
        print_success(f"Removed: {SPEC_FILE}")
    
    # Remove Python cache
    for pycache in Path(".").rglob("__pycache__"):
        shutil.rmtree(pycache)
    for pyc in Path(".").rglob("*.pyc"):
        pyc.unlink()
    print_success("Removed Python cache files")

def prepare_spec_file(args):
    """Prepare the spec file from template"""
    print_header("Preparing Build Configuration")
    
    # Read template
    with open(SPEC_TEMPLATE, 'r', encoding='utf-8') as f:
        spec_content = f.read()
    
    # Modify based on arguments
    if args.debug:
        spec_content = spec_content.replace(
            "CONSOLE_ENABLED = False",
            "CONSOLE_ENABLED = True"
        )
        print_success("Debug mode enabled (console visible)")
    
    if args.onedir:
        spec_content = spec_content.replace(
            "ONE_FILE = True",
            "ONE_FILE = False"
        )
        print_success("One-directory mode enabled (faster startup)")
    
    if args.no_upx:
        spec_content = spec_content.replace(
            "UPX_ENABLED = True",
            "UPX_ENABLED = False"
        )
        print_success("UPX compression disabled")
    
    # Write spec file
    with open(SPEC_FILE, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print_success("Spec file created from template")

def run_tests(args):
    """Run pre-build tests"""
    if args.skip_tests:
        return True
    
    print_header("Running Tests")
    
    # Test critical imports
    print("  Testing critical imports...")
    test_code = """
import sys
try:
    import flet
    import backend.cleaner
    import backend.security_core
    import frontend.app
    print('OK')
except Exception as e:
    print(f'ERROR: {e}')
    sys.exit(1)
"""
    
    success, stdout, stderr = run_command(f'python -c "{test_code}"', check=False)
    if success and 'OK' in stdout:
        print_success("All imports successful")
    else:
        print_error(f"Import test failed: {stderr}")
        return False
    
    # Verify signature
    print("  Verifying code signature...")
    success, _, _ = run_command("python backend/signature_manager.py --verify", check=False)
    if success:
        print_success("Signature verification passed")
    else:
        print_warning("Signature verification failed (continuing anyway)")
    
    return True

def build_executable(args):
    """Build the executable with PyInstaller"""
    print_header("Building Executable")
    
    print("  Running PyInstaller...")
    success, stdout, stderr = run_command(f"pyinstaller {SPEC_FILE} --clean", check=False)
    
    if not success:
        print_error("Build failed!")
        print(stderr)
        return False
    
    print_success("Build completed successfully!")
    return True

def post_build_tasks(args):
    """Perform post-build tasks"""
    print_header("Post-Build Tasks")
    
    # Determine exe path
    if args.onedir:
        exe_path = DIST_DIR / APP_NAME / f"{APP_NAME}.exe"
    else:
        exe_path = DIST_DIR / f"{APP_NAME}.exe"
    
    # Check if exe exists
    if not exe_path.exists():
        print_error(f"Executable not found: {exe_path}")
        return False
    
    exe_size = exe_path.stat().st_size / (1024 * 1024)  # MB
    print_success(f"Executable created: {exe_path} ({exe_size:.2f} MB)")
    
    # Generate checksums
    print("  Generating checksums...")
    sha256_hash = calculate_sha256(exe_path)
    
    checksum_file = DIST_DIR / "CHECKSUMS_BUILD.txt"
    with open(checksum_file, 'w', encoding='utf-8') as f:
        f.write(f"5GH'z Cleaner {VERSION} - Build Checksums\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Executable: {APP_NAME}.exe\n")
        f.write(f"SHA-256: {sha256_hash}\n\n")
        f.write("Verify with:\n")
        f.write(f"  python -c \"import hashlib; print(hashlib.sha256(open('{APP_NAME}.exe', 'rb').read()).hexdigest())\"\n")
    
    print_success(f"Checksums saved: {checksum_file}")
    
    # Copy documentation
    print("  Copying documentation...")
    docs_to_copy = ["README.md", "LICENSE"]
    for doc in docs_to_copy:
        if Path(doc).exists():
            shutil.copy(doc, DIST_DIR)
    
    # Copy checksums from docs
    checksums_src = Path("docs/reports/CHECKSUMS.txt")
    if checksums_src.exists():
        shutil.copy(checksums_src, DIST_DIR)
    
    print_success("Documentation copied")
    
    return True, exe_path, exe_size

def print_summary(args, exe_path, exe_size):
    """Print build summary"""
    print_header("Build Summary")
    
    summary = f"""
  Build Configuration:
    - Version:      {VERSION}
    - Mode:         {"One Directory" if args.onedir else "One File"}
    - Console:      {"Enabled (Debug)" if args.debug else "Disabled"}
    - UPX:          {"Disabled" if args.no_upx else "Enabled"}
    - Size:         {exe_size:.2f} MB
    
  Output:
    - Executable:   {exe_path}
    - Checksums:    {DIST_DIR / 'CHECKSUMS_BUILD.txt'}
    
  Next Steps:
    1. Test the executable
    2. Run security scan
    3. Create release package
    4. Upload to GitHub Releases
"""
    print(f"{Colors.OKGREEN}{summary}{Colors.ENDC}")
    
    print(f"""
{Colors.OKGREEN}
  ╔═══════════════════════════════════════════════════════════════════╗
  ║                    BUILD COMPLETED SUCCESSFULLY!                  ║
  ╚═══════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
""")

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main build function"""
    # Parse arguments
    parser = argparse.ArgumentParser(description='Build 5GHz Cleaner executable')
    parser.add_argument('--clean', action='store_true', help='Clean previous build')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode (console visible)')
    parser.add_argument('--onedir', action='store_true', help='One directory mode (faster startup)')
    parser.add_argument('--no-upx', action='store_true', help='Disable UPX compression')
    parser.add_argument('--skip-tests', action='store_true', help='Skip pre-build tests')
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Clean build
    clean_build(args)
    
    # Prepare spec file
    prepare_spec_file(args)
    
    # Run tests
    if not run_tests(args):
        sys.exit(1)
    
    # Build executable
    if not build_executable(args):
        sys.exit(1)
    
    # Post-build tasks
    result = post_build_tasks(args)
    if not result:
        sys.exit(1)
    
    success, exe_path, exe_size = result
    
    # Print summary
    print_summary(args, exe_path, exe_size)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
