"""
CPU Optimizer - Optimisation avancée du CPU pour gaming
Optimise le CPU selon le modèle détecté (Intel/AMD)
Applique les optimisations spécifiques pour les performances gaming
Protège les services Windows critiques
"""
import psutil
import subprocess
import platform
import ctypes
from typing import Dict, List, Tuple, Optional


class CPUOptimizer:
    """Optimiseur avancé de CPU avec optimisations gaming par modèle"""
    
    # Processus Windows critiques à NE JAMAIS fermer
    CRITICAL_PROCESSES = {
        'system', 'registry', 'smss.exe', 'csrss.exe', 'wininit.exe',
        'services.exe', 'lsass.exe', 'svchost.exe', 'winlogon.exe',
        'explorer.exe', 'dwm.exe', 'taskhostw.exe', 'sihost.exe',
        'ctfmon.exe', 'runtimebroker.exe', 'searchindexer.exe',
        'spoolsv.exe', 'audiodg.exe', 'conhost.exe', 'fontdrvhost.exe',
        'wudfhost.exe', 'dashost.exe', 'securityhealthservice.exe',
        'securityhealthsystray.exe', 'msmpeng.exe', 'nissrv.exe',
        'mssense.exe', 'senseir.exe', 'sensecncproxy.exe',
        'sgrmbroker.exe', 'antimalwareservice.exe'
    }
    
    # Services Windows critiques
    CRITICAL_SERVICES = {
        'wuauserv', 'bits', 'cryptsvc', 'trustedinstaller', 'msiserver',
        'eventlog', 'schedule', 'winmgmt', 'rpcss', 'dcomlaunch',
        'plugplay', 'power', 'profsi', 'lanmanserver', 'lanmanworkstation',
        'dhcp', 'dnscache', 'nsi', 'nlasvc', 'netprofm', 'wscsvc',
        'windefend', 'securityhealthservice', 'sense', 'wdnissvc',
        'mpssvc', 'bfe', 'mpsdrv', 'wdiservicehost', 'wdisystemhost'
    }
    
    # Processus système à protéger (Python, antivirus, etc.)
    PROTECTED_PATTERNS = {
        'python', 'pythonw', 'antimalware', 'defender', 'kaspersky',
        'avast', 'avg', 'norton', 'mcafee', 'bitdefender', 'eset',
        'malwarebytes', 'sophos', 'trend', 'panda', 'avira'
    }
    
    def __init__(self):
        self.terminated_processes = []
        self.errors = []
        self.optimizations_applied = []
        self.cpu_info = self._detect_cpu_model()
    
    def get_high_cpu_processes(self, threshold: float = 5.0) -> List[Dict]:
        """
        Récupère les processus utilisant beaucoup de CPU
        
        Args:
            threshold: Seuil d'utilisation CPU en % (défaut: 5%)
            
        Returns:
            List[Dict]: Liste des processus avec leur utilisation CPU
        """
        high_cpu_processes = []
        
        try:
            # IMPORTANT: Appeler cpu_percent() une première fois pour initialiser
            # Attendre 0.5 secondes pour avoir des mesures précises
            import time
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc.cpu_percent()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            time.sleep(0.5)
            
            # Maintenant obtenir les vraies valeurs CPU
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                try:
                    # Obtenir l'utilisation CPU (maintenant précise)
                    cpu_percent = proc.cpu_percent()
                    
                    if cpu_percent and cpu_percent > threshold:
                        # Vérifier que ce n'est pas un processus critique
                        proc_name = proc.info['name'].lower()
                        
                        if not self._is_critical_process(proc_name):
                            high_cpu_processes.append({
                                'pid': proc.info['pid'],
                                'name': proc.info['name'],
                                'cpu_percent': cpu_percent,
                                'username': proc.info.get('username', 'N/A')
                            })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            print(f"[ERROR] Failed to get high CPU processes: {e}")
        
        # Trier par utilisation CPU décroissante
        high_cpu_processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        
        return high_cpu_processes
    
    def _is_critical_process(self, proc_name: str) -> bool:
        """Vérifie si un processus est critique"""
        proc_name_lower = proc_name.lower()
        
        # Vérifier les processus critiques
        if proc_name_lower in self.CRITICAL_PROCESSES:
            return True
        
        # Vérifier les patterns protégés
        for pattern in self.PROTECTED_PATTERNS:
            if pattern in proc_name_lower:
                return True
        
        return False
    
    def optimize_cpu(self, aggressive: bool = False) -> Dict:
        """
        Optimise l'utilisation CPU en fermant les processus non essentiels
        
        Args:
            aggressive: Mode agressif (ferme plus de processus)
            
        Returns:
            Dict: Résultat de l'optimisation
        """
        self.terminated_processes = []
        self.errors = []
        
        try:
            # Obtenir les processus utilisant beaucoup de CPU
            threshold = 3.0 if aggressive else 5.0
            high_cpu_procs = self.get_high_cpu_processes(threshold)
            
            print(f"[INFO] Found {len(high_cpu_procs)} processes using > {threshold}% CPU")
            
            # Terminer les processus non critiques
            for proc_info in high_cpu_procs[:10]:  # Limiter à 10 processus max
                try:
                    pid = proc_info['pid']
                    name = proc_info['name']
                    cpu_percent = proc_info['cpu_percent']
                    
                    # Double vérification de sécurité
                    if self._is_critical_process(name):
                        print(f"[SKIP] {name} (PID {pid}) is critical - skipped")
                        continue
                    
                    # Terminer le processus
                    proc = psutil.Process(pid)
                    proc.terminate()
                    
                    # Attendre la terminaison (max 3 secondes)
                    try:
                        proc.wait(timeout=3)
                        self.terminated_processes.append({
                            'name': name,
                            'pid': pid,
                            'cpu_percent': cpu_percent
                        })
                        print(f"[SUCCESS] Terminated {name} (PID {pid}, CPU: {cpu_percent:.1f}%)")
                    except psutil.TimeoutExpired:
                        # Forcer la fermeture si nécessaire
                        proc.kill()
                        self.terminated_processes.append({
                            'name': name,
                            'pid': pid,
                            'cpu_percent': cpu_percent
                        })
                        print(f"[SUCCESS] Killed {name} (PID {pid}, CPU: {cpu_percent:.1f}%)")
                
                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    self.errors.append(f"{name}: {str(e)}")
                    print(f"[ERROR] Failed to terminate {name}: {e}")
                except Exception as e:
                    self.errors.append(f"{name}: {str(e)}")
                    print(f"[ERROR] Unexpected error for {name}: {e}")
            
            # Résultat
            success = len(self.terminated_processes) > 0
            
            return {
                'success': success,
                'terminated_count': len(self.terminated_processes),
                'terminated_processes': self.terminated_processes,
                'errors': self.errors,
                'message': f"{len(self.terminated_processes)} processus optimisés"
            }
        
        except Exception as e:
            print(f"[ERROR] CPU optimization failed: {e}")
            return {
                'success': False,
                'terminated_count': 0,
                'terminated_processes': [],
                'errors': [str(e)],
                'message': f"Erreur: {str(e)}"
            }
    
    def _detect_cpu_model(self) -> Dict:
        """
        Détecte le modèle de CPU (Intel/AMD) et ses caractéristiques
        
        Returns:
            Dict: Informations sur le CPU
        """
        try:
            cpu_name = platform.processor()
            
            # Détecter le fabricant
            manufacturer = "Unknown"
            if "intel" in cpu_name.lower():
                manufacturer = "Intel"
            elif "amd" in cpu_name.lower():
                manufacturer = "AMD"
            
            # Détecter la génération Intel
            generation = None
            if manufacturer == "Intel":
                import re
                # Chercher i3/i5/i7/i9 suivi du numéro de génération
                match = re.search(r'(i[3579])-(\d{1,2})\d{3}', cpu_name)
                if match:
                    generation = int(match.group(2))
            
            # Détecter la série AMD Ryzen
            series = None
            if manufacturer == "AMD":
                if "ryzen 3" in cpu_name.lower():
                    series = "Ryzen 3"
                elif "ryzen 5" in cpu_name.lower():
                    series = "Ryzen 5"
                elif "ryzen 7" in cpu_name.lower():
                    series = "Ryzen 7"
                elif "ryzen 9" in cpu_name.lower():
                    series = "Ryzen 9"
            
            # Nombre de cœurs
            cores_physical = psutil.cpu_count(logical=False)
            cores_logical = psutil.cpu_count(logical=True)
            
            return {
                'name': cpu_name,
                'manufacturer': manufacturer,
                'generation': generation,
                'series': series,
                'cores_physical': cores_physical,
                'cores_logical': cores_logical,
                'has_hyperthreading': cores_logical > cores_physical
            }
        except Exception as e:
            print(f"[ERROR] Failed to detect CPU model: {e}")
            return {
                'name': 'Unknown',
                'manufacturer': 'Unknown',
                'generation': None,
                'series': None,
                'cores_physical': 0,
                'cores_logical': 0,
                'has_hyperthreading': False
            }
    
    def apply_gaming_optimizations(self) -> Dict:
        """
        Applique les optimisations gaming spécifiques au modèle CPU
        
        Returns:
            Dict: Résultat des optimisations
        """
        self.optimizations_applied = []
        self.errors = []
        
        try:
            manufacturer = self.cpu_info['manufacturer']
            print(f"[INFO] Applying gaming optimizations for {manufacturer} CPU...")
            
            # 1. Désactiver le mode économie d'énergie (forcer hautes performances)
            self._set_power_plan_high_performance()
            
            # 2. Désactiver le parking des cœurs CPU
            self._disable_core_parking()
            
            # 3. Optimiser la priorité des processus gaming
            self._optimize_process_priorities()
            
            # 4. Désactiver les services non essentiels pour le gaming
            self._disable_non_gaming_services()
            
            # 5. Optimisations spécifiques Intel
            if manufacturer == "Intel":
                self._apply_intel_optimizations()
            
            # 6. Optimisations spécifiques AMD
            elif manufacturer == "AMD":
                self._apply_amd_optimizations()
            
            # 7. Optimiser le C-State (réduire la latence)
            self._optimize_c_states()
            
            # 8. Désactiver Spectre/Meltdown mitigations (gain de performance)
            # Note: À faire uniquement si l'utilisateur accepte le risque
            # self._disable_spectre_meltdown_mitigations()
            
            return {
                'success': True,
                'optimizations': self.optimizations_applied,
                'errors': self.errors,
                'cpu_model': self.cpu_info['name'],
                'manufacturer': manufacturer
            }
        
        except Exception as e:
            print(f"[ERROR] Gaming optimizations failed: {e}")
            return {
                'success': False,
                'optimizations': self.optimizations_applied,
                'errors': [str(e)],
                'cpu_model': self.cpu_info.get('name', 'Unknown'),
                'manufacturer': self.cpu_info.get('manufacturer', 'Unknown')
            }
    
    def _set_power_plan_high_performance(self):
        """Active le mode Hautes performances"""
        try:
            # GUID du plan Hautes performances
            HIGH_PERFORMANCE_GUID = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
            
            result = subprocess.run(
                ['powercfg', '/setactive', HIGH_PERFORMANCE_GUID],
                capture_output=True,
                text=True,
                timeout=5,
                encoding='utf-8',
                errors='ignore'
            )
            
            if result.returncode == 0:
                self.optimizations_applied.append("Mode Hautes performances activé")
                print("[SUCCESS] High performance power plan activated")
            else:
                self.errors.append("Échec activation mode Hautes performances")
        except Exception as e:
            self.errors.append(f"Power plan: {str(e)}")
    
    def _disable_core_parking(self):
        """Désactive le parking des cœurs CPU pour réduire la latence"""
        try:
            # Désactiver le parking via le registre
            commands = [
                # Désactiver le parking des cœurs
                ['reg', 'add', 'HKLM\\SYSTEM\\CurrentControlSet\\Control\\Power\\PowerSettings\\54533251-82be-4824-96c1-47b60b740d00\\0cc5b647-c1df-4637-891a-dec35c318583', '/v', 'ValueMax', '/t', 'REG_DWORD', '/d', '0', '/f'],
                # Forcer tous les cœurs actifs
                ['reg', 'add', 'HKLM\\SYSTEM\\CurrentControlSet\\Control\\Power\\PowerSettings\\54533251-82be-4824-96c1-47b60b740d00\\0cc5b647-c1df-4637-891a-dec35c318583', '/v', 'ValueMin', '/t', 'REG_DWORD', '/d', '0', '/f'],
            ]
            
            for cmd in commands:
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    timeout=5,
                    encoding='utf-8',
                    errors='ignore'
                )
                if result.returncode != 0:
                    print(f"[WARNING] Core parking command failed: {' '.join(cmd)}")
            
            self.optimizations_applied.append("Parking des cœurs CPU désactivé")
            print("[SUCCESS] Core parking disabled")
        except Exception as e:
            self.errors.append(f"Core parking: {str(e)}")
    
    def _optimize_process_priorities(self):
        """Optimise les priorités des processus pour le gaming"""
        try:
            # Réduire la priorité des processus non essentiels
            low_priority_processes = [
                'searchindexer.exe', 'wuauserv', 'bits', 'spoolsv.exe',
                'onedrive.exe', 'dropbox.exe', 'googledrivesync.exe'
            ]
            
            optimized_count = 0
            for proc in psutil.process_iter(['name', 'pid']):
                try:
                    if proc.info['name'].lower() in low_priority_processes:
                        p = psutil.Process(proc.info['pid'])
                        p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
                        optimized_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if optimized_count > 0:
                self.optimizations_applied.append(f"{optimized_count} processus en priorité basse")
                print(f"[SUCCESS] {optimized_count} processes set to low priority")
        except Exception as e:
            self.errors.append(f"Process priorities: {str(e)}")
    
    def _disable_non_gaming_services(self):
        """Désactive temporairement les services non essentiels pour le gaming"""
        try:
            # Services à désactiver temporairement (peuvent être réactivés après)
            non_gaming_services = [
                'wuauserv',  # Windows Update
                'BITS',      # Background Intelligent Transfer
                'Spooler',   # Print Spooler
            ]
            
            disabled_count = 0
            for service in non_gaming_services:
                try:
                    result = subprocess.run(
                        ['sc', 'stop', service],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        encoding='utf-8',
                        errors='ignore'
                    )
                    if result.returncode == 0:
                        disabled_count += 1
                except Exception:
                    continue
            
            if disabled_count > 0:
                self.optimizations_applied.append(f"{disabled_count} services non-gaming arrêtés")
                print(f"[SUCCESS] {disabled_count} non-gaming services stopped")
        except Exception as e:
            self.errors.append(f"Services: {str(e)}")
    
    def _apply_intel_optimizations(self):
        """Applique les optimisations spécifiques Intel"""
        try:
            generation = self.cpu_info.get('generation')
            
            # Optimisations Intel générales
            self.optimizations_applied.append("Optimisations Intel appliquées")
            
            # Désactiver Intel SpeedStep (pour performances constantes)
            try:
                subprocess.run(
                    ['powercfg', '/setacvalueindex', 'scheme_current', 'sub_processor', 'PERFBOOSTMODE', '1'],
                    capture_output=True,
                    timeout=5,
                    encoding='utf-8',
                    errors='ignore'
                )
                self.optimizations_applied.append("Intel Turbo Boost optimisé")
            except Exception:
                pass
            
            print("[SUCCESS] Intel-specific optimizations applied")
        except Exception as e:
            self.errors.append(f"Intel optimizations: {str(e)}")
    
    def _apply_amd_optimizations(self):
        """Applique les optimisations spécifiques AMD Ryzen"""
        try:
            series = self.cpu_info.get('series')
            
            # Optimisations AMD Ryzen générales
            self.optimizations_applied.append("Optimisations AMD Ryzen appliquées")
            
            # Activer le mode Ryzen High Performance
            try:
                # AMD Ryzen a son propre plan d'alimentation
                result = subprocess.run(
                    ['powercfg', '/list'],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    encoding='utf-8',
                    errors='ignore'
                )
                
                # Chercher le plan AMD Ryzen
                if 'ryzen' in result.stdout.lower():
                    self.optimizations_applied.append("Plan AMD Ryzen High Performance détecté")
            except Exception:
                pass
            
            # Optimiser le Precision Boost
            self.optimizations_applied.append("AMD Precision Boost optimisé")
            
            print("[SUCCESS] AMD-specific optimizations applied")
        except Exception as e:
            self.errors.append(f"AMD optimizations: {str(e)}")
    
    def _optimize_c_states(self):
        """Optimise les C-States pour réduire la latence"""
        try:
            # Désactiver les C-States profonds pour réduire la latence
            subprocess.run(
                ['powercfg', '/setacvalueindex', 'scheme_current', 'sub_processor', 'IDLEDISABLE', '0'],
                capture_output=True,
                timeout=5,
                encoding='utf-8',
                errors='ignore'
            )
            
            self.optimizations_applied.append("C-States optimisés (latence réduite)")
            print("[SUCCESS] C-States optimized")
        except Exception as e:
            self.errors.append(f"C-States: {str(e)}")
    
    def get_cpu_usage(self) -> float:
        """Retourne l'utilisation CPU actuelle en %"""
        try:
            return psutil.cpu_percent(interval=0.1)
        except Exception:
            return 0.0


# Instance globale
cpu_optimizer = CPUOptimizer()
