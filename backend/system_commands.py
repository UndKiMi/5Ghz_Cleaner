"""
Module de commandes système sécurisées
Définit les chemins absolus pour toutes les commandes Windows
"""
import os
import sys
import io
import subprocess
from typing import List, Optional

# Configurer l'encodage UTF-8 pour Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Chemins absolus des commandes système Windows
SYSTEM_ROOT = os.environ.get('SystemRoot', r'C:\Windows')
SYSTEM32 = os.path.join(SYSTEM_ROOT, 'System32')
WBEM = os.path.join(SYSTEM32, 'wbem')

# Commandes système (chemins absolus pour éviter PATH hijacking)
SC_EXE = os.path.join(SYSTEM32, 'sc.exe')
REG_EXE = os.path.join(SYSTEM32, 'reg.exe')
WMIC_EXE = os.path.join(WBEM, 'wmic.exe')

# Commandes optionnelles (peuvent ne pas exister)
NVIDIA_SMI = r'C:\Program Files\NVIDIA Corporation\NVSMI\nvidia-smi.exe'


class SystemCommand:
    """Wrapper sécurisé pour les commandes système"""
    
    @staticmethod
    def run_sc(args: List[str], timeout: int = 5) -> subprocess.CompletedProcess:
        """
        Exécute une commande sc.exe (Service Control)
        
        Args:
            args: Arguments pour sc.exe (ex: ['query', 'wuauserv'])
            timeout: Timeout en secondes
            
        Returns:
            CompletedProcess avec le résultat
        """
        cmd = [SC_EXE] + args
        return subprocess.run(  # nosec B603 - Commande système sécurisée avec chemin absolu
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False
        )
    
    @staticmethod
    def run_reg(args: List[str], timeout: int = 10) -> subprocess.CompletedProcess:
        """
        Exécute une commande reg.exe (Registry Editor)
        
        Args:
            args: Arguments pour reg.exe (ex: ['export', 'HKLM\\...', 'backup.reg'])
            timeout: Timeout en secondes
            
        Returns:
            CompletedProcess avec le résultat
        """
        cmd = [REG_EXE] + args
        return subprocess.run(  # nosec B603 - Commande système sécurisée avec chemin absolu
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False
        )
    
    @staticmethod
    def run_wmic(args: List[str], timeout: int = 5) -> subprocess.CompletedProcess:
        """
        Exécute une commande wmic.exe (Windows Management Instrumentation)
        
        Args:
            args: Arguments pour wmic.exe
            timeout: Timeout en secondes
            
        Returns:
            CompletedProcess avec le résultat
        """
        cmd = [WMIC_EXE] + args
        return subprocess.run(  # nosec B603 - Commande système sécurisée avec chemin absolu
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False
        )
    
    @staticmethod
    def run_nvidia_smi(args: List[str], timeout: int = 5) -> Optional[subprocess.CompletedProcess]:
        """
        Exécute nvidia-smi (si disponible)
        
        Args:
            args: Arguments pour nvidia-smi
            timeout: Timeout en secondes
            
        Returns:
            CompletedProcess ou None si nvidia-smi n'existe pas
        """
        if not os.path.exists(NVIDIA_SMI):
            return None
        
        cmd = [NVIDIA_SMI] + args
        try:
            return subprocess.run(  # nosec B603 - Commande NVIDIA sécurisée avec chemin absolu
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                shell=False
            )
        except (subprocess.SubprocessError, FileNotFoundError):
            return None
    
    @staticmethod
    def verify_commands() -> dict:
        """
        Vérifie que toutes les commandes système existent
        
        Returns:
            Dict avec le statut de chaque commande
        """
        commands = {
            'sc.exe': SC_EXE,
            'reg.exe': REG_EXE,
            'wmic.exe': WMIC_EXE,
            'nvidia-smi.exe': NVIDIA_SMI
        }
        
        status = {}
        for name, path in commands.items():
            status[name] = {
                'path': path,
                'exists': os.path.exists(path),
                'executable': os.access(path, os.X_OK) if os.path.exists(path) else False
            }
        
        return status


# Instance globale
system_cmd = SystemCommand()


if __name__ == "__main__":
    """Test des commandes système"""
    print("="*80)
    print("VÉRIFICATION DES COMMANDES SYSTÈME")
    print("="*80)
    print()
    
    status = SystemCommand.verify_commands()
    
    for cmd, info in status.items():
        exists = "✅" if info['exists'] else "❌"
        print(f"{exists} {cmd}")
        print(f"   Chemin: {info['path']}")
        print(f"   Existe: {info['exists']}")
        print(f"   Exécutable: {info['executable']}")
        print()
    
    # Test sc.exe
    print("="*80)
    print("TEST: sc.exe query wuauserv")
    print("="*80)
    try:
        result = system_cmd.run_sc(['query', 'wuauserv'])
        print(f"Return code: {result.returncode}")
        print(f"Output: {result.stdout[:200]}...")
    except Exception as e:
        print(f"Erreur: {e}")
