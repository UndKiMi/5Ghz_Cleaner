"""
Hardware Monitoring Module
Monitore les composants matériels avec températures en temps réel
AUCUNE TÉLÉMÉTRIE - Toutes les données restent locales
"""
import psutil
import platform
import subprocess
import struct
import threading
import time
from typing import Dict, List, Optional
from datetime import datetime

# Importer le module de capteurs matériels
try:
    from backend.hardware_sensors import hardware_sensors
    SENSORS_AVAILABLE = True
except Exception as e:
    print(f"[INFO] Hardware sensors not available: {e}")
    SENSORS_AVAILABLE = False
    hardware_sensors = None


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
            
            # Récupérer le nom commercial du CPU via WMI
            cpu_name = platform.processor()
            try:
                import win32com.client
                wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
                processors = wmi.ExecQuery("SELECT Name FROM Win32_Processor")
                for processor in processors:
                    if processor.Name:
                        cpu_name = processor.Name.strip()
                        break
            except:
                pass  # Garder le nom par défaut si WMI échoue
            
            return {
                "name": cpu_name,
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
            ram_manufacturer = None
            
            try:
                import win32com.client
                wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
                memory_chips = wmi.ExecQuery("SELECT * FROM Win32_PhysicalMemory")
                
                module_count = 0
                for chip in memory_chips:
                    module_count += 1
                    
                    # Fabricant (premier module seulement)
                    if ram_manufacturer is None and hasattr(chip, 'Manufacturer') and chip.Manufacturer:
                        manufacturer = chip.Manufacturer.strip()
                        # Nettoyer les noms de fabricants
                        if manufacturer and manufacturer not in ["", "Manufacturer", "Unknown"]:
                            ram_manufacturer = manufacturer
                    
                    # Type de mémoire (SMBIOSMemoryType est plus précis)
                    if hasattr(chip, 'SMBIOSMemoryType') and chip.SMBIOSMemoryType:
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
                    
                    # Fallback: MemoryType (moins précis)
                    if ram_type == "Unknown" and hasattr(chip, 'MemoryType') and chip.MemoryType:
                        memory_type = chip.MemoryType
                        if memory_type == 24:
                            ram_type = "DDR3"
                        elif memory_type == 20:
                            ram_type = "DDR"
                    
                    # Vitesse de la RAM
                    if hasattr(chip, 'Speed') and chip.Speed:
                        ram_speed = chip.Speed
                    
                    # Capacité du module
                    if hasattr(chip, 'Capacity') and chip.Capacity:
                        capacity_gb = int(chip.Capacity) / (1024**3)
                        ram_modules.append(capacity_gb)
                
                # Si aucun module détecté mais on a de la RAM, estimer
                if module_count == 0 and mem.total > 0:
                    # Estimer le nombre de modules (approximation)
                    total_gb = mem.total / (1024**3)
                    if total_gb <= 8:
                        ram_modules = [total_gb]
                    elif total_gb <= 16:
                        ram_modules = [total_gb / 2, total_gb / 2]
                    else:
                        # Supposer 4 modules pour les grandes capacités
                        module_size = total_gb / 4
                        ram_modules = [module_size] * 4
            except Exception as e:
                # Fallback: estimer basé sur la capacité totale
                if mem.total > 0:
                    total_gb = mem.total / (1024**3)
                    if total_gb <= 8:
                        ram_modules = [total_gb]
                    elif total_gb <= 16:
                        ram_modules = [total_gb / 2, total_gb / 2]
                    else:
                        module_size = total_gb / 4
                        ram_modules = [module_size] * 4
            
            # Construire le nom commercial avec fabricant et type DDR (sans fréquence)
            name_parts = []
            
            # Ajouter le fabricant si disponible
            if ram_manufacturer:
                name_parts.append(ram_manufacturer)
            
            # Ajouter le type
            if ram_type != "Unknown":
                name_parts.append(ram_type)
            else:
                name_parts.append("RAM")
            
            # Ne PAS ajouter la vitesse dans le nom (sera dans les détails)
            
            name = " ".join(name_parts) if name_parts else "RAM"
            
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
            disk_info_map = {}  # Mapping partition -> (model, type)
            try:
                import win32com.client
                wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
                
                # Récupérer les disques physiques
                physical_disks = wmi.ExecQuery("SELECT * FROM Win32_DiskDrive")
                for disk in physical_disks:
                    model = disk.Model if disk.Model else "Unknown"
                    device_id = disk.DeviceID
                    
                    # Déterminer le type de disque
                    media_type = disk.MediaType if hasattr(disk, 'MediaType') else ""
                    interface_type = disk.InterfaceType if hasattr(disk, 'InterfaceType') else ""
                    
                    # Détection du type améliorée
                    model_upper = model.upper()
                    media_upper = media_type.upper() if media_type else ""
                    interface_upper = interface_type.upper() if interface_type else ""
                    
                    if "NVME" in model_upper or "NVME" in interface_upper or "NVM EXPRESS" in model_upper:
                        disk_type = "SSD NVMe"
                    elif "SSD" in model_upper or "SOLID STATE" in media_upper or "SAMSUNG" in model_upper or "CRUCIAL" in model_upper or "KINGSTON" in model_upper:
                        disk_type = "SSD"
                    elif "FIXED HARD DISK" in media_upper or "HDD" in model_upper or "SEAGATE" in model_upper or "WD" in model_upper or "WESTERN DIGITAL" in model_upper:
                        disk_type = "HDD"
                    else:
                        # Fallback: détecter par le nom du modèle
                        if any(brand in model_upper for brand in ["SAMSUNG", "CRUCIAL", "KINGSTON", "INTEL", "CORSAIR", "ADATA"]):
                            disk_type = "SSD"
                        else:
                            disk_type = "Unknown"
                    
                    # Mapper les partitions à ce disque
                    try:
                        partitions_query = wmi.ExecQuery(
                            f"ASSOCIATORS OF {{Win32_DiskDrive.DeviceID='{device_id}'}} "
                            "WHERE AssocClass = Win32_DiskDriveToDiskPartition"
                        )
                        for partition in partitions_query:
                            logical_disks = wmi.ExecQuery(
                                f"ASSOCIATORS OF {{Win32_DiskPartition.DeviceID='{partition.DeviceID}'}} "
                                "WHERE AssocClass = Win32_LogicalDiskToPartition"
                            )
                            for logical_disk in logical_disks:
                                drive_letter = logical_disk.DeviceID
                                disk_info_map[drive_letter] = (model, disk_type)
                    except Exception:
                        pass
            except Exception:
                pass
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    
                    # Température disque (si disponible via SMART)
                    temp = self._get_disk_temperature(partition.device)
                    
                    # Récupérer les infos du disque depuis le mapping
                    drive_letter = partition.device
                    if drive_letter in disk_info_map:
                        disk_model, disk_type = disk_info_map[drive_letter]
                    else:
                        # Fallback: Essayer de détecter via le nom du système de fichiers
                        disk_model = "Unknown"
                        # Détecter SSD vs HDD par la vitesse de lecture (méthode heuristique)
                        try:
                            # Les SSD sont généralement plus rapides
                            # On peut aussi vérifier si c'est un disque fixe
                            if partition.fstype in ['NTFS', 'exFAT', 'FAT32']:
                                # Assumer SSD pour les disques modernes (heuristique)
                                disk_type = "SSD"
                            else:
                                disk_type = "Unknown"
                        except:
                            disk_type = "Unknown"
                    
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
        Récupère la température CPU via LibreHardwareMonitor ou méthodes natives Windows
        """
        # Méthode 1: LibreHardwareMonitor (PRIORITAIRE - Fonctionne avec AMD)
        if SENSORS_AVAILABLE and hardware_sensors:
            try:
                temp = hardware_sensors.get_cpu_temperature()
                if temp is not None:
                    return round(temp, 1)
            except Exception as e:
                print(f"[DEBUG] LibreHardwareMonitor CPU temp failed: {e}")
        
        # Méthode 2: WMI MSAcpi_ThermalZoneTemperature (NATIF WINDOWS)
        try:
            import win32com.client
            wmi = win32com.client.GetObject("winmgmts://./root/wmi")
            temperature_info = wmi.ExecQuery("SELECT * FROM MSAcpi_ThermalZoneTemperature")
            
            temps = []
            for temp_obj in temperature_info:
                temp_kelvin = temp_obj.CurrentTemperature
                temp_celsius = (temp_kelvin / 10.0) - 273.15
                if 0 < temp_celsius < 150:
                    temps.append(temp_celsius)
            
            if temps:
                # Retourner la moyenne si plusieurs zones thermiques
                avg_temp = sum(temps) / len(temps)
                return round(avg_temp, 1)
        except Exception:
            pass
        
        # Méthode 2: WMI via wmic (NATIF WINDOWS)
        try:
            from backend.system_commands import system_cmd
            result = system_cmd.run_wmic(['/namespace:\\\\root\\wmi', 'PATH', 'MSAcpi_ThermalZoneTemperature', 'get', 'CurrentTemperature'])
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                temps = []
                for line in lines[1:]:  # Skip header
                    try:
                        temp_kelvin = int(line.strip())
                        temp_celsius = (temp_kelvin / 10.0) - 273.15
                        if 0 < temp_celsius < 150:
                            temps.append(temp_celsius)
                    except (ValueError, AttributeError):
                        continue
                
                if temps:
                    avg_temp = sum(temps) / len(temps)
                    return round(avg_temp, 1)
        except Exception:
            pass
        
        # Méthode 3: Win32_TemperatureProbe (NATIF WINDOWS)
        try:
            import win32com.client
            wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
            probes = wmi.ExecQuery("SELECT * FROM Win32_TemperatureProbe")
            
            for probe in probes:
                if probe.CurrentReading:
                    temp_celsius = probe.CurrentReading / 10.0
                    if 0 < temp_celsius < 150:
                        return round(temp_celsius, 1)
        except Exception:
            pass
        
        # Méthode 4: Win32_PerfFormattedData_Counters_ThermalZoneInformation (NATIF WINDOWS)
        try:
            import win32com.client
            wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
            thermal_zones = wmi.ExecQuery("SELECT * FROM Win32_PerfFormattedData_Counters_ThermalZoneInformation")
            
            temps = []
            for zone in thermal_zones:
                if zone.Temperature:
                    # La température est en dixièmes de Kelvin
                    temp_celsius = (zone.Temperature / 10.0) - 273.15
                    if 0 < temp_celsius < 150:
                        temps.append(temp_celsius)
            
            if temps:
                avg_temp = sum(temps) / len(temps)
                return round(avg_temp, 1)
        except Exception:
            pass
        
        # Méthode 5: Lecture directe via ctypes (MÉTHODE AVANCÉE)
        try:
            temp = self._read_cpu_temp_via_msr()
            if temp:
                return temp
        except Exception:
            pass
        
        # Afficher le message une seule fois si toutes les méthodes échouent
        if not self._temp_warning_shown:
            print(f"[INFO] CPU temperature sensors not exposed by your hardware/BIOS")
            print(f"[INFO] This is normal on some systems - temperature monitoring unavailable")
            self._temp_warning_shown = True
        
        return None
    
    def _read_cpu_temp_via_msr(self) -> Optional[float]:
        """
        Lecture directe des MSR (Model Specific Registers) pour Intel
        Nécessite des privilèges administrateur
        """
        try:
            # Vérifier si c'est un CPU Intel
            cpu_info = platform.processor().lower()
            if 'intel' not in cpu_info:
                return None
            
            # MSR pour la température Intel (IA32_THERM_STATUS)
            MSR_TEMPERATURE = 0x19C
            
            # Tenter de lire via le driver WinRing0 si disponible
            # Note: Cela nécessiterait un driver kernel, donc on skip pour l'instant
            return None
        except Exception:
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
        """Récupère la température GPU via LibreHardwareMonitor ou méthodes natives"""
        
        # Méthode 1: LibreHardwareMonitor (PRIORITAIRE - Fonctionne avec AMD et NVIDIA)
        if SENSORS_AVAILABLE and hardware_sensors:
            try:
                temp = hardware_sensors.get_gpu_temperature(gpu_name)
                if temp is not None:
                    return round(temp, 1)
            except Exception as e:
                print(f"[DEBUG] LibreHardwareMonitor GPU temp failed: {e}")
        
        # Méthode 2: NVIDIA via nvidia-smi (installé avec les drivers NVIDIA)
        if "nvidia" in gpu_name.lower():
            try:
                # nvidia-smi est installé automatiquement avec les drivers NVIDIA
                result = subprocess.run(
                    ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'],
                    capture_output=True,
                    text=True,
                    timeout=2,
                    creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                )
                if result.returncode == 0:
                    temp = float(result.stdout.strip())
                    if 0 < temp < 150:
                        return round(temp, 1)
            except Exception:
                pass
        
        # Méthode 2: AMD via ADL (AMD Display Library) - WMI
        if "amd" in gpu_name.lower() or "radeon" in gpu_name.lower():
            try:
                import win32com.client
                wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
                # Essayer de récupérer via les compteurs de performance
                perf_data = wmi.ExecQuery("SELECT * FROM Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine")
                # Note: AMD n'expose pas toujours la température via WMI
            except Exception:
                pass
        
        # Méthode 3: Intel via WMI
        if "intel" in gpu_name.lower():
            try:
                import win32com.client
                wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
                # Intel iGPU n'expose généralement pas la température
            except Exception:
                pass
        
        # Méthode 4: Essayer via DXGI (DirectX Graphics Infrastructure)
        try:
            temp = self._get_gpu_temp_via_dxgi()
            if temp:
                return temp
        except Exception:
            pass
        
        return None
    
    def _get_gpu_temp_via_dxgi(self) -> Optional[float]:
        """Tente de récupérer la température GPU via DXGI (Windows natif)"""
        try:
            # DXGI n'expose pas directement la température
            # Cette méthode est un placeholder pour de futures implémentations
            return None
        except Exception:
            return None
    
    def _get_gpu_usage(self, gpu_name: str) -> float:
        """Récupère l'utilisation GPU en pourcentage via LibreHardwareMonitor ou méthodes natives"""
        
        # Méthode 1: LibreHardwareMonitor (PRIORITAIRE - Fonctionne avec AMD et NVIDIA)
        if SENSORS_AVAILABLE and hardware_sensors:
            try:
                usage = hardware_sensors.get_gpu_usage(gpu_name)
                if usage is not None:
                    return round(usage, 1)
            except Exception as e:
                print(f"[DEBUG] LibreHardwareMonitor GPU usage failed: {e}")
        
        # Méthode 2: NVIDIA via nvidia-smi (natif avec drivers)
        if "nvidia" in gpu_name.lower():
            try:
                result = subprocess.run(
                    ['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'],
                    capture_output=True,
                    text=True,
                    timeout=2,
                    creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                )
                if result.returncode == 0:
                    usage = float(result.stdout.strip())
                    return round(usage, 1)
            except Exception:
                pass
        
        # Méthode 2: Compteurs de performance Windows (NATIF)
        try:
            import win32com.client
            wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
            
            # Windows 10/11 expose les compteurs GPU
            gpu_counters = wmi.ExecQuery(
                "SELECT * FROM Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine"
            )
            
            total_usage = 0
            count = 0
            for counter in gpu_counters:
                if hasattr(counter, 'UtilizationPercentage'):
                    total_usage += float(counter.UtilizationPercentage)
                    count += 1
            
            if count > 0:
                return round(total_usage / count, 1)
        except Exception:
            pass
        
        # Méthode 3: Via PDH (Performance Data Helper) - NATIF WINDOWS
        try:
            usage = self._get_gpu_usage_via_pdh()
            if usage is not None:
                return usage
        except Exception:
            pass
        
        return 0
    
    def _get_gpu_usage_via_pdh(self) -> Optional[float]:
        """Récupère l'utilisation GPU via PDH (Performance Data Helper)"""
        try:
            # PDH est l'API native Windows pour les compteurs de performance
            # Nécessite win32pdh (partie de pywin32)
            import win32pdh
            
            # Créer une requête
            query = win32pdh.OpenQuery()
            
            # Ajouter le compteur GPU
            counter_path = r'\GPU Engine(*)\Utilization Percentage'
            counter = win32pdh.AddCounter(query, counter_path)
            
            # Collecter les données
            win32pdh.CollectQueryData(query)
            time.sleep(0.1)  # Attendre un peu
            win32pdh.CollectQueryData(query)
            
            # Récupérer la valeur
            status, value = win32pdh.GetFormattedCounterValue(counter, win32pdh.PDH_FMT_DOUBLE)
            
            win32pdh.CloseQuery(query)
            
            if status == 0:
                return round(value, 1)
        except Exception:
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
