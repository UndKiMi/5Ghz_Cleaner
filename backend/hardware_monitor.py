"""
Hardware Monitoring Module
Monitore les composants matériels avec températures en temps réel
AUCUNE TÉLÉMÉTRIE - Toutes les données restent locales
"""
import psutil
import platform
import subprocess
import threading
import time
from typing import Dict, List, Optional


class HardwareMonitor:
    """
    Moniteur matériel sans télémétrie
    Toutes les données sont collectées et affichées localement uniquement
    """
    
    def __init__(self):
        self.monitoring = False
        self.monitor_thread = None
        self.last_data = {}
        self._lock = threading.Lock()
        self._temp_warning_shown = False  # Pour éviter les messages répétitifs
        self._gpu_warning_shown = False
    
    def get_cpu_info(self) -> Dict:
        """Récupère les informations CPU"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1, percpu=False)
            cpu_count = psutil.cpu_count(logical=False)
            cpu_count_logical = psutil.cpu_count(logical=True)
            cpu_freq = psutil.cpu_freq()
            
            # Température CPU (Windows - via WMI)
            temp = self._get_cpu_temperature()
            
            return {
                "name": platform.processor(),
                "usage": cpu_percent,
                "cores_physical": cpu_count,
                "cores_logical": cpu_count_logical,
                "frequency_current": cpu_freq.current if cpu_freq else 0,
                "frequency_max": cpu_freq.max if cpu_freq else 0,
                "temperature": temp,
            }
        except Exception as e:
            print(f"[ERROR] Failed to get CPU info: {e}")
            return {
                "name": "N/A",
                "usage": 0,
                "cores_physical": 0,
                "cores_logical": 0,
                "frequency_current": 0,
                "frequency_max": 0,
                "temperature": None,
            }
    
    def get_memory_info(self) -> Dict:
        """Récupère les informations mémoire"""
        try:
            mem = psutil.virtual_memory()
            
            return {
                "name": "RAM",
                "total": mem.total,
                "available": mem.available,
                "used": mem.used,
                "percent": mem.percent,
                "temperature": None,  # La RAM n'a généralement pas de capteur de température
            }
        except Exception as e:
            print(f"[ERROR] Failed to get memory info: {e}")
            return {
                "name": "RAM",
                "total": 0,
                "available": 0,
                "used": 0,
                "percent": 0,
                "temperature": None,
            }
    
    def get_disk_info(self) -> List[Dict]:
        """Récupère les informations disques"""
        disks = []
        try:
            partitions = psutil.disk_partitions()
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    
                    # Température disque (si disponible via SMART)
                    temp = self._get_disk_temperature(partition.device)
                    
                    disks.append({
                        "name": f"{partition.device} ({partition.fstype})",
                        "mountpoint": partition.mountpoint,
                        "total": usage.total,
                        "used": usage.used,
                        "free": usage.free,
                        "percent": usage.percent,
                        "temperature": temp,
                    })
                except PermissionError:
                    continue
                except Exception as e:
                    print(f"[WARNING] Failed to get disk info for {partition.device}: {e}")
                    continue
        except Exception as e:
            print(f"[ERROR] Failed to get disk info: {e}")
        
        return disks
    
    def get_gpu_info(self) -> List[Dict]:
        """Récupère les informations GPU (si disponible)"""
        gpus = []
        
        # Liste des adaptateurs à filtrer (virtuels, logiciels externes, etc.)
        excluded_keywords = [
            "Microsoft",      # Adaptateurs Microsoft de base
            "Parsec",         # Parsec Virtual Display
            "Virtual",        # Adaptateurs virtuels génériques
            "Remote",         # Adaptateurs de bureau à distance
            "TeamViewer",     # TeamViewer Display
            "VNC",            # VNC Display
            "Citrix",         # Citrix Display
        ]
        
        # Méthode 1: Essayer via WMI avec win32com (plus fiable)
        try:
            import win32com.client
            wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
            video_controllers = wmi.ExecQuery("SELECT * FROM Win32_VideoController")
            
            for gpu in video_controllers:
                gpu_name = gpu.Name
                
                # Filtrer les adaptateurs virtuels et logiciels externes
                if gpu_name and not any(keyword in gpu_name for keyword in excluded_keywords):
                    # Température GPU
                    temp = self._get_gpu_temperature(gpu_name)
                    
                    gpus.append({
                        "name": gpu_name,
                        "temperature": temp,
                    })
            
            if gpus:
                return gpus
        except Exception as e:
            # Ne pas afficher l'erreur COM, passer au fallback
            pass
        
        # Méthode 2: Fallback avec wmic subprocess
        try:
            result = subprocess.run(
                ['wmic', 'path', 'win32_VideoController', 'get', 'name'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                for line in lines:
                    gpu_name = line.strip()
                    
                    # Filtrer les adaptateurs virtuels et logiciels externes
                    if gpu_name and not any(keyword in gpu_name for keyword in excluded_keywords):
                        # Température GPU
                        temp = self._get_gpu_temperature(gpu_name)
                        
                        gpus.append({
                            "name": gpu_name,
                            "temperature": temp,
                        })
        except Exception as e:
            if not self._gpu_warning_shown:
                print(f"[INFO] GPU detection not available (normal on some systems)")
                self._gpu_warning_shown = True
        
        if not gpus:
            gpus.append({
                "name": "GPU non détecté",
                "temperature": None,
            })
        
        return gpus
    
    def get_network_info(self) -> Dict:
        """Récupère les informations réseau"""
        try:
            net_io = psutil.net_io_counters()
            
            return {
                "name": "Réseau",
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv,
                "temperature": None,
            }
        except Exception as e:
            print(f"[ERROR] Failed to get network info: {e}")
            return {
                "name": "Réseau",
                "bytes_sent": 0,
                "bytes_recv": 0,
                "packets_sent": 0,
                "packets_recv": 0,
                "temperature": None,
            }
    
    def _get_cpu_temperature(self) -> Optional[float]:
        """
        Récupère la température CPU via WMI (Windows)
        Note: Nécessite des privilèges admin et dépend du matériel
        """
        # Méthode 1: WMI MSAcpi_ThermalZoneTemperature
        try:
            result = subprocess.run(
                ['wmic', '/namespace:\\\\root\\wmi', 'PATH', 'MSAcpi_ThermalZoneTemperature', 'get', 'CurrentTemperature'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    try:
                        # La température est en dixièmes de Kelvin
                        temp_kelvin = int(lines[1].strip())
                        temp_celsius = (temp_kelvin / 10.0) - 273.15
                        if 0 < temp_celsius < 150:  # Vérification de validité
                            return round(temp_celsius, 1)
                    except ValueError:
                        pass
        except Exception:
            pass
        
        # Méthode 2: WMI Win32_TemperatureProbe
        try:
            result = subprocess.run(
                ['wmic', 'path', 'Win32_TemperatureProbe', 'get', 'CurrentReading'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    try:
                        # La température est en dixièmes de degrés Celsius
                        temp_raw = int(lines[1].strip())
                        temp_celsius = temp_raw / 10.0
                        if 0 < temp_celsius < 150:
                            return round(temp_celsius, 1)
                    except ValueError:
                        pass
        except Exception:
            pass
        
        # Méthode 3: WMI avec win32com
        try:
            import win32com.client
            wmi = win32com.client.GetObject("winmgmts://./root/wmi")
            temperature_info = wmi.ExecQuery("SELECT * FROM MSAcpi_ThermalZoneTemperature")
            
            for temp_obj in temperature_info:
                temp_kelvin = temp_obj.CurrentTemperature
                temp_celsius = (temp_kelvin / 10.0) - 273.15
                if 0 < temp_celsius < 150:
                    return round(temp_celsius, 1)
        except Exception:
            pass
        
        # Afficher le message une seule fois si toutes les méthodes échouent
        if not self._temp_warning_shown:
            print(f"[INFO] CPU temperature sensor not available (requires admin rights or specific hardware)")
            self._temp_warning_shown = True
        
        return None
    
    def _get_disk_temperature(self, device: str) -> Optional[float]:
        """
        Récupère la température disque via SMART
        Note: Difficile à obtenir sans outils tiers
        """
        # Non implémenté pour éviter les dépendances externes
        # Nécessiterait smartmontools ou similaire
        return None
    
    def _get_gpu_temperature(self, gpu_name: str) -> Optional[float]:
        """
        Récupère la température GPU
        Note: Nécessite des drivers spécifiques (NVIDIA-SMI, AMD ADL, etc.)
        """
        # Essayer nvidia-smi pour les GPU NVIDIA
        if "nvidia" in gpu_name.lower():
            try:
                result = subprocess.run(
                    ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode == 0:
                    temp = float(result.stdout.strip())
                    return round(temp, 1)
            except Exception:
                # nvidia-smi non disponible - normal si pas installé
                pass
        
        return None
    
    def get_all_components(self) -> Dict:
        """
        Récupère toutes les informations des composants
        AUCUNE DONNÉE N'EST ENVOYÉE - Tout reste local
        """
        with self._lock:
            data = {
                "cpu": self.get_cpu_info(),
                "memory": self.get_memory_info(),
                "disks": self.get_disk_info(),
                "gpus": self.get_gpu_info(),
                "network": self.get_network_info(),
            }
            self.last_data = data
            return data
    
    def start_monitoring(self, interval: float = 2.0, callback=None):
        """
        Démarre le monitoring en temps réel
        
        Args:
            interval: Intervalle de mise à jour en secondes
            callback: Fonction appelée à chaque mise à jour avec les données
        """
        if self.monitoring:
            print("[WARNING] Monitoring already started")
            return
        
        self.monitoring = True
        
        def monitor_loop():
            print(f"[INFO] Hardware monitoring started (interval: {interval}s)")
            while self.monitoring:
                try:
                    data = self.get_all_components()
                    if callback:
                        callback(data)
                    time.sleep(interval)
                except Exception as e:
                    print(f"[ERROR] Monitoring error: {e}")
                    time.sleep(interval)
            print("[INFO] Hardware monitoring stopped")
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Arrête le monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
    
    def get_temperature_color(self, temperature: Optional[float], component_type: str = "cpu") -> str:
        """
        Retourne la couleur selon la température
        
        Args:
            temperature: Température en Celsius
            component_type: Type de composant (cpu, gpu, disk)
        
        Returns:
            Couleur: "green", "yellow", "red"
        """
        if temperature is None:
            return "gray"
        
        # Seuils selon le type de composant
        if component_type == "cpu":
            if temperature < 60:
                return "green"
            elif temperature < 80:
                return "yellow"
            else:
                return "red"
        elif component_type == "gpu":
            if temperature < 70:
                return "green"
            elif temperature < 85:
                return "yellow"
            else:
                return "red"
        elif component_type == "disk":
            if temperature < 45:
                return "green"
            elif temperature < 55:
                return "yellow"
            else:
                return "red"
        else:
            # Par défaut
            if temperature < 50:
                return "green"
            elif temperature < 70:
                return "yellow"
            else:
                return "red"


# Instance globale
hardware_monitor = HardwareMonitor()
