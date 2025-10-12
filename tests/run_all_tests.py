"""
Suite de tests complète pour 5GHz Cleaner
Lance tous les tests de sécurité et génère un rapport
"""
import sys
import os
import subprocess

def run_test_file(test_file):
    """Exécute un fichier de test et retourne le résultat"""
    print(f"\n{'='*80}")
    print(f"EXECUTION: {test_file}")
    print('='*80)
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"[FAIL] Test timeout: {test_file}")
        return False
    except Exception as e:
        print(f"[FAIL] Test error: {e}")
        return False

def main():
    """Lance tous les tests"""
    print("\n")
    print("="*80)
    print("SUITE DE TESTS COMPLETE - 5GHz Cleaner v1.6.0")
    print("="*80)
    print()
    
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Liste des tests à exécuter
    test_files = [
        os.path.join(tests_dir, "test_security_core.py"),
        os.path.join(tests_dir, "test_confirmations.py"),
        os.path.join(tests_dir, "test_restore_point.py"),
    ]
    
    results = {}
    
    for test_file in test_files:
        if os.path.exists(test_file):
            test_name = os.path.basename(test_file)
            results[test_name] = run_test_file(test_file)
        else:
            print(f"[WARNING] Test file not found: {test_file}")
    
    # Rapport final
    print("\n")
    print("="*80)
    print("RAPPORT FINAL - TOUS LES TESTS")
    print("="*80)
    print()
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Resultat global: {passed}/{total} suites de tests reussies")
    print()
    
    if passed == total:
        print("="*80)
        print("TOUS LES TESTS SONT PASSES!")
        print("L'application est prete pour la production!")
        print("="*80)
        return 0
    else:
        print("="*80)
        print("CERTAINS TESTS ONT ECHOUE!")
        print("Verifiez les erreurs ci-dessus!")
        print("="*80)
        return 1

if __name__ == "__main__":
    sys.exit(main())
