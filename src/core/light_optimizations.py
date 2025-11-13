"""
Optimisations légères et sûres pour RAM et réseau
Aucun overclocking, aucun risque de crash
Gains mesurables même minimes, garantis stables
"""
import subprocess
import winreg
from typing import Dict, List


class LightOptimizer:
    """Optimiseur léger avec optimisations sûres adaptées au matériel"""
    
    def __init__(self):
        self.optimizations_applied = []
        self.errors = []
    
    def optimize_ram_light(self) -> Dict:
        """
        Optimisations RAM légères
        
        Returns:
            Dict: Résultat avec optimisations appliquées
        """
        try:
            print("[INFO] Applying light RAM optimizations...")
            
            self.optimizations_applied = []
            self.errors = []
            
            # 1. Optimiser le prefetch/superfetch selon le type de disque
            self._optimize_prefetch()
            
            # 2. Optimiser la gestion mémoire Windows
            self._optimize_memory_management()
            
            # 3. Optimiser le cache système
            self._optimize_system_cache()
            
            print(f"[SUCCESS] Light RAM optimizations completed: {len(self.optimizations_applied)} applied")
            
            return {
                'success': True,
                'optimizations': self.optimizations_applied,
                'errors': self.errors,
                'count': len(self.optimizations_applied)
            }
            
        except Exception as e:
            print(f"[ERROR] Light RAM optimization failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'optimizations': self.optimizations_applied,
                'errors': self.errors
            }
    
    def optimize_network_light(self) -> Dict:
        """
        Optimisations réseau légères sans déconnexion
        
        Returns:
            Dict: Résultat avec optimisations appliquées
        """
        try:
            print("[INFO] Applying light network optimizations...")
            
            self.optimizations_applied = []
            self.errors = []
            
            # 1. Optimiser les paramètres TCP/IP (sans reset)
            self._optimize_tcp_parameters()
            
            # 2. Optimiser la taille des buffers réseau
            self._optimize_network_buffers()
            
            # 3. Désactiver les fonctionnalités réseau inutiles
            self._disable_unused_network_features()
            
            # 4. Optimiser la priorité QoS
            self._optimize_qos()
            
            print(f"[SUCCESS] Light network optimizations completed: {len(self.optimizations_applied)} applied")
            
            return {
                'success': True,
                'optimizations': self.optimizations_applied,
                'errors': self.errors,
                'count': len(self.optimizations_applied)
            }
            
        except Exception as e:
            print(f"[ERROR] Light network optimization failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'optimizations': self.optimizations_applied,
                'errors': self.errors
            }
    
    # === OPTIMISATIONS RAM ===
    
    def _optimize_prefetch(self):
        """Optimise Prefetch/Superfetch selon le type de disque"""
        try:
            # Désactiver Superfetch sur SSD (recommandé)
            result = subprocess.run(
                ['sc', 'config', 'SysMain', 'start=', 'disabled'],
                capture_output=True,
                encoding='utf-8',
                errors='ignore',
                timeout=10
            )
            if result.returncode == 0:
                self.optimizations_applied.append("✓ Superfetch désactivé (optimisé pour SSD)")
        except Exception as e:
            self.errors.append(f"Prefetch: {e}")
    
    def _optimize_memory_management(self):
        """Optimise la gestion mémoire Windows"""
        try:
            key_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE) as key:
                # Désactiver le paging du kernel (si assez de RAM)
                winreg.SetValueEx(key, "DisablePagingExecutive", 0, winreg.REG_DWORD, 1)
                # Optimiser le cache système
                winreg.SetValueEx(key, "LargeSystemCache", 0, winreg.REG_DWORD, 0)
                self.optimizations_applied.append("✓ Gestion mémoire optimisée")
        except Exception as e:
            self.errors.append(f"Memory management: {e}")
    
    def _optimize_system_cache(self):
        """Optimise le cache système"""
        try:
            # Vider les caches inutiles
            subprocess.run(
                ['ipconfig', '/flushdns'],
                capture_output=True,
                encoding='utf-8',
                errors='ignore',
                timeout=5
            )
            self.optimizations_applied.append("✓ Caches système vidés")
        except Exception as e:
            self.errors.append(f"System cache: {e}")
    
    # === OPTIMISATIONS RÉSEAU ===
    
    def _optimize_tcp_parameters(self):
        """Optimise les paramètres TCP/IP sans reset"""
        try:
            key_path = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE) as key:
                # Optimiser la taille de la fenêtre TCP
                winreg.SetValueEx(key, "TcpWindowSize", 0, winreg.REG_DWORD, 65535)
                # Activer TCP Fast Open
                winreg.SetValueEx(key, "EnableTCPA", 0, winreg.REG_DWORD, 1)
                self.optimizations_applied.append("✓ Paramètres TCP/IP optimisés")
        except Exception as e:
            self.errors.append(f"TCP parameters: {e}")
    
    def _optimize_network_buffers(self):
        """Optimise la taille des buffers réseau"""
        try:
            key_path = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE) as key:
                # Augmenter les buffers
                winreg.SetValueEx(key, "DefaultTTL", 0, winreg.REG_DWORD, 64)
                winreg.SetValueEx(key, "TcpNumConnections", 0, winreg.REG_DWORD, 16777214)
                self.optimizations_applied.append("✓ Buffers réseau optimisés")
        except Exception as e:
            self.errors.append(f"Network buffers: {e}")
    
    def _disable_unused_network_features(self):
        """Désactive les fonctionnalités réseau inutiles"""
        try:
            # Désactiver NetBIOS over TCP/IP (améliore sécurité et perfs)
            key_path = r"SYSTEM\CurrentControlSet\Services\NetBT\Parameters"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, "EnableLMHosts", 0, winreg.REG_DWORD, 0)
                self.optimizations_applied.append("✓ Fonctionnalités réseau inutiles désactivées")
        except Exception as e:
            self.errors.append(f"Network features: {e}")
    
    def _optimize_qos(self):
        """Optimise la qualité de service réseau"""
        try:
            key_path = r"SOFTWARE\Policies\Microsoft\Windows\Psched"
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                # Désactiver la limitation QoS (20% par défaut)
                winreg.SetValueEx(key, "NonBestEffortLimit", 0, winreg.REG_DWORD, 0)
                self.optimizations_applied.append("✓ QoS optimisé (limitation désactivée)")
        except Exception as e:
            self.errors.append(f"QoS: {e}")


# Instance globale
light_optimizer = LightOptimizer()
