"""
Cooldown Manager - Gestion centralisée des cooldowns
Optimisation: État centralisé, moins de mémoire, thread-safe
"""
import threading
import time
from typing import Dict, Tuple, Optional, Callable
from datetime import datetime, timedelta


class CooldownManager:
    """Gestionnaire centralisé de cooldowns thread-safe"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._cooldowns: Dict[str, float] = {}  # action_name -> timestamp
            self._durations: Dict[str, int] = {}    # action_name -> duration
            self._callbacks: Dict[str, list] = {}   # action_name -> [callbacks]
            self._lock = threading.RLock()
            self._initialized = True
    
    def register(self, action_name: str, duration: int):
        """
        Enregistre une action avec sa durée de cooldown
        
        Args:
            action_name: Nom de l'action
            duration: Durée du cooldown en secondes
        """
        with self._lock:
            self._durations[action_name] = duration
    
    def start(self, action_name: str) -> bool:
        """
        Démarre un cooldown pour une action
        
        Args:
            action_name: Nom de l'action
            
        Returns:
            bool: True si le cooldown a démarré, False si déjà actif
        """
        with self._lock:
            if self.is_active(action_name):
                return False
            
            self._cooldowns[action_name] = time.time()
            return True
    
    def is_active(self, action_name: str) -> bool:
        """Vérifie si un cooldown est actif"""
        with self._lock:
            if action_name not in self._cooldowns:
                return False
            
            elapsed = time.time() - self._cooldowns[action_name]
            duration = self._durations.get(action_name, 0)
            
            if elapsed >= duration:
                # Cooldown terminé, nettoyer
                del self._cooldowns[action_name]
                return False
            
            return True
    
    def get_remaining(self, action_name: str) -> int:
        """Retourne le temps restant en secondes"""
        with self._lock:
            if action_name not in self._cooldowns:
                return 0
            
            elapsed = time.time() - self._cooldowns[action_name]
            duration = self._durations.get(action_name, 0)
            remaining = max(0, duration - elapsed)
            
            return int(remaining)
    
    def can_execute(self, action_name: str) -> Tuple[bool, int]:
        """
        Vérifie si une action peut être exécutée
        
        Returns:
            Tuple[bool, int]: (peut_executer, temps_restant)
        """
        remaining = self.get_remaining(action_name)
        return (remaining == 0, remaining)
    
    def reset(self, action_name: str):
        """Réinitialise un cooldown"""
        with self._lock:
            self._cooldowns.pop(action_name, None)
    
    def reset_all(self):
        """Réinitialise tous les cooldowns"""
        with self._lock:
            self._cooldowns.clear()
    
    def add_callback(self, action_name: str, callback: Callable):
        """Ajoute un callback appelé quand le cooldown se termine"""
        with self._lock:
            if action_name not in self._callbacks:
                self._callbacks[action_name] = []
            self._callbacks[action_name].append(callback)
    
    def get_all_active(self) -> Dict[str, int]:
        """Retourne tous les cooldowns actifs avec leur temps restant"""
        with self._lock:
            return {
                name: self.get_remaining(name)
                for name in self._cooldowns.keys()
                if self.is_active(name)
            }


# Instance globale singleton
cooldown_manager = CooldownManager()

# Enregistrer les cooldowns par défaut
cooldown_manager.register('clear_ram', 600)  # 10 minutes
cooldown_manager.register('quick_clean', 600)
cooldown_manager.register('create_restore_point', 600)
cooldown_manager.register('optimize_disk', 180)  # 3 minutes
cooldown_manager.register('empty_recycle', 600)
cooldown_manager.register('flush_dns', 600)
