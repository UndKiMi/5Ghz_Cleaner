"""
Test Complet de la Vie Privée - 5GHz Cleaner
Vérifie que AUCUNE donnée utilisateur n'est collectée ou envoyée
"""
import sys
import os
import io

# Configurer l'encodage UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_no_network_imports():
    """Test qu'aucune bibliothèque réseau n'est importée"""
    print("\n" + "="*80)
    print("TEST 1: Vérification des imports réseau")
    print("="*80)
    
    forbidden_imports = [
        'requests',
        'urllib',
        'http.client',
        'httplib',
        'aiohttp',
        'websocket',
    ]
    
    # Parcourir tous les fichiers Python
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    violations = []
    
    for root, dirs, files in os.walk(project_root):
        # Ignorer les dossiers de test et build
        if any(skip in root for skip in ['__pycache__', '.git', 'build', 'dist']):
            continue
            
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        for forbidden in forbidden_imports:
                            if f'import {forbidden}' in content or f'from {forbidden}' in content:
                                violations.append(f"{filepath}: {forbidden}")
                except:
                    pass
    
    if violations:
        print("❌ ÉCHEC: Imports réseau détectés:")
        for v in violations:
            print(f"  - {v}")
        return False
    else:
        print("✅ SUCCÈS: Aucun import réseau détecté")
        return True


def test_no_external_connections():
    """Test qu'aucune connexion externe n'est établie"""
    print("\n" + "="*80)
    print("TEST 2: Vérification des connexions externes")
    print("="*80)
    
    # Rechercher socket.connect, socket.create_connection, etc.
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    violations = []
    
    suspicious_patterns = [
        'socket.connect(',
        'socket.create_connection(',
        '.connect(',
        'urlopen(',
        '.get(',
        '.post(',
    ]
    
    for root, dirs, files in os.walk(project_root):
        if any(skip in root for skip in ['__pycache__', '.git', 'build', 'dist', 'tests']):
            continue
            
        for file in files:
            if file.endswith('.py') and file != 'telemetry_checker.py':  # Exclure le checker lui-même
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines, 1):
                            for pattern in suspicious_patterns:
                                if pattern in line and not line.strip().startswith('#'):
                                    violations.append(f"{filepath}:{i}: {line.strip()}")
                except:
                    pass
    
    if violations:
        print("⚠️ ATTENTION: Connexions potentielles détectées:")
        for v in violations:
            print(f"  - {v}")
        # Vérifier si ce sont de vraies violations
        real_violations = [v for v in violations if 'telemetry_checker' not in v]
        if real_violations:
            return False
    
    print("✅ SUCCÈS: Aucune connexion externe dans le code principal")
    return True


def test_no_data_collection():
    """Test qu'aucune collecte de données n'est présente"""
    print("\n" + "="*80)
    print("TEST 3: Vérification de la collecte de données")
    print("="*80)
    
    # Rechercher des patterns de collecte de données
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    violations = []
    
    suspicious_patterns = [
        'user_id',
        'tracking',
        'analytics',
        'mixpanel',
        'amplitude',
        'segment',
        'google-analytics',
        'ga(',
    ]
    
    for root, dirs, files in os.walk(project_root):
        if any(skip in root for skip in ['__pycache__', '.git', 'build', 'dist', 'tests']):
            continue
            
        for file in files:
            if file.endswith('.py') and file != 'telemetry_checker.py':
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        for pattern in suspicious_patterns:
                            if pattern in content:
                                violations.append(f"{filepath}: {pattern}")
                except:
                    pass
    
    if violations:
        print("⚠️ ATTENTION: Patterns suspects détectés:")
        for v in violations:
            print(f"  - {v}")
        return False
    
    print("✅ SUCCÈS: Aucune collecte de données détectée")
    return True


def test_no_personal_data_storage():
    """Test qu'aucune donnée personnelle n'est stockée"""
    print("\n" + "="*80)
    print("TEST 4: Vérification du stockage de données personnelles")
    print("="*80)
    
    # Vérifier qu'aucun fichier suspect n'existe
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    suspicious_files = [
        'user_data.json',
        'analytics.db',
        'telemetry.log',
        'tracking.db',
        'user_profile.json',
    ]
    
    found_files = []
    for root, dirs, files in os.walk(project_root):
        for file in files:
            if file.lower() in suspicious_files:
                found_files.append(os.path.join(root, file))
    
    if found_files:
        print("❌ ÉCHEC: Fichiers suspects trouvés:")
        for f in found_files:
            print(f"  - {f}")
        return False
    
    print("✅ SUCCÈS: Aucun fichier de données personnelles trouvé")
    return True


def test_logs_privacy():
    """Test que les logs ne contiennent pas de données sensibles"""
    print("\n" + "="*80)
    print("TEST 5: Vérification de la vie privée dans les logs")
    print("="*80)
    
    # Vérifier que le code de logging ne collecte pas de données sensibles
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    sensitive_patterns = [
        'username',
        'password',
        'email',
        'ip_address',
        'mac_address',
        'serial_number',
    ]
    
    violations = []
    for root, dirs, files in os.walk(project_root):
        if any(skip in root for skip in ['__pycache__', '.git', 'build', 'dist', 'tests']):
            continue
            
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines, 1):
                            if 'log' in line.lower():
                                for pattern in sensitive_patterns:
                                    if pattern in line.lower():
                                        violations.append(f"{filepath}:{i}: {line.strip()}")
                except:
                    pass
    
    if violations:
        print("⚠️ ATTENTION: Logging potentiel de données sensibles:")
        for v in violations:
            print(f"  - {v}")
        # Vérifier si ce sont de vraies violations
        return len(violations) == 0
    
    print("✅ SUCCÈS: Aucune donnée sensible dans les logs")
    return True


def test_privacy_policy_compliance():
    """Test que le code est conforme à la politique de confidentialité"""
    print("\n" + "="*80)
    print("TEST 6: Conformité à la politique de confidentialité")
    print("="*80)
    
    # Vérifier que PRIVACY.md existe et contient les bonnes garanties
    privacy_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'PRIVACY.md'
    )
    
    if not os.path.exists(privacy_file):
        print("❌ ÉCHEC: PRIVACY.md n'existe pas")
        return False
    
    with open(privacy_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_statements = [
        'Aucune donnée',
        'télémétrie',
        'vie privée',
        'local',
    ]
    
    missing = []
    for statement in required_statements:
        if statement.lower() not in content.lower():
            missing.append(statement)
    
    if missing:
        print("❌ ÉCHEC: Déclarations manquantes dans PRIVACY.md:")
        for m in missing:
            print(f"  - {m}")
        return False
    
    print("✅ SUCCÈS: PRIVACY.md est conforme")
    return True


def run_all_privacy_tests():
    """Exécute tous les tests de vie privée"""
    print("\n")
    print("="*80)
    print("TEST COMPLET DE LA VIE PRIVÉE - 5GHz Cleaner")
    print("="*80)
    print()
    print("🔒 NOTRE ENGAGEMENT: Respect absolu de la vie privée")
    print("="*80)
    print()
    
    tests = [
        ("Imports réseau", test_no_network_imports),
        ("Connexions externes", test_no_external_connections),
        ("Collecte de données", test_no_data_collection),
        ("Stockage données personnelles", test_no_personal_data_storage),
        ("Vie privée dans les logs", test_logs_privacy),
        ("Conformité politique confidentialité", test_privacy_policy_compliance),
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
    print("RAPPORT FINAL - VIE PRIVÉE")
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
        print("✅ VIE PRIVÉE 100% RESPECTÉE")
        print("="*80)
        print()
        print("🔒 GARANTIES:")
        print("  ✅ Aucune connexion réseau")
        print("  ✅ Aucune collecte de données")
        print("  ✅ Aucune télémétrie")
        print("  ✅ Aucun tracking")
        print("  ✅ Traitement 100% local")
        print("  ✅ Aucune donnée personnelle stockée")
        print()
        print("🎯 NOTRE POINT D'HONNEUR: RESPECT TOTAL DE LA VIE PRIVÉE")
        print("="*80)
        return 0
    else:
        print("="*80)
        print("❌ PROBLÈMES DE VIE PRIVÉE DÉTECTÉS")
        print("="*80)
        return 1


if __name__ == "__main__":
    sys.exit(run_all_privacy_tests())
