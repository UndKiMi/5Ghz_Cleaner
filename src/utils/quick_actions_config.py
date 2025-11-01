"""
Module de configuration des actions rapides personnalisables
Permet à l'utilisateur de choisir quelles actions afficher dans l'onglet "Nettoyage rapide"
"""

import json
import os
from pathlib import Path
from typing import List, Dict

# Chemin du fichier de configuration
CONFIG_DIR = Path.home() / "AppData" / "Local" / "5GHz_Cleaner"
CONFIG_FILE = CONFIG_DIR / "quick_actions_config.json"

# Actions disponibles avec leurs métadonnées
AVAILABLE_ACTIONS = {
    "restore_point": {
        "id": "restore_point",
        "icon": "RESTORE_ROUNDED",
        "title": "Point de restauration",
        "description": "Crée une sauvegarde du système.",
        "category": "Sécurité",
        "recommended": True,
    },
    "optimize_disk": {
        "id": "optimize_disk",
        "icon": "STORAGE_ROUNDED",
        "title": "Optimisation Disque dur",
        "description": "Optimise et fluidifie le disque.",
        "category": "Performance",
        "recommended": True,
    },
    "empty_recycle": {
        "id": "empty_recycle",
        "icon": "DELETE_SWEEP_ROUNDED",
        "title": "Vider la corbeille",
        "description": "Supprime définitivement les éléments.",
        "category": "Nettoyage",
        "recommended": True,
    },
    "flush_dns": {
        "id": "flush_dns",
        "icon": "DNS_ROUNDED",
        "title": "Flush DNS",
        "description": "Réinitialise le cache DNS.",
        "category": "Réseau",
        "recommended": True,
    },
    "clear_temp": {
        "id": "clear_temp",
        "icon": "CLEANING_SERVICES_ROUNDED",
        "title": "Nettoyer fichiers temp",
        "description": "Supprime les fichiers temporaires.",
        "category": "Nettoyage",
        "recommended": False,
    },
    "clear_prefetch": {
        "id": "clear_prefetch",
        "icon": "SPEED_ROUNDED",
        "title": "Vider Prefetch",
        "description": "Nettoie le cache de préchargement.",
        "category": "Performance",
        "recommended": False,
    },
    "disable_telemetry": {
        "id": "disable_telemetry",
        "icon": "PRIVACY_TIP_ROUNDED",
        "title": "Désactiver télémétrie",
        "description": "Désactive la collecte de données Windows.",
        "category": "Confidentialité",
        "recommended": False,
    },
    "clear_logs": {
        "id": "clear_logs",
        "icon": "DESCRIPTION_ROUNDED",
        "title": "Nettoyer logs système",
        "description": "Supprime les fichiers logs volumineux.",
        "category": "Nettoyage",
        "recommended": False,
    },
    "clear_ram": {
        "id": "clear_ram",
        "icon": "MEMORY_ROUNDED",
        "title": "Vider RAM Standby",
        "description": "Libère la mémoire en attente.",
        "category": "Performance",
        "recommended": False,
    },
    "network_reset": {
        "id": "network_reset",
        "icon": "WIFI_ROUNDED",
        "title": "Réinitialiser réseau",
        "description": "Reset complet de la configuration réseau.",
        "category": "Réseau",
        "recommended": False,
    },
}

# Configuration par défaut (4 actions affichées)
DEFAULT_QUICK_ACTIONS = [
    "restore_point",
    "optimize_disk",
    "empty_recycle",
    "flush_dns",
]


class QuickActionsConfig:
    """Gestionnaire de configuration des actions rapides"""
    
    def __init__(self):
        self.config_file = CONFIG_FILE
        self.ensure_config_dir()
        self.load_config()
    
    def ensure_config_dir(self):
        """Crée le répertoire de configuration s'il n'existe pas"""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    def load_config(self) -> List[str]:
        """
        Charge la configuration depuis le fichier JSON
        
        Returns:
            Liste des IDs d'actions actives
        """
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.active_actions = data.get('active_actions', DEFAULT_QUICK_ACTIONS.copy())
                    
                    # Validation: s'assurer que les actions existent
                    self.active_actions = [
                        action_id for action_id in self.active_actions
                        if action_id in AVAILABLE_ACTIONS
                    ]
                    
                    # Si moins de 4 actions, compléter avec les actions par défaut
                    if len(self.active_actions) < 4:
                        for default_action in DEFAULT_QUICK_ACTIONS:
                            if default_action not in self.active_actions:
                                self.active_actions.append(default_action)
                            if len(self.active_actions) >= 4:
                                break
            else:
                self.active_actions = DEFAULT_QUICK_ACTIONS.copy()
                self.save_config()
        except Exception as e:
            print(f"[ERROR] Failed to load quick actions config: {e}")
            self.active_actions = DEFAULT_QUICK_ACTIONS.copy()
        
        return self.active_actions
    
    def save_config(self):
        """Sauvegarde la configuration dans le fichier JSON"""
        try:
            data = {
                'active_actions': self.active_actions,
                'version': '1.0'
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"[INFO] Quick actions config saved: {self.active_actions}")
        except Exception as e:
            print(f"[ERROR] Failed to save quick actions config: {e}")
    
    def get_active_actions(self) -> List[Dict]:
        """
        Retourne les actions actives avec leurs métadonnées
        
        Returns:
            Liste de dictionnaires contenant les infos des actions
        """
        return [
            AVAILABLE_ACTIONS[action_id]
            for action_id in self.active_actions
            if action_id in AVAILABLE_ACTIONS
        ]
    
    def get_available_actions(self) -> List[Dict]:
        """
        Retourne toutes les actions disponibles
        
        Returns:
            Liste de dictionnaires contenant les infos de toutes les actions
        """
        return list(AVAILABLE_ACTIONS.values())
    
    def set_active_actions(self, action_ids: List[str]):
        """
        Définit les actions actives
        
        Args:
            action_ids: Liste des IDs d'actions à activer (max 4)
        """
        # Valider et limiter à 4 actions
        valid_actions = [
            action_id for action_id in action_ids
            if action_id in AVAILABLE_ACTIONS
        ][:4]
        
        # S'assurer qu'on a au moins 4 actions
        if len(valid_actions) < 4:
            for default_action in DEFAULT_QUICK_ACTIONS:
                if default_action not in valid_actions:
                    valid_actions.append(default_action)
                if len(valid_actions) >= 4:
                    break
        
        self.active_actions = valid_actions
        self.save_config()
    
    def reset_to_default(self):
        """Réinitialise la configuration aux valeurs par défaut"""
        self.active_actions = DEFAULT_QUICK_ACTIONS.copy()
        self.save_config()


# Instance globale
quick_actions_config = QuickActionsConfig()
