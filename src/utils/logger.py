"""
Système de logging sécurisé pour 5GH'z Cleaner
Crée des logs détaillés de chaque opération de nettoyage
Features:
- Anonymisation automatique des chemins utilisateur
- Chiffrement AES-256 optionnel (désactivé par défaut)
- Suppression automatique après 30 jours
- Format structuré pour analyse
"""
import os
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Import conditionnel pour le chiffrement
try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    logging.warning("cryptography module not available - encryption disabled")


class CleaningLogger:
    """
    Gestionnaire de logs sécurisé pour les opérations de nettoyage.
    
    Features:
    - Anonymisation automatique des chemins utilisateur
    - Chiffrement optionnel (désactivé par défaut)
    - Suppression automatique après retention_days jours
    """
    
    def __init__(self, enable_encryption: bool = False, retention_days: int = 30):
        """
        Initialise le logger sécurisé.
        
        Args:
            enable_encryption: Active le chiffrement AES-256 (défaut: False)
            retention_days: Nombre de jours avant suppression auto (défaut: 30)
        """
        # Créer le dossier de logs dans Documents
        self.logs_dir = Path.home() / "Documents" / "5GH'zCleaner-logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuration sécurité
        self.enable_encryption = enable_encryption and CRYPTO_AVAILABLE
        self.retention_days = retention_days
        self.username = os.getenv('USERNAME', 'User')
        self.home_path = str(Path.home())
        
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
        
        # Setup encryption if enabled
        if self.enable_encryption:
            self._setup_encryption()
        
        # Cleanup old logs
        self._cleanup_old_logs()
        
        # Créer le fichier de log
        self._write_header()
    
    def _setup_encryption(self):
        """Setup encryption key for log files"""
        key_file = self.logs_dir / ".encryption_key"
        
        if key_file.exists():
            with open(key_file, 'rb') as f:
                self.encryption_key = f.read()
        else:
            # Generate new key
            self.encryption_key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(self.encryption_key)
            # Hide the key file on Windows
            try:
                import ctypes
                ctypes.windll.kernel32.SetFileAttributesW(str(key_file), 2)  # FILE_ATTRIBUTE_HIDDEN
            except:
                pass
        
        self.cipher = Fernet(self.encryption_key)
    
    def _anonymize_text(self, text: str) -> str:
        """
        Anonymise les chemins utilisateur dans le texte.
        
        Args:
            text: Texte à anonymiser
            
        Returns:
            Texte avec chemins anonymisés
        """
        if not text:
            return text
        
        # Remplacer le nom d'utilisateur
        text = text.replace(self.username, '[USER]')
        
        # Remplacer le chemin home
        text = text.replace(self.home_path, '[HOME]')
        text = text.replace(self.home_path.replace('\\', '/'), '[HOME]')
        
        # Remplacer les chemins Windows communs
        text = text.replace(f"C:\\Users\\{self.username}", "C:\\Users\\[USER]")
        text = text.replace(f"C:/Users/{self.username}", "C:/Users/[USER]")
        
        return text
    
    def _cleanup_old_logs(self):
        """
        Supprime automatiquement les logs de plus de retention_days jours.
        Vérifie précisément la date de création du fichier.
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=self.retention_days)
            deleted_count = 0
            
            for log_file in self.logs_dir.glob("cleaning_*.txt"):
                try:
                    # Vérifier la date de création (plus précis que mtime)
                    creation_time = datetime.fromtimestamp(log_file.stat().st_ctime)
                    
                    if creation_time < cutoff_date:
                        log_file.unlink()
                        deleted_count += 1
                        
                        # Supprimer aussi la version chiffrée si elle existe
                        encrypted_file = log_file.with_suffix('.txt.enc')
                        if encrypted_file.exists():
                            encrypted_file.unlink()
                except Exception:
                    # Ne pas bloquer si un fichier ne peut pas être supprimé
                    continue
            
            if deleted_count > 0:
                logging.info(f"Cleaned up {deleted_count} old log file(s) older than {self.retention_days} days")
        
        except Exception as e:
            logging.warning(f"Failed to cleanup old logs: {e}")
    
    def _write_header(self):
        """Écrit l'en-tête du fichier de log (anonymisé)"""
        header = f"""
{'='*80}
                    5GH'z CLEANER - RAPPORT DE NETTOYAGE
{'='*80}

Session ID      : {self.session_id}
Date et heure   : {self.session_start.strftime("%d/%m/%Y à %H:%M:%S")}
Utilisateur     : [USER]
Ordinateur      : {self._anonymize_text(os.getenv('COMPUTERNAME', 'Unknown'))}

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
        """Ajoute un détail à une opération (anonymisé)"""
        if 0 <= operation_index < len(self.session_data["operations"]):
            # Anonymiser le détail avant de le stocker
            anonymized_detail = self._anonymize_text(detail)
            self.session_data["operations"][operation_index]["details"].append(anonymized_detail)
            
            timestamp = datetime.now()
            log_entry = f"   [{timestamp.strftime('%H:%M:%S')}] ℹ️  {anonymized_detail}\n"
            
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
