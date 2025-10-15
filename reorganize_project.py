"""
Script de réorganisation complète du projet 5GHz Cleaner
- Supprime fichiers obsolètes
- Nettoie __pycache__
- Crée structure manquante
- Teste compatibilité
- Génère rapport
"""
import os
import shutil
import sys
from pathlib import Path
import importlib.util

class ProjectReorganizer:
    """Réorganise et nettoie le projet"""
    
    def __init__(self):
        self.root = Path(__file__).parent
        self.report = {
            "deleted": [],
            "created": [],
            "errors": [],
            "warnings": []
        }
    
    def clean_pycache(self):
        """Supprime tous les __pycache__"""
        print("\n[1/7] Nettoyage des __pycache__...")
        count = 0
        for pycache in self.root.rglob("__pycache__"):
            try:
                shutil.rmtree(pycache)
                self.report["deleted"].append(str(pycache.relative_to(self.root)))
                count += 1
            except Exception as e:
                self.report["errors"].append(f"Failed to delete {pycache}: {e}")
        print(f"   OK {count} dossiers __pycache__ supprimes")
    
    def remove_obsolete_files(self):
        """Supprime fichiers obsolètes"""
        print("\n[2/7] Suppression des fichiers obsolètes...")
        obsolete = [
            "clean_project.py",
            "cleanup_project.py",
            "CORRECTIONS_APPLIQUEES.md",
        ]
        count = 0
        for file in obsolete:
            file_path = self.root / file
            if file_path.exists():
                try:
                    file_path.unlink()
                    self.report["deleted"].append(file)
                    count += 1
                    print(f"   OK Supprime: {file}")
                except Exception as e:
                    self.report["errors"].append(f"Failed to delete {file}: {e}")
        print(f"   OK {count} fichiers obsoletes supprimes")
    
    def create_missing_structure(self):
        """Crée structure manquante"""
        print("\n[3/7] Création de la structure manquante...")
        
        # Créer dossiers
        dirs_to_create = [
            "tests",
            "docs",
            "docs/source",
        ]
        
        for dir_name in dirs_to_create:
            dir_path = self.root / dir_name
            if not dir_path.exists():
                dir_path.mkdir(parents=True)
                self.report["created"].append(dir_name + "/")
                print(f"   OK Cree: {dir_name}/")
        
        # Créer __init__.py dans tests
        tests_init = self.root / "tests" / "__init__.py"
        if not tests_init.exists():
            tests_init.touch()
            self.report["created"].append("tests/__init__.py")
            print(f"   OK Cree: tests/__init__.py")
    
    def create_gitignore(self):
        """Crée .gitignore"""
        print("\n[4/7] Création de .gitignore...")
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
.eggs/

# Tests
.pytest_cache/
.coverage
htmlcov/
.tox/

# IDE
.vscode/
.idea/
*.swp

# Logs
*.log
logs/

# Encryption
.encryption_key
*.enc

# OS
.DS_Store
Thumbs.db
desktop.ini

# Temporary
*.tmp
*.bak
~*

# Build
*.spec
"""
        gitignore_path = self.root / ".gitignore"
        try:
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
            self.report["created"].append(".gitignore")
            print("   OK .gitignore cree")
        except Exception as e:
            self.report["errors"].append(f"Failed to create .gitignore: {e}")
    
    def create_pytest_ini(self):
        """Crée pytest.ini"""
        print("\n[5/7] Création de pytest.ini...")
        pytest_content = """[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --cov=backend
    --cov=frontend
    --cov-report=html
    --cov-report=term-missing
    --tb=short
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
"""
        pytest_path = self.root / "pytest.ini"
        try:
            with open(pytest_path, 'w', encoding='utf-8') as f:
                f.write(pytest_content)
            self.report["created"].append("pytest.ini")
            print("   OK pytest.ini cree")
        except Exception as e:
            self.report["errors"].append(f"Failed to create pytest.ini: {e}")
    
    def test_imports(self):
        """Teste tous les imports critiques"""
        print("\n[6/7] Test des imports...")
        
        critical_modules = [
            "config.settings",
            "backend.cleaner",
            "backend.security_core",
            "backend.logger",
            "backend.signature_manager",
            "backend.system_commands",
            "backend.elevation",
            "backend.dry_run",
            "backend.telemetry_checker",
            "frontend.app",
        ]
        
        success = 0
        for module_name in critical_modules:
            try:
                spec = importlib.util.find_spec(module_name)
                if spec is not None:
                    print(f"   OK {module_name}")
                    success += 1
                else:
                    print(f"   ERREUR {module_name} - Not found")
                    self.report["errors"].append(f"Module not found: {module_name}")
            except Exception as e:
                print(f"   ERREUR {module_name} - {e}")
                self.report["errors"].append(f"Import error {module_name}: {e}")
        
        print(f"\n   Résultat: {success}/{len(critical_modules)} modules OK")
        
        if success == len(critical_modules):
            print("   SUCCES Tous les imports fonctionnent parfaitement!")
        else:
            self.report["warnings"].append(f"Seulement {success}/{len(critical_modules)} modules importables")
    
    def generate_report(self):
        """Génère rapport final"""
        print("\n[7/7] Génération du rapport...")
        print("\n" + "="*70)
        print("RAPPORT DE RÉORGANISATION")
        print("="*70)
        
        print(f"\nFichiers/dossiers supprimes: {len(self.report['deleted'])}")
        for item in self.report['deleted']:
            print(f"   - {item}")
        
        print(f"\nFichiers/dossiers crees: {len(self.report['created'])}")
        for item in self.report['created']:
            print(f"   - {item}")
        
        if self.report['errors']:
            print(f"\nErreurs ({len(self.report['errors'])}):")
            for error in self.report['errors']:
                print(f"   - {error}")
        
        if self.report['warnings']:
            print(f"\nAvertissements ({len(self.report['warnings'])}):")
            for warning in self.report['warnings']:
                print(f"   - {warning}")
        
        print("\n" + "="*70)
        
        if not self.report['errors']:
            print("OK REORGANISATION TERMINEE AVEC SUCCES")
            print("\nPROCHAINES ETAPES:")
            print("   1. Remplir backend/file_scanner.py avec le code fourni")
            print("   2. Creer backend/security_auditor.py avec le code fourni")
            print("   3. Creer les fichiers de tests dans tests/")
            print("   4. Generer nouvelle signature: py backend/signature_manager.py")
            print("   5. Tester l'application: py main.py")
        else:
            print("ATTENTION REORGANISATION TERMINEE AVEC ERREURS")
            print("   Veuillez corriger les erreurs ci-dessus")
        print("="*70)
    
    def run(self):
        """Exécute la réorganisation complète"""
        print("="*70)
        print("REORGANISATION DU PROJET - 5GH'z CLEANER")
        print("="*70)
        print("\nATTENTION: Cette operation va supprimer des fichiers!")
        print("   Assurez-vous d'avoir une sauvegarde si necessaire.")
        print("\nDemarrage dans 3 secondes...")
        
        import time
        time.sleep(3)
        
        self.clean_pycache()
        self.remove_obsolete_files()
        self.create_missing_structure()
        self.create_gitignore()
        self.create_pytest_ini()
        self.test_imports()
        self.generate_report()

if __name__ == "__main__":
    reorganizer = ProjectReorganizer()
    reorganizer.run()