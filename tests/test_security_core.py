"""
Tests pour le module de sécurité core
Vérifie que tous les chemins système sont bien protégés
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.security_core import security_core

def test_critical_paths_blocked():
    """Test que les chemins critiques sont bloqués"""
    print("="*80)
    print("TEST 1: Vérification des chemins système critiques")
    print("="*80)
    
    critical_paths = [
        r"C:\Windows\System32\kernel32.dll",
        r"C:\Windows\SysWOW64\ntdll.dll",
        r"C:\Windows\explorer.exe",
        r"C:\Windows\System32\drivers\ntfs.sys",
        r"C:\Program Files\test.exe",
        r"C:\Windows\Boot\bootmgr",
    ]
    
    all_blocked = True
    for path in critical_paths:
        is_safe = security_core.is_path_safe(path)
        status = "BLOQUE" if not is_safe else "AUTORISE"
        print(f"{status}: {path}")
        if is_safe:
            all_blocked = False
    
    print()
    if all_blocked:
        print("SUCCES: Tous les chemins critiques sont bloques")
    else:
        print("ECHEC: Certains chemins critiques ne sont pas bloques!")
    print()
    return all_blocked

def test_temp_paths_allowed():
    """Test que les chemins temp sont autorisés"""
    print("="*80)
    print("TEST 2: Vérification des chemins temporaires autorisés")
    print("="*80)
    
    temp_path = os.getenv('TEMP')
    if temp_path:
        test_file = os.path.join(temp_path, "test_file.tmp")
        is_safe = security_core.is_path_safe(test_file)
        is_in_temp = security_core.is_in_allowed_temp_directory(test_file)
        
        print(f"Chemin temp: {temp_path}")
        print(f"Fichier test: {test_file}")
        print(f"is_path_safe: {is_safe}")
        print(f"is_in_allowed_temp: {is_in_temp}")
        print()
        
        if is_safe and is_in_temp:
            print("SUCCES: Les fichiers .tmp dans TEMP sont autorises")
            return True
        else:
            print("ECHEC: Les fichiers temp ne sont pas correctement autorises!")
            return False
    else:
        print("WARNING: Variable TEMP non definie")
        return True

def test_validation_operation():
    """Test de la validation des opérations"""
    print("="*80)
    print("TEST 3: Validation des opérations")
    print("="*80)
    
    # Test suppression dans System32 (doit être refusée)
    path1 = r"C:\Windows\System32\test.dll"
    is_safe1, reason1 = security_core.validate_operation(path1, "delete")
    print(f"Suppression dans System32: {is_safe1} - {reason1}")
    
    # Test suppression dans TEMP (doit être autorisée)
    temp_path = os.getenv('TEMP')
    if temp_path:
        path2 = os.path.join(temp_path, "test.tmp")
        is_safe2, reason2 = security_core.validate_operation(path2, "delete")
        print(f"Suppression dans TEMP: {is_safe2} - {reason2}")
        
        success = (not is_safe1) and is_safe2
    else:
        success = not is_safe1
    
    print()
    if success:
        print("SUCCES: Validation des operations fonctionne correctement")
    else:
        print("ECHEC: Validation des operations incorrecte!")
    print()
    return success

def test_protected_extensions():
    """Test que les extensions protégées sont bloquées"""
    print("="*80)
    print("TEST 4: Vérification des extensions protégées")
    print("="*80)
    
    temp_path = os.getenv('TEMP', 'C:\\Temp')
    
    protected_files = [
        os.path.join(temp_path, "test.dll"),
        os.path.join(temp_path, "test.exe"),
        os.path.join(temp_path, "test.sys"),
        os.path.join(temp_path, "test.inf"),
    ]
    
    all_blocked = True
    for path in protected_files:
        is_safe = security_core.is_path_safe(path)
        status = "BLOQUE" if not is_safe else "AUTORISE"
        print(f"{status}: {os.path.basename(path)}")
        if is_safe:
            all_blocked = False
    
    print()
    if all_blocked:
        print("SUCCES: Toutes les extensions protegees sont bloquees")
    else:
        print("ECHEC: Certaines extensions protegees ne sont pas bloquees!")
    print()
    return all_blocked

def run_all_tests():
    """Exécute tous les tests"""
    print("\n")
    print("=" + "="*78 + "=")
    print(" "*20 + "TESTS DE SECURITE - MODULE CORE")
    print("=" + "="*78 + "=")
    print()
    
    results = []
    
    results.append(("Chemins critiques bloqués", test_critical_paths_blocked()))
    results.append(("Chemins temp autorisés", test_temp_paths_allowed()))
    results.append(("Validation opérations", test_validation_operation()))
    results.append(("Extensions protégées", test_protected_extensions()))
    
    print("="*80)
    print("RÉSUMÉ DES TESTS")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status}: {name}")
    
    print()
    print(f"Resultat: {passed}/{total} tests reussis")
    
    if passed == total:
        print()
        print("TOUS LES TESTS SONT PASSES!")
        print("Le module de securite fonctionne parfaitement!")
    else:
        print()
        print("CERTAINS TESTS ONT ECHOUE!")
        print("Verifiez la configuration du module de securite!")
    
    print("="*80)
    print()
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
