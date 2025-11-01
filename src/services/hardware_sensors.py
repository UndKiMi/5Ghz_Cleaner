"""
Module pour lire les températures matérielles via LibreHardwareMonitor
Supporte CPU AMD/Intel, GPU AMD/NVIDIA, Disques
"""
import os
import sys
from typing import Dict, Optional

class HardwareSensors:
    """Interface pour LibreHardwareMonitor"""
    
    def __init__(self):
        self.computer = None
        self.available = False
        self._initialize()
    
    def _initialize(self):
        """Initialise LibreHardwareMonitor"""
        try:
            import clr
            
            # Chemin vers le dossier libs (à la racine du projet)
            libs_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "libs"
            )
            
            dll_path = os.path.join(libs_dir, "LibreHardwareMonitorLib.dll")
            hidsharp_path = os.path.join(libs_dir, "HidSharp.dll")
            
            if not os.path.exists(dll_path):
                print(f"[INFO] LibreHardwareMonitorLib.dll not found at {dll_path}")
                print("[INFO] Temperature monitoring will use fallback methods")
                return
            
            # Charger HidSharp.dll d'abord (dépendance)
            if os.path.exists(hidsharp_path):
                try:
                    clr.AddReference(hidsharp_path)
                except Exception as e:
                    pass  # Silencieux
            
            # Charger LibreHardwareMonitorLib.dll
            clr.AddReference(dll_path)
            from LibreHardwareMonitor import Hardware
            
            # Créer l'instance Computer
            self.computer = Hardware.Computer()
            self.computer.IsCpuEnabled = True
            self.computer.IsGpuEnabled = True
            self.computer.IsMemoryEnabled = True
            self.computer.IsMotherboardEnabled = True
            self.computer.IsControllerEnabled = True
            self.computer.IsNetworkEnabled = False
            self.computer.IsStorageEnabled = True
            
            self.computer.Open()
            self.available = True
            
            print("    ✓ LibreHardwareMonitor loaded")
            
        except ImportError:
            pass  # Silencieux - géré par le message principal
        except Exception as e:
            pass  # Silencieux - géré par le message principal
    
    def get_cpu_temperature(self) -> Optional[float]:
        """Récupère la température CPU"""
        if not self.available or not self.computer:
            return None
        
        try:
            for hardware in self.computer.Hardware:
                hardware.Update()
                
                # Chercher le CPU
                if str(hardware.HardwareType) == "Cpu":
                    for sensor in hardware.Sensors:
                        # Température du package CPU
                        if str(sensor.SensorType) == "Temperature":
                            if "Package" in str(sensor.Name) or "CPU" in str(sensor.Name):
                                if sensor.Value is not None:
                                    return float(sensor.Value)
                    
                    # Si pas de "Package", prendre la première température
                    for sensor in hardware.Sensors:
                        if str(sensor.SensorType) == "Temperature":
                            if sensor.Value is not None:
                                return float(sensor.Value)
        except Exception as e:
            print(f"[WARNING] Error reading CPU temperature: {e}")
        
        return None
    
    def get_gpu_temperature(self, gpu_name: str = None) -> Optional[float]:
        """Récupère la température GPU"""
        if not self.available or not self.computer:
            return None
        
        try:
            for hardware in self.computer.Hardware:
                hardware.Update()
                
                # Chercher le GPU (AMD ou NVIDIA)
                hw_type = str(hardware.HardwareType)
                if hw_type in ["GpuAmd", "GpuNvidia", "GpuIntel"]:
                    # Si un nom spécifique est demandé, vérifier
                    if gpu_name and gpu_name.lower() not in str(hardware.Name).lower():
                        continue
                    
                    for sensor in hardware.Sensors:
                        if str(sensor.SensorType) == "Temperature":
                            # Prendre la température du core GPU
                            if "Core" in str(sensor.Name) or "GPU" in str(sensor.Name):
                                if sensor.Value is not None:
                                    return float(sensor.Value)
                    
                    # Si pas de "Core", prendre la première température
                    for sensor in hardware.Sensors:
                        if str(sensor.SensorType) == "Temperature":
                            if sensor.Value is not None:
                                return float(sensor.Value)
        except Exception as e:
            print(f"[WARNING] Error reading GPU temperature: {e}")
        
        return None
    
    def get_gpu_usage(self, gpu_name: str = None) -> Optional[float]:
        """Récupère l'utilisation GPU"""
        if not self.available or not self.computer:
            return None
        
        try:
            for hardware in self.computer.Hardware:
                hardware.Update()
                
                hw_type = str(hardware.HardwareType)
                if hw_type in ["GpuAmd", "GpuNvidia", "GpuIntel"]:
                    if gpu_name and gpu_name.lower() not in str(hardware.Name).lower():
                        continue
                    
                    for sensor in hardware.Sensors:
                        if str(sensor.SensorType) == "Load":
                            if "Core" in str(sensor.Name) or "GPU" in str(sensor.Name):
                                if sensor.Value is not None:
                                    return float(sensor.Value)
        except Exception as e:
            print(f"[WARNING] Error reading GPU usage: {e}")
        
        return None
    
    def get_disk_temperature(self, disk_name: str) -> Optional[float]:
        """Récupère la température d'un disque"""
        if not self.available or not self.computer:
            return None
        
        try:
            for hardware in self.computer.Hardware:
                hardware.Update()
                
                if str(hardware.HardwareType) == "Storage":
                    # Vérifier si c'est le bon disque
                    if disk_name and disk_name not in str(hardware.Name):
                        continue
                    
                    for sensor in hardware.Sensors:
                        if str(sensor.SensorType) == "Temperature":
                            if sensor.Value is not None:
                                return float(sensor.Value)
        except Exception as e:
            print(f"[WARNING] Error reading disk temperature: {e}")
        
        return None
    
    def close(self):
        """Ferme LibreHardwareMonitor"""
        if self.computer:
            try:
                self.computer.Close()
            except:
                pass


# Instance globale
hardware_sensors = HardwareSensors()
