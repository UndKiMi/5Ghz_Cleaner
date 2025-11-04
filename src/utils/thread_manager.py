"""
Thread Manager - Gestion centralisée des threads
Optimisation: Réutilisation des threads, pool optimisé
"""
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Optional
import time


class ThreadManager:
    """Gestionnaire centralisé de threads avec pool optimisé"""
    
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
            # Pool de threads réutilisables (max 4 threads pour UI)
            self._executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="5GHz_")
            self._active_threads = {}
            self._thread_lock = threading.Lock()
            self._initialized = True
    
    def run_async(self, func: Callable, name: str = None, *args, **kwargs):
        """
        Exécute une fonction en arrière-plan de manière optimisée
        
        Args:
            func: Fonction à exécuter
            name: Nom du thread (optionnel)
            *args, **kwargs: Arguments de la fonction
        """
        if name and name in self._active_threads:
            # Thread déjà actif avec ce nom
            return None
        
        future = self._executor.submit(func, *args, **kwargs)
        
        if name:
            with self._thread_lock:
                self._active_threads[name] = future
                
                # Nettoyage automatique quand terminé
                def cleanup(_):
                    with self._thread_lock:
                        self._active_threads.pop(name, None)
                
                future.add_done_callback(cleanup)
        
        return future
    
    def is_running(self, name: str) -> bool:
        """Vérifie si un thread nommé est actif"""
        with self._thread_lock:
            return name in self._active_threads
    
    def wait_for(self, name: str, timeout: float = None) -> bool:
        """Attend la fin d'un thread nommé"""
        with self._thread_lock:
            future = self._active_threads.get(name)
        
        if future:
            try:
                future.result(timeout=timeout)
                return True
            except:
                return False
        return True
    
    def shutdown(self, wait: bool = True):
        """Arrête proprement tous les threads"""
        self._executor.shutdown(wait=wait)


# Instance globale singleton
thread_manager = ThreadManager()
