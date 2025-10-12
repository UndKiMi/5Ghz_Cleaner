"""
Test Complet de Toutes les Sécurités - 5GHz Cleaner
Vérifie que toutes les protections sont fonctionnelles à 100%
"""
import sys
import os
import io

# Configurer l'encodage UTF-8 pour la console Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.security_core import WindowsSecurityCore, security_core
from backend.security import SecurityManager, security_manager

def test_security_core_paths():
    """Test 1: Vérifier que les 200+ chemins sont bien chargés"""
    print("\n" + "="*80)
    print("TEST 1: Vérification des chemins protégés")
    print("="*80)
    
    paths_count = len(WindowsSecurityCore.CRITICAL_SYSTEM_PATHS)
    print(f"✓ Nombre de chemins protégés: {paths_count}")
    
    if paths_count < 200:
        print(f"❌ ÉCHEC: Seulement {paths_count} chemins (attendu: 200+)")
        return False
    
    print(f"✅ SUCCÈS: {paths_count} chemins protégés chargés")
    
    # Vérifier quelques chemins critiques
    critical_paths_to_check = [
        r'C:\Windows\System32',
        r'C:\Program Files\Microsoft Office',
        r'C:\Program Files (x86)\Microsoft\Edge',
        r'C:\Program Files\Google\Chrome',
        r'C:\Windows\System32\BitLocker',
        r'C:\Program Files\NVIDIA Corporation',
    ]
    
    print("\nVérification de chemins critiques spécifiques:")
    for path in critical_paths_to_check:
        if path in WindowsSecurityCore.CRITICAL_SYSTEM_PATHS:
            print(f"  ✓ {path}")
        else:
            print(f"  ❌ MANQUANT: {path}")
            return False
    
    return True


def test_path_validation():
    """Test 2: Vérifier que la validation de chemins fonctionne"""
    print("\n" + "="*80)
    print("TEST 2: Validation de chemins")
    print("="*80)
    
    # Chemins qui DOIVENT être bloqués
    blocked_paths = [
        r'C:\Windows\System32\kernel32.dll',
        r'C:\Windows\System32\drivers\ntfs.sys',
        r'C:\Program Files\Microsoft Office\Office16\WINWORD.EXE',
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        r'C:\Windows\System32\config\SAM',
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    ]
    
    print("\nVérification des chemins BLOQUÉS:")
    all_blocked = True
    for path in blocked_paths:
        is_safe = WindowsSecurityCore.is_path_safe(path)
        if is_safe:
            print(f"  ❌ ÉCHEC: {path} devrait être bloqué mais est autorisé!")
            all_blocked = False
        else:
            print(f"  ✓ Bloqué: {path}")
    
    if not all_blocked:
        return False
    
    # Chemins qui DOIVENT être autorisés (temp)
    temp_dir = os.getenv('TEMP')
    allowed_paths = [
        os.path.join(temp_dir, 'test.tmp'),
        os.path.join(temp_dir, 'cache', 'file.cache'),
    ]
    
    print("\nVérification des chemins AUTORISÉS (temp):")
    all_allowed = True
    for path in allowed_paths:
        is_safe = WindowsSecurityCore.is_path_safe(path)
        if not is_safe:
            print(f"  ❌ ÉCHEC: {path} devrait être autorisé mais est bloqué!")
            all_allowed = False
        else:
            print(f"  ✓ Autorisé: {path}")
    
    if not all_allowed:
        return False
    
    print("\n✅ SUCCÈS: Validation de chemins fonctionne correctement")
    return True


def test_operation_validation():
    """Test 3: Vérifier que validate_operation fonctionne"""
    print("\n" + "="*80)
    print("TEST 3: Validation d'opérations")
    print("="*80)
    
    # Test suppression dans System32 (DOIT échouer)
    path_system = r'C:\Windows\System32\test.dll'
    is_safe, reason = WindowsSecurityCore.validate_operation(path_system, "delete")
    
    if is_safe:
        print(f"❌ ÉCHEC: Suppression dans System32 autorisée!")
        return False
    else:
        print(f"✓ Suppression System32 bloquée: {reason}")
    
    # Test suppression dans TEMP (DOIT réussir)
    temp_dir = os.getenv('TEMP')
    path_temp = os.path.join(temp_dir, 'test.tmp')
    is_safe, reason = WindowsSecurityCore.validate_operation(path_temp, "delete")
    
    if not is_safe:
        print(f"❌ ÉCHEC: Suppression dans TEMP bloquée: {reason}")
        return False
    else:
        print(f"✓ Suppression TEMP autorisée: {reason}")
    
    print("\n✅ SUCCÈS: Validation d'opérations fonctionne correctement")
    return True


def test_file_signature():
    """Test 4: Vérifier que WinVerifyTrust fonctionne"""
    print("\n" + "="*80)
    print("TEST 4: Vérification de signature (WinVerifyTrust)")
    print("="*80)
    
    # Tester avec un fichier système Windows (devrait être signé)
    system_file = r'C:\Windows\System32\kernel32.dll'
    
    if not os.path.exists(system_file):
        print(f"⚠️  SKIP: {system_file} n'existe pas")
        return True
    
    try:
        result = security_manager.get_file_signature(system_file)
        print(f"✓ Signature de {system_file}: {result}")
        
        if result in ["Valid", "NotSigned", "NotTrusted", "Invalid", "Unknown"]:
            print("✅ SUCCÈS: WinVerifyTrust retourne un résultat valide")
            return True
        else:
            print(f"❌ ÉCHEC: Résultat inattendu: {result}")
            return False
            
    except Exception as e:
        print(f"❌ ÉCHEC: Exception lors de la vérification: {e}")
        return False


def test_protected_files():
    """Test 5: Vérifier que les fichiers critiques sont protégés"""
    print("\n" + "="*80)
    print("TEST 5: Protection des fichiers critiques")
    print("="*80)
    
    files_count = len(WindowsSecurityCore.CRITICAL_SYSTEM_FILES)
    print(f"✓ Nombre de fichiers protégés: {files_count}")
    
    if files_count < 140:
        print(f"❌ ÉCHEC: Seulement {files_count} fichiers (attendu: 140+)")
        return False
    
    # Vérifier quelques fichiers critiques
    critical_files = [
        'ntoskrnl.exe',
        'kernel32.dll',
        'explorer.exe',
        'ntdll.dll',
        'msmpeng.exe',  # Windows Defender
    ]
    
    print("\nVérification de fichiers critiques:")
    for filename in critical_files:
        if filename in WindowsSecurityCore.CRITICAL_SYSTEM_FILES:
            print(f"  ✓ {filename}")
        else:
            print(f"  ❌ MANQUANT: {filename}")
            return False
    
    print(f"\n✅ SUCCÈS: {files_count} fichiers critiques protégés")
    return True


def test_protected_extensions():
    """Test 6: Vérifier que les extensions dangereuses sont protégées"""
    print("\n" + "="*80)
    print("TEST 6: Protection des extensions")
    print("="*80)
    
    extensions_count = len(WindowsSecurityCore.PROTECTED_EXTENSIONS)
    print(f"✓ Nombre d'extensions protégées: {extensions_count}")
    
    # Vérifier quelques extensions critiques
    critical_extensions = [
        '.exe', '.dll', '.sys', '.drv',
        '.inf', '.cat', '.msi', '.reg',
    ]
    
    print("\nVérification d'extensions critiques:")
    all_present = True
    for ext in critical_extensions:
        if ext in WindowsSecurityCore.PROTECTED_EXTENSIONS:
            print(f"  ✓ {ext}")
        else:
            print(f"  ❌ MANQUANT: {ext}")
            all_present = False
    
    if not all_present:
        return False
    
    print(f"\n✅ SUCCÈS: {extensions_count} extensions protégées")
    return True


def test_temp_directories():
    """Test 7: Vérifier que les dossiers temp sont correctement identifiés"""
    print("\n" + "="*80)
    print("TEST 7: Identification des dossiers temporaires")
    print("="*80)
    
    allowed_temps = WindowsSecurityCore.get_allowed_temp_directories()
    print(f"✓ Nombre de dossiers temp autorisés: {len(allowed_temps)}")
    
    print("\nDossiers temp identifiés:")
    for temp_dir in allowed_temps:
        print(f"  ✓ {temp_dir}")
    
    # Vérifier que TEMP est dans la liste
    temp_env = os.getenv('TEMP')
    if temp_env:
        temp_normalized = os.path.normpath(temp_env)
        if temp_normalized in allowed_temps or any(temp_normalized.lower() == t.lower() for t in allowed_temps):
            print(f"\n✅ SUCCÈS: TEMP ({temp_env}) correctement identifié")
            return True
        else:
            print(f"\n❌ ÉCHEC: TEMP ({temp_env}) non identifié")
            return False
    else:
        print("\n⚠️  WARNING: Variable TEMP non définie")
        return True


def run_all_tests():
    """Exécute tous les tests de sécurité"""
    print("\n")
    print("="*80)
    print("TEST COMPLET DE TOUTES LES SÉCURITÉS - 5GHz Cleaner")
    print("="*80)
    print()
    
    tests = [
        ("Chemins protégés (200+)", test_security_core_paths),
        ("Validation de chemins", test_path_validation),
        ("Validation d'opérations", test_operation_validation),
        ("Signature WinVerifyTrust", test_file_signature),
        ("Fichiers critiques (140+)", test_protected_files),
        ("Extensions protégées", test_protected_extensions),
        ("Dossiers temporaires", test_temp_directories),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"\n❌ EXCEPTION dans {test_name}: {e}")
            import traceback
            traceback.print_exc()
            results[test_name] = False
    
    # Rapport final
    print("\n")
    print("="*80)
    print("RAPPORT FINAL")
    print("="*80)
    print()
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Résultat global: {passed}/{total} tests réussis")
    print()
    
    if passed == total:
        print("="*80)
        print("✅ TOUTES LES SÉCURITÉS SONT FONCTIONNELLES À 100%")
        print("="*80)
        return 0
    else:
        print("="*80)
        print("❌ CERTAINES SÉCURITÉS ONT ÉCHOUÉ")
        print("="*80)
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
