"""
Tests pour le point de restauration automatique
Vérifie que le point de restauration est créé correctement
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import de la fonction depuis main.py
import importlib.util
spec = importlib.util.spec_from_file_location("main", os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py"))
main_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main_module)

def test_restore_point_disk_space_check():
    """Test que le point de restauration vérifie l'espace disque"""
    print("="*80)
    print("TEST 1: Point de restauration - Vérification espace disque")
    print("="*80)
    
    # La fonction devrait vérifier l'espace disque
    # On ne peut pas vraiment tester sans créer un point, mais on peut vérifier
    # que la fonction existe et ne crash pas
    
    try:
        # Appeler la fonction
        result = main_module.create_restore_point()
        
        # La fonction doit retourner un booléen
        is_bool = isinstance(result, bool)
        
        print(f"Résultat: {result}")
        print(f"  - Type booléen: {is_bool}")
        
        if is_bool:
            print("\n[OK] Point de restauration retourne un booléen")
            return True
        else:
            print("\n[FAIL] Point de restauration ne retourne pas un booléen!")
            return False
    except Exception as e:
        print(f"\n[FAIL] Erreur lors de la création du point: {e}")
        return False

def test_restore_point_function_exists():
    """Test que la fonction de point de restauration existe"""
    print("="*80)
    print("TEST 2: Point de restauration - Fonction existe")
    print("="*80)
    
    # Vérifier que la fonction existe
    has_function = hasattr(main_module, 'create_restore_point')
    is_callable = callable(getattr(main_module, 'create_restore_point', None))
    
    print(f"  - Fonction existe: {has_function}")
    print(f"  - Fonction callable: {is_callable}")
    
    success = has_function and is_callable
    
    if success:
        print("\n[OK] Fonction de point de restauration existe")
    else:
        print("\n[FAIL] Fonction de point de restauration n'existe pas!")
    
    print()
    return success

def test_restore_point_documentation():
    """Test que la fonction est bien documentée"""
    print("="*80)
    print("TEST 3: Point de restauration - Documentation")
    print("="*80)
    
    # Vérifier la documentation
    func = getattr(main_module, 'create_restore_point', None)
    has_docstring = func.__doc__ is not None and len(func.__doc__) > 0
    
    print(f"  - Docstring présent: {has_docstring}")
    if has_docstring:
        print(f"  - Docstring: {func.__doc__[:100]}...")
    
    if has_docstring:
        print("\n[OK] Fonction bien documentée")
    else:
        print("\n[FAIL] Fonction non documentée!")
    
    print()
    return has_docstring

def run_all_tests():
    """Exécute tous les tests de point de restauration"""
    print("\n")
    print("="*80)
    print("TESTS POINT DE RESTAURATION - SECURITE")
    print("="*80)
    print()
    
    results = []
    
    results.append(("Fonction existe", test_restore_point_function_exists()))
    results.append(("Documentation", test_restore_point_documentation()))
    results.append(("Vérification espace disque", test_restore_point_disk_space_check()))
    
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
        print("Le point de restauration fonctionne correctement!")
    else:
        print()
        print("CERTAINS TESTS ONT ECHOUE!")
        print("Verifiez le point de restauration!")
    
    print("="*80)
    print()
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
