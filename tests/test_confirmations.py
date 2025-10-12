"""
Tests pour les confirmations de sécurité
Vérifie que Windows.old et la corbeille nécessitent une confirmation
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import cleaner

def test_windows_old_requires_confirmation():
    """Test que Windows.old nécessite une confirmation"""
    print("="*80)
    print("TEST 1: Windows.old - Confirmation requise")
    print("="*80)
    
    # Appeler sans confirmation
    result = cleaner.clear_windows_old(confirmed=False)
    
    # Vérifier qu'il y a une erreur
    has_error = 'error' in result
    has_warning = 'warning' in result
    not_deleted = result.get('windows_old_deleted', 1) == 0
    
    print(f"Résultat sans confirmation: {result}")
    print(f"  - Erreur présente: {has_error}")
    print(f"  - Warning présent: {has_warning}")
    print(f"  - Non supprimé: {not_deleted}")
    
    success = has_error and has_warning and not_deleted
    
    if success:
        print("\n[OK] Windows.old nécessite bien une confirmation")
    else:
        print("\n[FAIL] Windows.old ne nécessite PAS de confirmation!")
    
    print()
    return success

def test_windows_old_with_confirmation():
    """Test que Windows.old fonctionne avec confirmation"""
    print("="*80)
    print("TEST 2: Windows.old - Avec confirmation")
    print("="*80)
    
    # Appeler avec confirmation
    result = cleaner.clear_windows_old(confirmed=True)
    
    # Vérifier qu'il n'y a pas d'erreur de confirmation
    no_confirmation_error = result.get('error') != 'User confirmation required'
    
    print(f"Résultat avec confirmation: {result}")
    print(f"  - Pas d'erreur de confirmation: {no_confirmation_error}")
    
    if no_confirmation_error:
        print("\n[OK] Windows.old fonctionne avec confirmation")
    else:
        print("\n[FAIL] Windows.old ne fonctionne pas avec confirmation!")
    
    print()
    return no_confirmation_error

def test_recycle_bin_requires_confirmation():
    """Test que la corbeille nécessite une confirmation"""
    print("="*80)
    print("TEST 3: Corbeille - Confirmation requise")
    print("="*80)
    
    # Appeler sans confirmation
    result = cleaner.empty_recycle_bin(confirmed=False)
    
    # Vérifier qu'il y a une erreur
    has_error = 'error' in result
    has_warning = 'warning' in result
    not_deleted = result.get('recycle_bin_deleted', 1) == 0
    
    print(f"Résultat sans confirmation: {result}")
    print(f"  - Erreur présente: {has_error}")
    print(f"  - Warning présent: {has_warning}")
    print(f"  - Non vidée: {not_deleted}")
    
    success = has_error and has_warning and not_deleted
    
    if success:
        print("\n[OK] Corbeille nécessite bien une confirmation")
    else:
        print("\n[FAIL] Corbeille ne nécessite PAS de confirmation!")
    
    print()
    return success

def test_recycle_bin_with_confirmation():
    """Test que la corbeille fonctionne avec confirmation"""
    print("="*80)
    print("TEST 4: Corbeille - Avec confirmation")
    print("="*80)
    
    # Appeler avec confirmation
    result = cleaner.empty_recycle_bin(confirmed=True)
    
    # Vérifier qu'il n'y a pas d'erreur de confirmation
    no_confirmation_error = result.get('error') != 'User confirmation required'
    
    print(f"Résultat avec confirmation: {result}")
    print(f"  - Pas d'erreur de confirmation: {no_confirmation_error}")
    
    if no_confirmation_error:
        print("\n[OK] Corbeille fonctionne avec confirmation")
    else:
        print("\n[FAIL] Corbeille ne fonctionne pas avec confirmation!")
    
    print()
    return no_confirmation_error

def run_all_tests():
    """Exécute tous les tests de confirmation"""
    print("\n")
    print("="*80)
    print("TESTS DE CONFIRMATION - SECURITE")
    print("="*80)
    print()
    
    results = []
    
    results.append(("Windows.old - Confirmation requise", test_windows_old_requires_confirmation()))
    results.append(("Windows.old - Avec confirmation", test_windows_old_with_confirmation()))
    results.append(("Corbeille - Confirmation requise", test_recycle_bin_requires_confirmation()))
    results.append(("Corbeille - Avec confirmation", test_recycle_bin_with_confirmation()))
    
    print("="*80)
    print("RESUME DES TESTS")
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
        print("Les confirmations de securite fonctionnent parfaitement!")
    else:
        print()
        print("CERTAINS TESTS ONT ECHOUE!")
        print("Verifiez les confirmations de securite!")
    
    print("="*80)
    print()
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
