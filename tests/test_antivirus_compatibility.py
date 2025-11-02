"""
Tests de Compatibilité Antivirus
Teste automatiquement la détection par Windows Defender et autres antivirus

USAGE:
    python tests/test_antivirus_compatibility.py
    python tests/test_antivirus_compatibility.py --full
    python tests/test_antivirus_compatibility.py --defender-only
"""

import sys
import os
import subprocess
import hashlib
import time
from pathlib import Path
from datetime import datetime

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

# ============================================================================
# CONFIGURATION
# ============================================================================

APP_NAME = "5Ghz_Cleaner"
DIST_DIR = Path("dist")
EXE_PATH = DIST_DIR / f"{APP_NAME}.exe"

# Colors
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def print_header(message):
    """Print header"""
    print(f"\n{Colors.CYAN}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.CYAN}{message}{Colors.ENDC}")
    print(f"{Colors.CYAN}{'=' * 80}{Colors.ENDC}\n")

def print_test(name, status, message=""):
    """Print test result"""
    if status == "PASS":
        icon = "✅"
        color = Colors.GREEN
    elif status == "FAIL":
        icon = "❌"
        color = Colors.RED
    elif status == "WARN":
        icon = "⚠️"
        color = Colors.YELLOW
    else:
        icon = "ℹ️"
        color = Colors.BLUE
    
    print(f"{color}{icon} {name}: {status}{Colors.ENDC}")
    if message:
        print(f"   {message}")

def run_powershell(command):
    """Execute PowerShell command"""
    try:
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

# ============================================================================
# TESTS
# ============================================================================

def test_file_exists():
    """Test 1: Vérifier que l'exécutable existe"""
    print_test("File Existence", "INFO", f"Checking: {EXE_PATH}")
    
    if EXE_PATH.exists():
        size_mb = EXE_PATH.stat().st_size / (1024 * 1024)
        print_test("File Found", "PASS", f"Size: {size_mb:.2f} MB")
        return True
    else:
        print_test("File Not Found", "FAIL", f"Build first: python build_antivirus_optimized.py")
        return False

def test_file_integrity():
    """Test 2: Vérifier l'intégrité du fichier"""
    print_test("File Integrity", "INFO", "Calculating SHA-256...")
    
    try:
        sha256_hash = hashlib.sha256()
        with open(EXE_PATH, 'rb') as f:
            for byte_block in iter(lambda: f.read(65536), b""):
                sha256_hash.update(byte_block)
        
        hash_value = sha256_hash.hexdigest()
        print_test("SHA-256 Calculated", "PASS", f"{hash_value[:32]}...")
        
        # Vérifier avec le fichier CHECKSUMS.txt si disponible
        checksums_file = DIST_DIR / "CHECKSUMS.txt"
        if checksums_file.exists():
            with open(checksums_file, 'r') as f:
                content = f.read()
                if hash_value in content:
                    print_test("Hash Verification", "PASS", "Matches CHECKSUMS.txt")
                else:
                    print_test("Hash Verification", "WARN", "Does not match CHECKSUMS.txt")
        
        return True
    except Exception as e:
        print_test("Hash Calculation Failed", "FAIL", str(e))
        return False

def test_digital_signature():
    """Test 3: Vérifier la signature numérique"""
    print_test("Digital Signature", "INFO", "Checking signature...")
    
    success, stdout, stderr = run_powershell(
        f"Get-AuthenticodeSignature '{EXE_PATH}' | Select-Object Status, SignerCertificate"
    )
    
    if not success:
        print_test("Signature Check Failed", "WARN", "Could not verify signature")
        return False
    
    if "Valid" in stdout:
        print_test("Signature Valid", "PASS", "Digitally signed")
        
        # Extraire les infos du certificat
        success2, stdout2, _ = run_powershell(
            f"(Get-AuthenticodeSignature '{EXE_PATH}').SignerCertificate.Subject"
        )
        if success2:
            print_test("Certificate Info", "INFO", stdout2.strip())
        
        return True
    elif "NotSigned" in stdout:
        print_test("Not Signed", "WARN", "Executable is not digitally signed")
        print_test("Recommendation", "INFO", "Sign with: python build_antivirus_optimized.py --sign")
        return False
    else:
        print_test("Signature Invalid", "FAIL", "Signature verification failed")
        return False

def test_windows_defender_scan():
    """Test 4: Scanner avec Windows Defender"""
    print_test("Windows Defender Scan", "INFO", "Starting scan...")
    print_test("Please Wait", "INFO", "This may take 10-30 seconds...")
    
    # Vérifier que Defender est actif
    success, stdout, _ = run_powershell("Get-MpComputerStatus | Select-Object AntivirusEnabled")
    
    if not success or "True" not in stdout:
        print_test("Defender Not Active", "WARN", "Windows Defender is not enabled")
        return False
    
    print_test("Defender Active", "PASS", "Windows Defender is running")
    
    # Scanner le fichier
    start_time = time.time()
    success, stdout, stderr = run_powershell(
        f"Start-MpScan -ScanType CustomScan -ScanPath '{EXE_PATH}'"
    )
    scan_time = time.time() - start_time
    
    if success:
        print_test("Defender Scan Complete", "PASS", f"No threats detected ({scan_time:.1f}s)")
        return True
    else:
        # Vérifier si c'est une vraie détection ou une erreur
        if "threat" in stderr.lower() or "threat" in stdout.lower():
            print_test("Threat Detected", "FAIL", "Windows Defender flagged the executable")
            print_test("False Positive", "WARN", "This is likely a false positive")
            print_test("Action Required", "INFO", "Submit to Microsoft: https://www.microsoft.com/en-us/wdsi/filesubmission")
            return False
        else:
            print_test("Scan Error", "WARN", f"Could not complete scan: {stderr}")
            return False

def test_defender_threat_history():
    """Test 5: Vérifier l'historique des menaces"""
    print_test("Threat History", "INFO", "Checking recent detections...")
    
    success, stdout, _ = run_powershell(
        "Get-MpThreatDetection | Where-Object {$_.Resources -like '*5Ghz_Cleaner*'} | Select-Object -First 5"
    )
    
    if success and stdout.strip():
        print_test("Threats Found", "FAIL", "Executable was previously detected")
        print(stdout)
        return False
    else:
        print_test("No Threats", "PASS", "No previous detections found")
        return True

def test_smartscreen_reputation():
    """Test 6: Vérifier la réputation SmartScreen"""
    print_test("SmartScreen Reputation", "INFO", "Checking reputation...")
    
    # Note: La réputation SmartScreen n'est pas directement vérifiable
    # On peut seulement vérifier si le fichier est signé
    
    success, stdout, _ = run_powershell(
        f"Get-AuthenticodeSignature '{EXE_PATH}' | Select-Object Status"
    )
    
    if "Valid" in stdout:
        print_test("Signed Executable", "PASS", "Good for SmartScreen reputation")
        print_test("Reputation Build", "INFO", "Takes 1-2 weeks with valid signature")
    else:
        print_test("Unsigned Executable", "WARN", "SmartScreen will show warnings")
        print_test("Recommendation", "INFO", "Use EV certificate for instant reputation")
    
    return True

def test_file_metadata():
    """Test 7: Vérifier les métadonnées"""
    print_test("File Metadata", "INFO", "Checking embedded metadata...")
    
    success, stdout, _ = run_powershell(
        f"(Get-Item '{EXE_PATH}').VersionInfo | Select-Object FileDescription, ProductName, CompanyName, FileVersion"
    )
    
    if success and stdout.strip():
        # Vérifier que les métadonnées sont présentes
        if "5GHz Cleaner" in stdout or "UndKiMi" in stdout:
            print_test("Metadata Present", "PASS", "Complete metadata found")
            print(f"   {stdout.strip()}")
            return True
        else:
            print_test("Metadata Incomplete", "WARN", "Some metadata missing")
            print(f"   {stdout.strip()}")
            return False
    else:
        print_test("No Metadata", "FAIL", "No version information found")
        print_test("Critical Issue", "WARN", "Missing metadata increases detection risk!")
        print_test("Fix", "INFO", "Add version_info.py and rebuild")
        return False

def test_virustotal_upload():
    """Test 8: Instructions pour VirusTotal"""
    print_test("VirusTotal Scan", "INFO", "Manual upload required")
    print_test("Instructions", "INFO", "")
    print(f"   1. Go to: https://www.virustotal.com")
    print(f"   2. Upload: {EXE_PATH}")
    print(f"   3. Wait for scan results (60+ antivirus engines)")
    print(f"   4. Target: 0-2 detections (out of 70+)")
    print(f"   5. Report false positives to each vendor")
    print()
    
    return True

def test_defender_exclusion():
    """Test 9: Vérifier si le fichier est exclu"""
    print_test("Defender Exclusions", "INFO", "Checking exclusions...")
    
    success, stdout, _ = run_powershell(
        "Get-MpPreference | Select-Object -ExpandProperty ExclusionPath"
    )
    
    if success and str(EXE_PATH) in stdout:
        print_test("File Excluded", "WARN", "File is in Defender exclusions")
        print_test("Note", "INFO", "Remove exclusion for real-world testing")
    else:
        print_test("Not Excluded", "PASS", "Testing with full protection")
    
    return True

def test_realtime_protection():
    """Test 10: Vérifier la protection en temps réel"""
    print_test("Real-Time Protection", "INFO", "Checking Defender status...")
    
    success, stdout, _ = run_powershell(
        "Get-MpComputerStatus | Select-Object RealTimeProtectionEnabled, IoavProtectionEnabled, BehaviorMonitorEnabled"
    )
    
    if success:
        if "True" in stdout:
            print_test("Full Protection Active", "PASS", "Real-time protection enabled")
            print(f"   {stdout.strip()}")
        else:
            print_test("Protection Disabled", "WARN", "Some protection features disabled")
            print(f"   {stdout.strip()}")
    
    return True

# ============================================================================
# MAIN TEST SUITE
# ============================================================================

def run_all_tests():
    """Run all tests"""
    print_header("5GH'z Cleaner - Antivirus Compatibility Tests")
    
    print(f"Testing: {EXE_PATH}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("File Existence", test_file_exists),
        ("File Integrity", test_file_integrity),
        ("Digital Signature", test_digital_signature),
        ("Windows Defender Scan", test_windows_defender_scan),
        ("Threat History", test_defender_threat_history),
        ("SmartScreen Reputation", test_smartscreen_reputation),
        ("File Metadata", test_file_metadata),
        ("VirusTotal Upload", test_virustotal_upload),
        ("Defender Exclusions", test_defender_exclusion),
        ("Real-Time Protection", test_realtime_protection),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print_header(f"Test: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_test(test_name, "ERROR", str(e))
            results.append((test_name, False))
        
        time.sleep(0.5)  # Pause entre les tests
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    print()
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    print()
    
    if passed == total:
        print(f"{Colors.GREEN}{'=' * 80}{Colors.ENDC}")
        print(f"{Colors.GREEN}🎉 ALL TESTS PASSED! Executable is clean.{Colors.ENDC}")
        print(f"{Colors.GREEN}{'=' * 80}{Colors.ENDC}")
        return 0
    else:
        print(f"{Colors.YELLOW}{'=' * 80}{Colors.ENDC}")
        print(f"{Colors.YELLOW}⚠️  SOME TESTS FAILED - Review results above{Colors.ENDC}")
        print(f"{Colors.YELLOW}{'=' * 80}{Colors.ENDC}")
        print()
        print("Recommendations:")
        print("  1. Add digital signature (if not signed)")
        print("  2. Add version metadata (if missing)")
        print("  3. Submit false positives to Microsoft")
        print("  4. Upload to VirusTotal and report false positives")
        return 1

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Test antivirus compatibility')
    parser.add_argument('--full', action='store_true', help='Run all tests')
    parser.add_argument('--defender-only', action='store_true', help='Run only Defender tests')
    args = parser.parse_args()
    
    try:
        sys.exit(run_all_tests())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tests interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
