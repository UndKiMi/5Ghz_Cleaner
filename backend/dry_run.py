"""
Dry-Run Module for 5GH'z Cleaner
Provides preview functionality without actually deleting files
"""
from backend import cleaner


class DryRunManager:
    """Gestionnaire de prévisualisation de nettoyage"""
    
    def __init__(self):
        self.preview_data = {
            "total_files": 0,
            "total_size_bytes": 0,
            "total_size_mb": 0,
            "operations": []
        }
    
    def preview_full_cleaning(self, options=None):
        """
        Prévisualise un nettoyage complet sans supprimer
        
        Args:
            options (dict): Options de nettoyage avancées
        
        Returns:
            dict: Rapport de prévisualisation détaillé
        """
        # IMPORTANT: Réinitialiser les données à chaque appel pour éviter l'accumulation
        self.preview_data = {
            "total_files": 0,
            "total_size_bytes": 0,
            "total_size_mb": 0,
            "operations": []
        }
        
        if options is None:
            options = {
                "clear_standby_memory": True,
                "flush_dns": True,
                "disable_telemetry": False,
                "clear_large_logs": True
            }
        
        print("="*80)
        print("MODE DRY-RUN - PRÉVISUALISATION DU NETTOYAGE")
        print("="*80)
        print("[INFO] Aucun fichier ne sera supprimé")
        print()
        
        # 1. Fichiers temporaires
        print("[1/8] Analyse des fichiers temporaires...")
        temp_result = cleaner.clear_temp(dry_run=True)
        self._add_operation("Fichiers temporaires", temp_result)
        
        # 2. Cache Windows Update (simulation)
        print("[2/8] Analyse du cache Windows Update...")
        # Note: Nécessite adaptation de la fonction
        self._add_operation("Cache Windows Update", {
            "temp_deleted": 0,
            "dry_run": True,
            "note": "Analyse non implémentée - nécessite droits admin"
        })
        
        # 3. Prefetch (simulation)
        print("[3/8] Analyse du prefetch...")
        self._add_operation("Prefetch", {
            "prefetch_cleared": 0,
            "dry_run": True,
            "note": "Analyse non implémentée"
        })
        
        # 4. Historique récent (simulation)
        print("[4/8] Analyse de l'historique récent...")
        self._add_operation("Historique récent", {
            "recent_cleared": 0,
            "dry_run": True,
            "note": "Analyse non implémentée"
        })
        
        # 5. Cache miniatures (simulation)
        print("[5/8] Analyse du cache miniatures...")
        self._add_operation("Cache miniatures", {
            "thumbs_cleared": 0,
            "dry_run": True,
            "note": "Analyse non implémentée"
        })
        
        # 6. Dumps de crash (simulation)
        print("[6/8] Analyse des dumps de crash...")
        self._add_operation("Dumps de crash", {
            "dumps_deleted": 0,
            "dry_run": True,
            "note": "Analyse non implémentée"
        })
        
        # 7. Windows.old (simulation)
        print("[7/8] Vérification de Windows.old...")
        import os
        windows_old_path = os.path.normpath(os.path.join(os.getenv('WINDIR', 'C:\\Windows'), '..', 'Windows.old'))
        if os.path.isdir(windows_old_path):
            try:
                size = sum(os.path.getsize(os.path.join(dirpath, filename))
                          for dirpath, dirnames, filenames in os.walk(windows_old_path)
                          for filename in filenames)
                self._add_operation("Windows.old", {
                    "windows_old_deleted": 1,
                    "size_bytes": size,
                    "size_mb": size / (1024 * 1024),
                    "dry_run": True,
                    "warning": "ATTENTION: Supprime la possibilité de rollback Windows!"
                })
            except:
                self._add_operation("Windows.old", {
                    "windows_old_deleted": 0,
                    "dry_run": True,
                    "note": "Impossible d'analyser"
                })
        else:
            self._add_operation("Windows.old", {
                "windows_old_deleted": 0,
                "dry_run": True,
                "note": "Dossier non trouvé"
            })
        
        # 8. Corbeille (simulation)
        print("[8/8] Analyse de la corbeille...")
        try:
            recycle_count = cleaner.get_recycle_bin_count()
            self._add_operation("Corbeille", {
                "recycle_bin_deleted": recycle_count,
                "dry_run": True,
                "warning": "Suppression définitive sans récupération possible!"
            })
        except:
            self._add_operation("Corbeille", {
                "recycle_bin_deleted": 0,
                "dry_run": True,
                "note": "Impossible de compter les éléments"
            })
        
        # Calculer totaux
        self._calculate_totals()
        
        # Afficher rapport
        self._print_report()
        
        return self.preview_data
    
    def _add_operation(self, name, result):
        """Ajoute une opération au rapport"""
        operation = {
            "name": name,
            "result": result
        }
        
        # Extraire statistiques
        if "temp_deleted" in result:
            operation["files_count"] = result["temp_deleted"]
        elif "prefetch_cleared" in result:
            operation["files_count"] = result["prefetch_cleared"]
        elif "recent_cleared" in result:
            operation["files_count"] = result["recent_cleared"]
        elif "thumbs_cleared" in result:
            operation["files_count"] = result["thumbs_cleared"]
        elif "dumps_deleted" in result:
            operation["files_count"] = result["dumps_deleted"]
        elif "windows_old_deleted" in result:
            operation["files_count"] = result["windows_old_deleted"]
        elif "recycle_bin_deleted" in result:
            operation["files_count"] = result["recycle_bin_deleted"]
        else:
            operation["files_count"] = 0
        
        # Extraire taille
        if "total_size_mb" in result:
            operation["size_mb"] = result["total_size_mb"]
        elif "size_mb" in result:
            operation["size_mb"] = result["size_mb"]
        else:
            operation["size_mb"] = 0
        
        self.preview_data["operations"].append(operation)
    
    def _calculate_totals(self):
        """Calcule les totaux"""
        for op in self.preview_data["operations"]:
            self.preview_data["total_files"] += op.get("files_count", 0)
            self.preview_data["total_size_mb"] += op.get("size_mb", 0)
        
        self.preview_data["total_size_bytes"] = self.preview_data["total_size_mb"] * 1024 * 1024
    
    def _print_report(self):
        """Affiche le rapport de prévisualisation"""
        print()
        print("="*80)
        print("RAPPORT DE PRÉVISUALISATION")
        print("="*80)
        print()
        
        for op in self.preview_data["operations"]:
            files = op.get("files_count", 0)
            size = op.get("size_mb", 0)
            warning = op["result"].get("warning", "")
            note = op["result"].get("note", "")
            
            print(f"[{op['name']}]")
            print(f"  Fichiers/Éléments: {files:,}")
            if size > 0:
                print(f"  Espace libéré: {size:.2f} MB ({size/1024:.2f} GB)")
            if warning:
                print(f"  [WARN] AVERTISSEMENT: {warning}")
            if note:
                print(f"  [INFO] Note: {note}")
            print()
        
        print("="*80)
        print("TOTAUX")
        print("="*80)
        print(f"Fichiers/Éléments total: {self.preview_data['total_files']:,}")
        print(f"Espace total à libérer: {self.preview_data['total_size_mb']:.2f} MB")
        print(f"                       ({self.preview_data['total_size_mb']/1024:.2f} GB)")
        print("="*80)
        print()
        print("[INFO] Ceci est une PRÉVISUALISATION - Aucun fichier n'a été supprimé")
        print("[INFO] Pour effectuer le nettoyage réel, lancez le mode normal")
        print("="*80)


# Instance globale
dry_run_manager = DryRunManager()
