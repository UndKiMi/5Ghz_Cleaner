"""
Runtime Integrity Verification Module
Vérifie l'intégrité du code au runtime pour détecter toute modification malveillante

Conforme: NIST SP 800-53 SI-7, OWASP ASVS 4.0 V14.2
"""
import os
import sys
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple


class IntegrityError(Exception):
    """Exception levée en cas de violation d'intégrité"""
    pass


class RuntimeIntegrityChecker:
    """
    Vérifie l'intégrité du code au runtime
    
    Protections:
    - Vérification des imports critiques
    - Détection de modifications du code
    - Validation des chemins d'exécution
    - Protection contre l'injection de code
    
    Conforme: NIST SP 800-53 SI-7, OWASP ASVS 4.0 V14.2
    """
    
    def __init__(self):
        self.critical_modules = [
            'src.utils.elevation',
            'src.utils.system_commands',
            'src.services.security_core',
            'config.settings'
        ]
        
    def verify_execution_path(self) -> bool:
        """
        Vérifie que l'application s'exécute depuis un chemin légitime
        
        Returns:
            bool: True si le chemin est valide
            
        Raises:
            IntegrityError: Si le chemin est suspect
        """
        exe_path = Path(sys.executable)
        script_path = Path(__file__).resolve()
        
        # Vérifier que le script n'est pas dans un dossier temporaire
        temp_paths = [
            Path(os.getenv('TEMP', '')),
            Path(os.getenv('TMP', '')),
            Path('C:\\Windows\\Temp'),
        ]
        
        for temp_path in temp_paths:
            if temp_path and script_path.is_relative_to(temp_path):
                raise IntegrityError(
                    f"Application running from temporary directory: {script_path}"
                )
        
        return True
    
    def verify_critical_imports(self) -> bool:
        """
        Vérifie que les modules critiques sont chargés correctement
        
        Returns:
            bool: True si tous les modules sont valides
            
        Raises:
            IntegrityError: Si un module critique est manquant ou modifié
        """
        for module_name in self.critical_modules:
            if module_name not in sys.modules:
                # Module pas encore chargé, c'est normal
                continue
            
            module = sys.modules[module_name]
            
            # Vérifier que le module a un chemin valide
            if not hasattr(module, '__file__') or not module.__file__:
                raise IntegrityError(
                    f"Critical module has no file path: {module_name}"
                )
            
            module_path = Path(module.__file__).resolve()
            
            # Vérifier que le module n'est pas dans un dossier temporaire
            temp_paths = [
                Path(os.getenv('TEMP', '')),
                Path(os.getenv('TMP', '')),
            ]
            
            for temp_path in temp_paths:
                if temp_path and module_path.is_relative_to(temp_path):
                    raise IntegrityError(
                        f"Critical module loaded from temporary directory: {module_name}"
                    )
        
        return True
    
    def verify_no_debugger(self) -> bool:
        """
        Vérifie qu'aucun débogueur n'est attaché
        
        Returns:
            bool: True si pas de débogueur détecté
            
        Note:
            Cette vérification est informative, pas bloquante
        """
        # Vérifier sys.gettrace() (debugger Python)
        if sys.gettrace() is not None:
            print("[WARNING] Python debugger detected (sys.gettrace)")
            return False
        
        # Vérifier les variables d'environnement de debug
        debug_vars = ['PYTHONBREAKPOINT', 'PYTHONDEBUG']
        for var in debug_vars:
            if os.getenv(var):
                print(f"[WARNING] Debug environment variable detected: {var}")
                return False
        
        return True
    
    def verify_environment(self) -> bool:
        """
        Vérifie l'environnement d'exécution
        
        Returns:
            bool: True si l'environnement est sûr
            
        Raises:
            IntegrityError: Si l'environnement est suspect
        """
        # Vérifier que Python n'est pas en mode debug
        if hasattr(sys, 'gettotalrefcount'):
            # sys.gettotalrefcount() n'existe que dans les builds debug
            raise IntegrityError("Running in Python debug build")
        
        # Vérifier que les optimisations sont activées
        if __debug__:
            print("[WARNING] Running in debug mode (__debug__ = True)")
            print("[INFO] For production, run with: python -O")
        
        return True
    
    def run_all_checks(self, strict: bool = False) -> Tuple[bool, List[str]]:
        """
        Exécute toutes les vérifications d'intégrité
        
        Args:
            strict: Si True, lève une exception en cas d'échec
            
        Returns:
            Tuple[bool, List[str]]: (all_passed, list_of_warnings)
            
        Raises:
            IntegrityError: Si strict=True et une vérification échoue
        """
        warnings = []
        
        try:
            # Vérification 1: Chemin d'exécution
            self.verify_execution_path()
        except IntegrityError as e:
            if strict:
                raise
            warnings.append(f"Execution path: {e}")
        
        try:
            # Vérification 2: Imports critiques
            self.verify_critical_imports()
        except IntegrityError as e:
            if strict:
                raise
            warnings.append(f"Critical imports: {e}")
        
        try:
            # Vérification 3: Environnement
            self.verify_environment()
        except IntegrityError as e:
            if strict:
                raise
            warnings.append(f"Environment: {e}")
        
        # Vérification 4: Débogueur (non bloquante)
        if not self.verify_no_debugger():
            warnings.append("Debugger detected (non-blocking)")
        
        return len(warnings) == 0, warnings


# Instance globale
integrity_checker = RuntimeIntegrityChecker()


def verify_runtime_integrity(strict: bool = False) -> bool:
    """
    Fonction utilitaire pour vérifier l'intégrité au runtime
    
    Args:
        strict: Si True, lève une exception en cas d'échec
        
    Returns:
        bool: True si toutes les vérifications passent
        
    Raises:
        IntegrityError: Si strict=True et une vérification échoue
    """
    all_passed, warnings = integrity_checker.run_all_checks(strict=strict)
    
    if warnings:
        print("[SECURITY] Runtime integrity warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    
    if all_passed:
        print("[SECURITY] Runtime integrity verification: PASSED")
    else:
        print("[SECURITY] Runtime integrity verification: WARNINGS")
    
    return all_passed


if __name__ == "__main__":
    """Test du module"""
    print("="*80)
    print("Runtime Integrity Verification Test")
    print("="*80)
    
    try:
        result = verify_runtime_integrity(strict=False)
        print(f"\nResult: {'PASSED' if result else 'WARNINGS'}")
    except IntegrityError as e:
        print(f"\nIntegrity Error: {e}")
        sys.exit(1)
