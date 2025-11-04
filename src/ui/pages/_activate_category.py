"""
Fonction d'activation rapide par catégorie pour les options avancées
"""

def get_category_actions():
    """
    Retourne le mapping des actions par catégorie de risque
    
    Returns:
        Dict: Mapping catégorie -> liste de clés d'actions
    """
    return {
        "safe": [
            "clear_standby_memory",  # Libérer RAM Standby
            "flush_dns",              # Flush DNS
            "clear_large_logs",       # Nettoyer logs volumineux
            "gaming_mode",            # Mode Gaming
            "optimize_pagefile",      # Optimiser fichier de pagination
        ],
        "warning": [
            "disable_telemetry",      # Désactiver télémétrie
            "clear_browser_cache",    # Vider cache des navigateurs
            "clean_event_logs",       # Nettoyer logs d'événements
            "disable_superfetch",     # Désactiver Superfetch/Prefetch
            "disable_cortana",        # Désactiver Cortana
            "optimize_tcp_ip",        # Optimiser TCP/IP
            "disable_services",       # Désactiver services inutiles
            "clean_drivers",          # Nettoyer pilotes obsolètes
            "optimize_startup",       # Optimiser programmes au démarrage
        ],
        "danger": [
            "disable_hibernation",    # Désactiver l'hibernation
            "clean_restore_points",   # Nettoyer points de restauration anciens
            "clean_winsxs",           # Vider WinSxS
        ],
    }
