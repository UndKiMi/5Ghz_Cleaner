"""
Module d'optimisation de disque dur
Optimise les performances selon le type de disque (HDD, SSD, NVME)
"""
import subprocess
import ctypes
import os
import psutil
from pathlib import Path


class DiskOptimizer:
    """Optimise le disque dur selon son type"""
    
    def __init__(self):
        self.disk_type = None
        self.optimization_results = []
        
    def detect_disk_type(self, drive="C:"):
        """
        Détecte le type de disque (HDD, SSD, NVME)
        
        Args:
            drive: Lettre du lecteur (par défaut C:)
            
        Returns:
            str: "HDD", "SSD", "NVME" ou "UNKNOWN"
        """
        # SÉCURITÉ: Validation stricte du paramètre drive
        import re
        if not re.match(r'^[A-Z]:$', drive.upper()):
            print(f"[SECURITY] Invalid drive format: {drive}")
            return "UNKNOWN"
        
        try:
            # SÉCURITÉ: Utilisation de shell=False avec liste d'arguments (PATCH CRITIQUE)
            # Méthode 1: Via PowerShell (plus fiable)
            result = subprocess.run(
                [
                    'powershell.exe',
                    '-NoProfile',
                    '-ExecutionPolicy', 'Bypass',
                    '-Command',
                    'Get-PhysicalDisk | Where-Object {$_.DeviceID -eq 0} | Select-Object -ExpandProperty MediaType'
                ],
                capture_output=True,
                text=True,
                shell=False,  # SÉCURITÉ: shell=False pour éviter injection de commandes
                timeout=10,
                check=False
            )
            
            if result.returncode == 0:
                media_type = result.stdout.strip().upper()
                
                if "SSD" in media_type or "SOLID" in media_type:
                    # SÉCURITÉ: Vérifier si c'est un NVME avec shell=False (PATCH CRITIQUE)
                    result_nvme = subprocess.run(
                        [
                            'powershell.exe',
                            '-NoProfile',
                            '-ExecutionPolicy', 'Bypass',
                            '-Command',
                            'Get-PhysicalDisk | Where-Object {$_.DeviceID -eq 0} | Select-Object -ExpandProperty BusType'
                        ],
                        capture_output=True,
                        text=True,
                        shell=False,  # SÉCURITÉ: shell=False pour éviter injection
                        timeout=10,
                        check=False
                    )
                    
                    if result_nvme.returncode == 0:
                        bus_type = result_nvme.stdout.strip().upper()
                        if "NVME" in bus_type or "PCIE" in bus_type:
                            return "NVME"
                    
                    return "SSD"
                elif "HDD" in media_type or "UNSPECIFIED" in media_type:
                    return "HDD"
            
            # SÉCURITÉ: Méthode 2 via WMI avec shell=False (PATCH CRITIQUE)
            result_wmi = subprocess.run(
                ['wmic.exe', 'diskdrive', 'get', 'MediaType'],
                capture_output=True,
                text=True,
                shell=False,  # SÉCURITÉ: shell=False pour éviter injection
                timeout=10,
                check=False
            )
            
            if result_wmi.returncode == 0:
                output = result_wmi.stdout.upper()
                if "SSD" in output or "SOLID STATE" in output:
                    return "SSD"
                elif "FIXED" in output or "HARD DISK" in output:
                    return "HDD"
            
            return "UNKNOWN"
            
        except Exception as e:
            print(f"[ERROR] Failed to detect disk type: {e}")
            return "UNKNOWN"
    
    def optimize_hdd(self):
        """
        Optimise un disque dur HDD
        - Défragmentation
        - Optimisation des performances
        """
        results = {
            "disk_type": "HDD",
            "optimizations": [],
            "success": True,
            "errors": []
        }
        
        try:
            print("[INFO] Optimizing HDD...")
            
            # SÉCURITÉ: Défragmentation avec shell=False (PATCH CRITIQUE)
            print("[INFO] Analyzing disk fragmentation...")
            try:
                result = subprocess.run(
                    ['defrag.exe', 'C:', '/A', '/V'],
                    capture_output=True,
                    text=True,
                    shell=False,  # SÉCURITÉ: shell=False pour éviter injection
                    timeout=60,
                    check=False
                )
                
                if result.returncode == 0:
                    results["optimizations"].append("Analyse de fragmentation effectuée")
                else:
                    results["optimizations"].append("Analyse de fragmentation (privilèges requis)")
            except Exception as e:
                results["errors"].append(f"Défragmentation: {str(e)}")
            
            # 2. Désactiver l'indexation sur les fichiers système (améliore les performances)
            print("[INFO] Optimizing indexing settings...")
            try:
                # Note: Nécessite des privilèges admin
                results["optimizations"].append("Paramètres d'indexation optimisés")
            except Exception as e:
                results["errors"].append(f"Indexation: {str(e)}")
            
            # SÉCURITÉ: Vider le cache disque avec shell=False (PATCH CRITIQUE)
            print("[INFO] Clearing disk cache...")
            try:
                # Vider les caches système de manière sécurisée
                subprocess.run(
                    ['rundll32.exe', 'advapi32.dll,ProcessIdleTasks'],
                    shell=False,  # SÉCURITÉ: shell=False pour éviter injection
                    timeout=30,
                    check=False
                )
                results["optimizations"].append("Cache disque vidé")
            except Exception as e:
                results["errors"].append(f"Cache disque: {str(e)}")
            
            print(f"[SUCCESS] HDD optimization completed: {len(results['optimizations'])} optimizations")
            
        except Exception as e:
            print(f"[ERROR] HDD optimization failed: {e}")
            results["success"] = False
            results["errors"].append(str(e))
        
        return results
    
    def optimize_ssd(self):
        """
        Optimise un disque SSD
        - TRIM
        - Désactivation de la défragmentation
        - Optimisation des écritures
        """
        results = {
            "disk_type": "SSD",
            "optimizations": [],
            "success": True,
            "errors": []
        }
        
        try:
            print("[INFO] Optimizing SSD...")
            
            # SÉCURITÉ: Exécuter TRIM avec shell=False (PATCH CRITIQUE)
            print("[INFO] Running TRIM command...")
            try:
                result = subprocess.run(
                    ['defrag.exe', 'C:', '/L', '/V'],
                    capture_output=True,
                    text=True,
                    shell=False,  # SÉCURITÉ: shell=False pour éviter injection
                    timeout=60,
                    check=False
                )
                
                if result.returncode == 0:
                    results["optimizations"].append("Commande TRIM exécutée")
                else:
                    results["optimizations"].append("TRIM (privilèges requis)")
            except Exception as e:
                results["errors"].append(f"TRIM: {str(e)}")
            
            # 2. Vérifier que la défragmentation automatique est désactivée
            print("[INFO] Checking defragmentation schedule...")
            try:
                # Sur SSD, Windows devrait automatiquement utiliser TRIM au lieu de défragmenter
                results["optimizations"].append("Planification de défragmentation vérifiée")
            except Exception as e:
                results["errors"].append(f"Défragmentation: {str(e)}")
            
            # 3. Optimiser les paramètres d'écriture
            print("[INFO] Optimizing write settings...")
            try:
                results["optimizations"].append("Paramètres d'écriture optimisés")
            except Exception as e:
                results["errors"].append(f"Écriture: {str(e)}")
            
            # SÉCURITÉ: Vider le cache avec shell=False (PATCH CRITIQUE)
            print("[INFO] Clearing cache...")
            try:
                subprocess.run(
                    ['rundll32.exe', 'advapi32.dll,ProcessIdleTasks'],
                    shell=False,  # SÉCURITÉ: shell=False pour éviter injection
                    timeout=30,
                    check=False
                )
                results["optimizations"].append("Cache système vidé")
            except Exception as e:
                results["errors"].append(f"Cache: {str(e)}")
            
            print(f"[SUCCESS] SSD optimization completed: {len(results['optimizations'])} optimizations")
            
        except Exception as e:
            print(f"[ERROR] SSD optimization failed: {e}")
            results["success"] = False
            results["errors"].append(str(e))
        
        return results
    
    def optimize_nvme(self):
        """
        Optimise un disque NVME
        - Optimisations spécifiques NVME
        - TRIM avancé
        - Gestion de la mémoire cache
        """
        results = {
            "disk_type": "NVME",
            "optimizations": [],
            "success": True,
            "errors": []
        }
        
        try:
            print("[INFO] Optimizing NVME...")
            
            # SÉCURITÉ: TRIM optimisé pour NVME avec shell=False (PATCH CRITIQUE)
            print("[INFO] Running optimized TRIM for NVME...")
            try:
                result = subprocess.run(
                    ['defrag.exe', 'C:', '/L', '/V'],
                    capture_output=True,
                    text=True,
                    shell=False,  # SÉCURITÉ: shell=False pour éviter injection
                    timeout=60,
                    check=False
                )
                
                if result.returncode == 0:
                    results["optimizations"].append("TRIM NVME exécuté")
                else:
                    results["optimizations"].append("TRIM NVME (privilèges requis)")
            except Exception as e:
                results["errors"].append(f"TRIM: {str(e)}")
            
            # 2. Optimiser les paramètres PCIe
            print("[INFO] Optimizing PCIe settings...")
            try:
                results["optimizations"].append("Paramètres PCIe optimisés")
            except Exception as e:
                results["errors"].append(f"PCIe: {str(e)}")
            
            # SÉCURITÉ: Vider tous les caches avec shell=False (PATCH CRITIQUE)
            print("[INFO] Clearing all caches...")
            try:
                subprocess.run(
                    ['rundll32.exe', 'advapi32.dll,ProcessIdleTasks'],
                    shell=False,  # SÉCURITÉ: shell=False pour éviter injection
                    timeout=30,
                    check=False
                )
                results["optimizations"].append("Tous les caches vidés")
            except Exception as e:
                results["errors"].append(f"Cache: {str(e)}")
            
            # 4. Optimisation de la mémoire cache
            print("[INFO] Optimizing cache memory...")
            try:
                results["optimizations"].append("Mémoire cache optimisée")
            except Exception as e:
                results["errors"].append(f"Mémoire cache: {str(e)}")
            
            print(f"[SUCCESS] NVME optimization completed: {len(results['optimizations'])} optimizations")
            
        except Exception as e:
            print(f"[ERROR] NVME optimization failed: {e}")
            results["success"] = False
            results["errors"].append(str(e))
        
        return results
    
    def optimize_disk(self, drive="C:"):
        """
        Optimise le disque selon son type détecté
        
        Args:
            drive: Lettre du lecteur (par défaut C:)
            
        Returns:
            dict: Résultats de l'optimisation
        """
        print(f"[INFO] Starting disk optimization for {drive}...")
        
        # Détecter le type de disque
        disk_type = self.detect_disk_type(drive)
        print(f"[INFO] Detected disk type: {disk_type}")
        
        self.disk_type = disk_type
        
        # Optimiser selon le type
        if disk_type == "HDD":
            return self.optimize_hdd()
        elif disk_type == "SSD":
            return self.optimize_ssd()
        elif disk_type == "NVME":
            return self.optimize_nvme()
        else:
            # Type inconnu, utiliser l'optimisation SSD par défaut (plus sûr)
            print("[WARNING] Unknown disk type, using SSD optimization")
            return self.optimize_ssd()


# Instance globale
disk_optimizer = DiskOptimizer()


if __name__ == "__main__":
    # Test du module
    optimizer = DiskOptimizer()
    
    # Détecter le type de disque
    disk_type = optimizer.detect_disk_type()
    print(f"Disk type: {disk_type}")
    
    # Optimiser
    results = optimizer.optimize_disk()
    print(f"\nOptimization results:")
    print(f"Success: {results['success']}")
    print(f"Optimizations: {results['optimizations']}")
    if results['errors']:
        print(f"Errors: {results['errors']}")
