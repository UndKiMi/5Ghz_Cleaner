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
        """Récupère les informations mémoire avec détails DDR"""
        try:
            mem = psutil.virtual_memory()
            
            # Récupérer les détails de la RAM via WMI
            ram_type = "Unknown"
            ram_speed = 0
            ram_modules = []
            
            try:
                import win32com.client
                wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
                memory_chips = wmi.ExecQuery("SELECT * FROM Win32_PhysicalMemory")
                
                for chip in memory_chips:
                    # Type de mémoire (SMBIOSMemoryType est plus précis)
                    memory_type = chip.SMBIOSMemoryType
                    if memory_type == 26:
                        ram_type = "DDR4"
                    elif memory_type == 34:
                        ram_type = "DDR5"
                    elif memory_type == 24:
                        ram_type = "DDR3"
                    elif memory_type == 21:
                        ram_type = "DDR2"
                    elif memory_type == 20:
                        ram_type = "DDR"
                    
                    # Vitesse de la RAM
                    if chip.Speed:
                        ram_speed = chip.Speed
                    
                    # Capacité du module
                    if chip.Capacity:
                        capacity_gb = int(chip.Capacity) / (1024**3)
                        ram_modules.append(capacity_gb)
            except Exception:
                pass
            
            # Construire le nom avec le type DDR
            if ram_type != "Unknown":
                name = f"RAM {ram_type}"
                if ram_speed > 0:
                    name += f" {ram_speed} MHz"
            else:
                name = "RAM"
            
            return {
                "name": name,
                "type": ram_type,
                "speed": ram_speed,
                "modules": ram_modules,
                "total": mem.total,
                "available": mem.available,
                "used": mem.used,
                "percent": mem.percent,
                "temperature": None,
            }
        except Exception as e:
            print(f"[ERROR] Failed to get memory info: {e}")
            return {
                "name": "RAM",
                "type": "Unknown",
                "speed": 0,
                "modules": [],
                "total": 0,
                "available": 0,
                "used": 0,
                "percent": 0,
                "temperature": None,
            }
    
    def get_disk_info(self) -> List[Dict]:
        """Récupère les informations disques avec type (HDD/SSD/NVMe)"""
        disks = []
        try:
            partitions = psutil.disk_partitions()
            
            # Récupérer les informations des disques physiques via WMI
            disk_models = {}
            disk_types = {}
            try:
                import win32com.client
                wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
                
                # Récupérer les disques physiques
                physical_disks = wmi.ExecQuery("SELECT * FROM Win32_DiskDrive")
                for disk in physical_disks:
                    device_id = disk.DeviceID.replace("\\\\\\\\.\\\\PHYSICALDRIVE", "")
                    model = disk.Model if disk.Model else "Unknown"
                    
                    # Déterminer le type de disque
                    media_type = disk.MediaType if hasattr(disk, 'MediaType') else ""
                    if "SSD" in model.upper() or "NVMe" in model.upper():
                        if "NVMe" in model.upper():
                            disk_type = "SSD NVMe"
                        else:
                            disk_type = "SSD"
                    elif media_type and "SSD" in media_type.upper():
                        disk_type = "SSD"
                    else:
                        disk_type = "HDD"
                    
                    disk_models[device_id] = model
                    disk_types[device_id] = disk_type
            except Exception:
                pass
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    
                    # Température disque (si disponible via SMART)
                    temp = self._get_disk_temperature(partition.device)
                    
                    # Extraire le numéro de disque physique
                    device_num = partition.device.replace(":", "").replace("\\", "")
                    disk_model = "Unknown"
                    disk_type = "Unknown"
                    
                    # Essayer de trouver le modèle et le type
                    for key in disk_models:
                        disk_model = disk_models.get(key, "Unknown")
                        disk_type = disk_types.get(key, "Unknown")
                        break
                    
                    disks.append({
                        "name": f"{partition.device}",
                        "model": disk_model,
                        "type": disk_type,
                        "fstype": partition.fstype,
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
        """Récupère les informations GPU avec utilisation et version du pilote"""
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
                    
                    # Version du pilote
                    driver_version = gpu.DriverVersion if gpu.DriverVersion else "N/A"
                    driver_date = gpu.DriverDate if gpu.DriverDate else "N/A"
                    
                    # Utilisation GPU (via nvidia-smi ou autres)
                    usage = self._get_gpu_usage(gpu_name)
                    
                    gpus.append({
                        "name": gpu_name,
                        "temperature": temp,
                        "driver_version": driver_version,
                        "driver_date": driver_date,
                        "usage": usage,
                    })
            
            if gpus:
                return gpus
        except Exception as e:
            # Ne pas afficher l'erreur COM, passer au fallback
            pass
        
        # Méthode 2: Fallback avec wmic subprocess
        try:
            from backend.system_commands import system_cmd
            result = system_cmd.run_wmic(['path', 'win32_VideoController', 'get', 'name'])
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                for line in lines:
                    gpu_name = line.strip()
                    
                    # Filtrer les adaptateurs virtuels et logiciels externes
                    if gpu_name and not any(keyword in gpu_name for keyword in excluded_keywords):
                        # Température GPU
                        temp = self._get_gpu_temperature(gpu_name)
                        usage = self._get_gpu_usage(gpu_name)
                        
                        gpus.append({
                            "name": gpu_name,
                            "temperature": temp,
                            "driver_version": "N/A",
                            "driver_date": "N/A",
                            "usage": usage,
                        })
        except Exception as e:
            if not self._gpu_warning_shown:
                print(f"[INFO] GPU detection not available (normal on some systems)")
                self._gpu_warning_shown = True
        
        if not gpus:
            gpus.append({
                "name": "GPU non détecté",
                "temperature": None,
                "driver_version": "N/A",
                "driver_date": "N/A",
                "usage": 0,
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
        Récupère la température CPU via WMI (Windows) avec méthodes multiples
        Note: Nécessite des privilèges admin et dépend du matériel
        """
        # Méthode 1: OpenHardwareMonitor/LibreHardwareMonitor (MEILLEURE MÉTHODE)
        try:
            import win32com.client
            wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\OpenHardwareMonitor")
            sensors = wmi.ExecQuery("SELECT * FROM Sensor")
            
            cpu_temps = []
            for sensor in sensors:
                if sensor.SensorType == 'Temperature' and 'CPU' in sensor.Name and 'GPU' not in sensor.Name:
                    cpu_temps.append(float(sensor.Value))
            
            if cpu_temps:
                # Retourner la moyenne des températures CPU
                avg_temp = sum(cpu_temps) / len(cpu_temps)
                return round(avg_temp, 1)
        except Exception:
            pass
        
        # Méthode 2: LibreHardwareMonitor namespace
        try:
            import win32com.client
            wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\LibreHardwareMonitor")
            sensors = wmi.ExecQuery("SELECT * FROM Sensor")
            
            cpu_temps = []
            for sensor in sensors:
                if sensor.SensorType == 'Temperature' and 'CPU' in sensor.Name and 'GPU' not in sensor.Name:
                    cpu_temps.append(float(sensor.Value))
            
            if cpu_temps:
                avg_temp = sum(cpu_temps) / len(cpu_temps)
                return round(avg_temp, 1)
        except Exception:
            pass
        
        # Méthode 3: WMI MSAcpi_ThermalZoneTemperature
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
        
        # Méthode 4: WMI via wmic
        try:
            from backend.system_commands import system_cmd
            result = system_cmd.run_wmic(['/namespace:\\\\root\\wmi', 'PATH', 'MSAcpi_ThermalZoneTemperature', 'get', 'CurrentTemperature'])
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    try:
                        temp_kelvin = int(lines[1].strip())
                        temp_celsius = (temp_kelvin / 10.0) - 273.15
                        if 0 < temp_celsius < 150:
                            return round(temp_celsius, 1)
                    except ValueError:
                        pass
        except Exception:
            pass
        
        # Méthode 5: Win32_TemperatureProbe
        try:
            from backend.system_commands import system_cmd
            result = system_cmd.run_wmic(['path', 'Win32_TemperatureProbe', 'get', 'CurrentReading'])
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    try:
                        temp_raw = int(lines[1].strip())
                        temp_celsius = temp_raw / 10.0
                        if 0 < temp_celsius < 150:
                            return round(temp_celsius, 1)
                    except ValueError:
                        pass
        except Exception:
            pass
        
        # Afficher le message une seule fois si toutes les méthodes échouent
        if not self._temp_warning_shown:
            print(f"[INFO] CPU temperature not available. Install OpenHardwareMonitor or LibreHardwareMonitor for temperature monitoring.")
            print(f"[INFO] Download: https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases")
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
        """Récupère la température GPU avec méthodes multiples
        Note: Nécessite des drivers spécifiques (NVIDIA-SMI, AMD ADL, etc.)
        """
        # Méthode 1: nvidia-smi pour les GPU NVIDIA
        if "nvidia" in gpu_name.lower():
            try:
                from backend.system_commands import system_cmd
                result = system_cmd.run_nvidia_smi(['--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'])
                if result is None:
                    return None
                
                if result.returncode == 0:
                    temp = float(result.stdout.strip())
                    return round(temp, 1)
            except Exception:
                pass
        
        # Méthode 2: Essayer OpenHardwareMonitor/LibreHardwareMonitor WMI
        try:
            import win32com.client
            wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\OpenHardwareMonitor")
            sensors = wmi.ExecQuery("SELECT * FROM Sensor")
            
            for sensor in sensors:
                if sensor.SensorType == 'Temperature' and 'GPU' in sensor.Name:
                    return round(float(sensor.Value), 1)
        except Exception:
            pass
        
        # Méthode 3: LibreHardwareMonitor namespace
        try:
            import win32com.client
            wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\LibreHardwareMonitor")
            sensors = wmi.ExecQuery("SELECT * FROM Sensor")
            
            for sensor in sensors:
                if sensor.SensorType == 'Temperature' and 'GPU' in sensor.Name:
                    return round(float(sensor.Value), 1)
        except Exception:
            pass
        
        return None
    
    def _get_gpu_usage(self, gpu_name: str) -> float:
        """Récupère l'utilisation GPU en pourcentage"""
        # Méthode 1: nvidia-smi pour les GPU NVIDIA
        if "nvidia" in gpu_name.lower():
            try:
                from backend.system_commands import system_cmd
                result = system_cmd.run_nvidia_smi(['--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'])
                if result and result.returncode == 0:
                    usage = float(result.stdout.strip())
                    return round(usage, 1)
            except Exception:
                pass
        
        # Méthode 2: OpenHardwareMonitor/LibreHardwareMonitor
        try:
            import win32com.client
            wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\OpenHardwareMonitor")
            sensors = wmi.ExecQuery("SELECT * FROM Sensor")
            
            for sensor in sensors:
                if sensor.SensorType == 'Load' and 'GPU Core' in sensor.Name:
                    return round(float(sensor.Value), 1)
        except Exception:
            pass
        
        # Méthode 3: LibreHardwareMonitor namespace
        try:
            import win32com.client
            wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\LibreHardwareMonitor")
            sensors = wmi.ExecQuery("SELECT * FROM Sensor")
            
            for sensor in sensors:
                if sensor.SensorType == 'Load' and 'GPU Core' in sensor.Name:
                    return round(float(sensor.Value), 1)
        except Exception:
            pass
        
        return 0
    
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
    
    def start_monitoring(self, interval: float = 1.0, callback=None):
        """
        Démarre le monitoring en temps réel
        
        Args:
            interval: Intervalle de mise à jour en secondes (défaut: 1.0 pour plus de fluidité)
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
