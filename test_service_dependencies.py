"""
Script de test pour vérifier la fonction de vérification des dépendances de services
"""
from backend.cleaner import (
    get_service_dependencies, 
    check_service_status, 
    stop_services,
    SERVICES_TO_STOP,
    PROTECTED_SERVICES
)

print("="*80)
print("TEST DE VÉRIFICATION DES DÉPENDANCES DE SERVICES")
print("="*80)
print()

# Test 1: Vérifier les services protégés
print("1. SERVICES PROTEGES:")
print("-" * 40)
for service in PROTECTED_SERVICES:
    print(f"  [OK] {service}")
print()

# Test 2: Vérifier les services à arrêter
print("2. SERVICES A ARRETER:")
print("-" * 40)
for service in SERVICES_TO_STOP:
    print(f"  -> {service}")
print()

# Test 3: Vérifier le statut de chaque service
print("3. STATUT DES SERVICES:")
print("-" * 40)
for service in SERVICES_TO_STOP:
    status = check_service_status(service)
    icon = "[RUN]" if status == "RUNNING" else "[STOP]" if status == "STOPPED" else "[???]"
    print(f"  {icon} {service}: {status}")
print()

# Test 4: Vérifier les dépendances
print("4. ANALYSE DES DEPENDANCES:")
print("-" * 40)
for service in SERVICES_TO_STOP:
    deps = get_service_dependencies(service)
    if deps:
        print(f"  [DEPS] {service}:")
        for dep in deps:
            is_protected = "[PROTEGE]" if dep in PROTECTED_SERVICES else "[OK]"
            print(f"     +-- {dep} {is_protected}")
    else:
        print(f"  [OK] {service}: Aucune dependance")
print()

# Test 5: Simulation d'arrêt (dry-run)
print("5. SIMULATION D'ARRET (DRY-RUN):")
print("-" * 40)
print("[INFO] Simulation uniquement - Aucun service ne sera reellement arrete")
print()

# On ne fait que vérifier, sans arrêter
for service in SERVICES_TO_STOP:
    print(f"\nAnalyse de {service}:")
    
    # Vérifier protection
    if service in PROTECTED_SERVICES:
        print(f"  [BLOQUE] Service protege")
        continue
    
    # Vérifier statut
    status = check_service_status(service)
    if status == "STOPPED":
        print(f"  [INFO] Deja arrete")
        continue
    elif status == "UNKNOWN":
        print(f"  [WARN] Service introuvable")
        continue
    
    # Vérifier dépendances
    deps = get_service_dependencies(service)
    if deps:
        protected_deps = [d for d in deps if d in PROTECTED_SERVICES]
        if protected_deps:
            print(f"  [BLOQUE] Dependances protegees detectees")
            print(f"     -> {', '.join(protected_deps)}")
            continue
        else:
            print(f"  [WARN] {len(deps)} dependance(s) non-protegee(s)")
            print(f"     -> {', '.join(deps)}")
    
    print(f"  [OK] Peut etre arrete en toute securite")

print()
print("="*80)
print("TEST TERMINÉ")
print("="*80)
