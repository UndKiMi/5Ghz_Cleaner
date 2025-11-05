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
            "clear_large_logs",              # Nettoyer logs volumineux
            "optimize_pagefile",             # Optimiser fichier de pagination
            "optimize_startup",              # Optimiser programmes au démarrage
            "clean_drivers",                 # Nettoyer pilotes obsolètes
            "clean_windows_update_temp",     # Nettoyer dossiers temporaires Windows Update
            "clean_orphan_files",            # Nettoyer fichiers orphelins
            "schedule_cleaning",             # 🆕 Planification du nettoyage automatique
            "clean_store_cache",             # 🆕 Nettoyer cache Windows Store
            "optimize_windows_search",       # 🆕 Optimiser base de données Windows Search
        ],
        "warning": [
            "disable_telemetry",             # Désactiver télémétrie
            "clear_browser_cache",           # Vider cache des navigateurs
            "clean_event_logs",              # Nettoyer logs d'événements
            "disable_superfetch",            # Désactiver Superfetch/Prefetch
            "disable_cortana",               # Désactiver Cortana
            "disable_services",              # Désactiver services inutiles
            "system_repair",                 # Analyse et réparation système (SFC/DISM)
            "optimize_registry",             # Optimiser registre (clés non critiques)
            "advanced_services_management",  # Gestion avancée services Windows
        ],
        "danger": [
            "disable_hibernation",           # Désactiver l'hibernation
            "clean_restore_points",          # Nettoyer points de restauration anciens
            "clean_winsxs",                  # Vider WinSxS
            "full_network_reset",            # Réinitialisation complète réseau
            "full_system_cache_clean",       # Nettoyage complet cache système
        ],
    }
