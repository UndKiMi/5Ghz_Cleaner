"""
Système de logging pour 5GH'z Cleaner
Crée des logs détaillés de chaque opération de nettoyage
"""
import os
from datetime import datetime
from pathlib import Path


class CleaningLogger:
    """Gestionnaire de logs pour les opérations de nettoyage"""
    
    def __init__(self):
        # Créer le dossier de logs dans Documents
        self.logs_dir = Path.home() / "Documents" / "5GH'zCleaner-logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialiser la session
        self.session_start = datetime.now()
        self.session_id = self.session_start.strftime("%Y%m%d_%H%M%S")
        self.log_file = self.logs_dir / f"cleaning_{self.session_id}.txt"
        
        # Données de la session
        self.session_data = {
            "session_id": self.session_id,
            "start_time": self.session_start.isoformat(),
            "end_time": None,
            "duration_seconds": 0,
            "operations": [],
            "summary": {
                "total_files_deleted": 0,
                "total_space_freed_mb": 0,
                "operations_completed": 0,
                "operations_failed": 0,
            }
        }
        
        # Créer le fichier de log
        self._write_header()
    
    def _write_header(self):
        """Écrit l'en-tête du fichier de log"""
        header = f"""
{'='*80}
                    5GH'z CLEANER - RAPPORT DE NETTOYAGE
{'='*80}

Session ID      : {self.session_id}
Date et heure   : {self.session_start.strftime("%d/%m/%Y à %H:%M:%S")}
Utilisateur     : {os.getenv('USERNAME', 'Unknown')}
Ordinateur      : {os.getenv('COMPUTERNAME', 'Unknown')}

{'='*80}

"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(header)
    
    def log_operation_start(self, operation_name, description):
        """Enregistre le début d'une opération"""
        timestamp = datetime.now()
        
        operation = {
            "name": operation_name,
            "description": description,
            "start_time": timestamp.isoformat(),
            "end_time": None,
            "duration_seconds": 0,
            "status": "in_progress",
            "files_deleted": 0,
            "space_freed_mb": 0,
            "details": [],
            "errors": []
        }
        
        self.session_data["operations"].append(operation)
        
        # Écrire dans le fichier texte
        log_entry = f"\n[{timestamp.strftime('%H:%M:%S')}] 🔄 DÉBUT: {operation_name}\n"
        log_entry += f"   Description: {description}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        return len(self.session_data["operations"]) - 1  # Retourner l'index
    
    def log_operation_detail(self, operation_index, detail):
        """Ajoute un détail à une opération"""
        if 0 <= operation_index < len(self.session_data["operations"]):
            self.session_data["operations"][operation_index]["details"].append(detail)
            
            timestamp = datetime.now()
            log_entry = f"   [{timestamp.strftime('%H:%M:%S')}] ℹ️  {detail}\n"
            
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
    
    def log_operation_end(self, operation_index, files_deleted=0, space_freed_mb=0, success=True, error=None):
        """Enregistre la fin d'une opération"""
        if 0 <= operation_index < len(self.session_data["operations"]):
            operation = self.session_data["operations"][operation_index]
            end_time = datetime.now()
            start_time = datetime.fromisoformat(operation["start_time"])
            duration = (end_time - start_time).total_seconds()
            
            operation["end_time"] = end_time.isoformat()
            operation["duration_seconds"] = duration
            operation["status"] = "completed" if success else "failed"
            operation["files_deleted"] = files_deleted
            operation["space_freed_mb"] = space_freed_mb
            
            if error:
                operation["errors"].append(error)
            
            # Mettre à jour le résumé
            self.session_data["summary"]["total_files_deleted"] += files_deleted
            self.session_data["summary"]["total_space_freed_mb"] += space_freed_mb
            
            if success:
                self.session_data["summary"]["operations_completed"] += 1
            else:
                self.session_data["summary"]["operations_failed"] += 1
            
            # Écrire dans le fichier texte
            status_icon = "✅" if success else "❌"
            log_entry = f"   [{end_time.strftime('%H:%M:%S')}] {status_icon} FIN: {operation['name']}\n"
            log_entry += f"   Durée: {duration:.2f}s | Fichiers: {files_deleted} | Espace: {space_freed_mb:.2f} MB\n"
            
            if error:
                log_entry += f"   ⚠️  Erreur: {error}\n"
            
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
    
    def finalize(self):
        """Finalise le log et crée le résumé"""
        end_time = datetime.now()
        duration = (end_time - self.session_start).total_seconds()
        
        self.session_data["end_time"] = end_time.isoformat()
        self.session_data["duration_seconds"] = duration
        
        # Écrire le résumé dans le fichier texte
        summary = f"""
{'='*80}
                              RÉSUMÉ DU NETTOYAGE
{'='*80}

Durée totale           : {duration:.2f} secondes ({duration/60:.2f} minutes)
Opérations réussies    : {self.session_data["summary"]["operations_completed"]}
Opérations échouées    : {self.session_data["summary"]["operations_failed"]}

Fichiers supprimés     : {self.session_data["summary"]["total_files_deleted"]:,}
Espace libéré          : {self.session_data["summary"]["total_space_freed_mb"]:.2f} MB
                         ({self.session_data["summary"]["total_space_freed_mb"]/1024:.2f} GB)

{'='*80}

Détails par opération:
"""
        
        for op in self.session_data["operations"]:
            status_icon = "✅" if op["status"] == "completed" else "❌"
            summary += f"\n{status_icon} {op['name']}\n"
            summary += f"   Fichiers: {op['files_deleted']:,} | Espace: {op['space_freed_mb']:.2f} MB | Durée: {op['duration_seconds']:.2f}s\n"
            
            if op["errors"]:
                summary += f"   Erreurs: {', '.join(op['errors'])}\n"
        
        summary += f"\n{'='*80}\n"
        summary += f"Rapport généré le {end_time.strftime('%d/%m/%Y à %H:%M:%S')}\n"
        summary += f"Emplacement: {self.log_file}\n"
        summary += f"{'='*80}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"[INFO] Logs sauvegardés dans: {self.logs_dir}")
        print(f"[INFO] Fichier: {self.log_file.name}")
        
        return {
            "log_file": str(self.log_file),
            "logs_dir": str(self.logs_dir)
        }
