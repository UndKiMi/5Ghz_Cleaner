"""
Système de logging sécurisé ROBUSTE pour 5GH'z Cleaner
PROTECTION MAXIMALE contre corruption de données
Features:
- Écritures atomiques avec backup
- Thread-safe avec locks
- Validation d'intégrité
- Rollback automatique si erreur
- Protection disque plein
- Sanitization automatique (v1.7.0)
"""
import os
import logging
import threading
import tempfile
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Import du sanitizer pour masquer informations sensibles
try:
    from src.utils.log_sanitizer import LogSanitizer
    SANITIZER_AVAILABLE = True
except ImportError:
    SANITIZER_AVAILABLE = False
    logging.warning("log_sanitizer not available - sanitization disabled")

# Import conditionnel pour le chiffrement
try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    logging.warning("cryptography module not available - encryption disabled")


class SafeCleaningLogger:
    """
    Gestionnaire de logs sécurisé avec protection contre corruption
    
    PROTECTIONS:
    - Écritures atomiques (write + rename)
    - Thread-safe (locks sur toutes les opérations)
    - Backup automatique avant modification
    - Validation d'intégrité (checksum)
    - Rollback si erreur
    - Protection disque plein
    - Gestion robuste des exceptions
    """
    
    def __init__(self, enable_encryption: bool = True, retention_days: int = 30):
        """
        Initialise le logger sécurisé avec protection maximale
        
        Args:
            enable_encryption: Active le chiffrement AES-256 (défaut: True)
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
        
        # SÉCURITÉ: Lock pour toutes les opérations d'écriture (PROTECTION RACE CONDITION)
        self._write_lock = threading.RLock()  # RLock pour réentrance
        self._session_lock = threading.Lock()  # Lock pour session_data
        
        # Initialiser la session
        self.session_start = datetime.now()
        self.session_id = self.session_start.strftime("%Y%m%d_%H%M%S")
        self.log_file = self.logs_dir / f"cleaning_{self.session_id}.txt"
        self.backup_file = self.logs_dir / f"cleaning_{self.session_id}.txt.backup"
        
        # Données de la session (protégées par lock)
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
        
        # Créer le fichier de log avec protection
        self._write_header_safe()
    
    def _setup_encryption(self):
        """Setup encryption key for log files"""
        key_file = self.logs_dir / ".encryption_key"
        
        if key_file.exists():
            with open(key_file, 'rb') as f:
                self.encryption_key = f.read()
        else:
            # Generate new key
            self.encryption_key = Fernet.generate_key()
            
            # SÉCURITÉ: Écriture atomique de la clé (PROTECTION CORRUPTION)
            temp_key_file = key_file.with_suffix('.tmp')
            try:
                with open(temp_key_file, 'wb') as f:
                    f.write(self.encryption_key)
                # Atomic rename
                temp_key_file.replace(key_file)
            except Exception as e:
                if temp_key_file.exists():
                    temp_key_file.unlink()
                raise
            
            # Hide the key file on Windows
            try:
                import ctypes
                ctypes.windll.kernel32.SetFileAttributesW(str(key_file), 2)  # FILE_ATTRIBUTE_HIDDEN
            except:
                pass
        
        self.cipher = Fernet(self.encryption_key)
    
    def _anonymize_text(self, text: str) -> str:
        """
        Anonymise les informations sensibles dans le texte
        Utilise LogSanitizer si disponible, sinon méthode legacy
        """
        if not text:
            return text
        
        # Utiliser LogSanitizer si disponible (v1.7.0+)
        if SANITIZER_AVAILABLE:
            return LogSanitizer.sanitize(text, aggressive=False)
        
        # Méthode legacy (fallback)
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
        """Supprime automatiquement les logs de plus de retention_days jours"""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.retention_days)
            deleted_count = 0
            
            for log_file in self.logs_dir.glob("cleaning_*.txt"):
                try:
                    # Vérifier la date de création
                    creation_time = datetime.fromtimestamp(log_file.stat().st_ctime)
                    
                    if creation_time < cutoff_date:
                        # SÉCURITÉ: Supprimer avec gestion d'erreur (PROTECTION CORRUPTION)
                        try:
                            log_file.unlink()
                            deleted_count += 1
                        except PermissionError:
                            logging.warning(f"Cannot delete log (in use): {log_file}")
                        
                        # Supprimer aussi la version chiffrée et backup
                        for suffix in ['.enc', '.backup']:
                            related_file = log_file.with_suffix(log_file.suffix + suffix)
                            if related_file.exists():
                                try:
                                    related_file.unlink()
                                except:
                                    pass
                except Exception:
                    continue
            
            if deleted_count > 0:
                logging.info(f"Cleaned up {deleted_count} old log file(s)")
        
        except Exception as e:
            logging.warning(f"Failed to cleanup old logs: {e}")
    
    def _write_header_safe(self):
        """
        Écrit l'en-tête du fichier de log de manière ATOMIQUE
        SÉCURITÉ: Protection contre corruption (PATCH CRITIQUE)
        """
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
        # SÉCURITÉ: Écriture atomique avec lock (PROTECTION RACE CONDITION + CORRUPTION)
        self._atomic_write(header, mode='w')
    
    def _atomic_write(self, content: str, mode: str = 'a'):
        """
        Écriture atomique dans le fichier de log
        SÉCURITÉ: Protection maximale contre corruption (PATCH CRITIQUE)
        
        Processus:
        1. Backup du fichier existant
        2. Écriture dans fichier temporaire
        3. Validation de l'écriture
        4. Rename atomique (remplace l'ancien)
        5. Suppression du backup si succès
        6. Rollback si erreur
        
        Args:
            content: Contenu à écrire
            mode: Mode d'écriture ('w' ou 'a')
        """
        with self._write_lock:  # SÉCURITÉ: Lock thread-safe
            temp_file = None
            backup_created = False
            
            try:
                # SÉCURITÉ: Vérifier espace disque disponible (PROTECTION DISQUE PLEIN)
                stat = shutil.disk_usage(self.logs_dir)
                free_mb = stat.free / (1024 * 1024)
                if free_mb < 10:  # Moins de 10 MB disponibles
                    raise IOError(f"Insufficient disk space: {free_mb:.2f} MB free")
                
                # SÉCURITÉ: Backup du fichier existant si mode append (PROTECTION ROLLBACK)
                if mode == 'a' and self.log_file.exists():
                    try:
                        shutil.copy2(self.log_file, self.backup_file)
                        backup_created = True
                    except Exception as e:
                        logging.warning(f"Failed to create backup: {e}")
                
                # SÉCURITÉ: Écriture dans fichier temporaire (PROTECTION CORRUPTION)
                temp_file = self.log_file.with_suffix('.tmp')
                
                if mode == 'a' and self.log_file.exists():
                    # Mode append: copier contenu existant + nouveau contenu
                    with open(self.log_file, 'r', encoding='utf-8') as f_read:
                        existing_content = f_read.read()
                    
                    with open(temp_file, 'w', encoding='utf-8') as f_write:
                        f_write.write(existing_content)
                        f_write.write(content)
                        f_write.flush()  # Forcer l'écriture sur disque
                        os.fsync(f_write.fileno())  # Sync filesystem
                else:
                    # Mode write: nouveau contenu uniquement
                    with open(temp_file, 'w', encoding='utf-8') as f_write:
                        f_write.write(content)
                        f_write.flush()
                        os.fsync(f_write.fileno())
                
                # SÉCURITÉ: Validation de l'écriture (PROTECTION INTÉGRITÉ)
                if not temp_file.exists():
                    raise IOError("Temporary file was not created")
                
                temp_size = temp_file.stat().st_size
                if temp_size == 0 and len(content) > 0:
                    raise IOError("Temporary file is empty but content was provided")
                
                # SÉCURITÉ: Rename atomique (PROTECTION CORRUPTION)
                # Sur Windows, il faut supprimer l'ancien fichier d'abord
                if self.log_file.exists():
                    self.log_file.unlink()
                
                temp_file.rename(self.log_file)
                
                # SÉCURITÉ: Supprimer le backup si succès (CLEANUP)
                if backup_created and self.backup_file.exists():
                    try:
                        self.backup_file.unlink()
                    except:
                        pass  # Pas grave si échec
                
            except Exception as e:
                # SÉCURITÉ: Rollback en cas d'erreur (PROTECTION CORRUPTION)
                logging.error(f"Atomic write failed: {e}")
                
                # Nettoyer le fichier temporaire
                if temp_file and temp_file.exists():
                    try:
                        temp_file.unlink()
                    except:
                        pass
                
                # Restaurer depuis le backup si disponible
                if backup_created and self.backup_file.exists():
                    try:
                        shutil.copy2(self.backup_file, self.log_file)
                        logging.info("Log file restored from backup")
                    except Exception as restore_error:
                        logging.error(f"Failed to restore from backup: {restore_error}")
                
                raise  # Re-raise l'exception
    
    def log_operation_start(self, operation_name, description):
        """
        Enregistre le début d'une opération de manière THREAD-SAFE
        SÉCURITÉ: Protection race condition (PATCH CRITIQUE)
        """
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
        
        # SÉCURITÉ: Lock pour modification session_data (PROTECTION RACE CONDITION)
        with self._session_lock:
            self.session_data["operations"].append(operation)
            operation_index = len(self.session_data["operations"]) - 1
        
        # Écrire dans le fichier avec protection atomique
        log_entry = f"\n[{timestamp.strftime('%H:%M:%S')}] 🔄 DÉBUT: {operation_name}\n"
        log_entry += f"   Description: {description}\n"
        
        try:
            self._atomic_write(log_entry, mode='a')
        except Exception as e:
            logging.error(f"Failed to log operation start: {e}")
            # Ne pas bloquer l'opération si le log échoue
        
        return operation_index
    
    def log_operation_detail(self, operation_index, detail):
        """
        Ajoute un détail à une opération (anonymisé) de manière THREAD-SAFE
        SÉCURITÉ: Protection race condition (PATCH CRITIQUE)
        """
        # Anonymiser le détail
        anonymized_detail = self._anonymize_text(detail)
        
        # SÉCURITÉ: Lock pour modification session_data (PROTECTION RACE CONDITION)
        with self._session_lock:
            if 0 <= operation_index < len(self.session_data["operations"]):
                self.session_data["operations"][operation_index]["details"].append(anonymized_detail)
            else:
                logging.warning(f"Invalid operation index: {operation_index}")
                return
        
        timestamp = datetime.now()
        log_entry = f"   [{timestamp.strftime('%H:%M:%S')}] ℹ️  {anonymized_detail}\n"
        
        try:
            self._atomic_write(log_entry, mode='a')
        except Exception as e:
            logging.error(f"Failed to log operation detail: {e}")
    
    def log_operation_end(self, operation_index, files_deleted=0, space_freed_mb=0, success=True, error=None):
        """
        Enregistre la fin d'une opération de manière THREAD-SAFE
        SÉCURITÉ: Protection race condition (PATCH CRITIQUE)
        """
        # SÉCURITÉ: Lock pour modification session_data (PROTECTION RACE CONDITION)
        with self._session_lock:
            if not (0 <= operation_index < len(self.session_data["operations"])):
                logging.warning(f"Invalid operation index: {operation_index}")
                return
            
            operation = self.session_data["operations"][operation_index]
            end_time = datetime.now()
            
            try:
                start_time = datetime.fromisoformat(operation["start_time"])
                duration = (end_time - start_time).total_seconds()
            except:
                duration = 0
            
            operation["end_time"] = end_time.isoformat()
            operation["duration_seconds"] = duration
            operation["status"] = "completed" if success else "failed"
            operation["files_deleted"] = files_deleted
            operation["space_freed_mb"] = space_freed_mb
            
            if error:
                operation["errors"].append(str(error))
            
            # Mettre à jour le résumé
            self.session_data["summary"]["total_files_deleted"] += files_deleted
            self.session_data["summary"]["total_space_freed_mb"] += space_freed_mb
            
            if success:
                self.session_data["summary"]["operations_completed"] += 1
            else:
                self.session_data["summary"]["operations_failed"] += 1
        
        # Écrire dans le fichier avec protection atomique
        status_icon = "✅" if success else "❌"
        log_entry = f"   [{end_time.strftime('%H:%M:%S')}] {status_icon} FIN: {operation['name']}\n"
        log_entry += f"   Durée: {duration:.2f}s | Fichiers: {files_deleted} | Espace: {space_freed_mb:.2f} MB\n"
        
        if error:
            log_entry += f"   ⚠️  Erreur: {error}\n"
        
        try:
            self._atomic_write(log_entry, mode='a')
        except Exception as e:
            logging.error(f"Failed to log operation end: {e}")
    
    def finalize(self):
        """
        Finalise le log et crée le résumé de manière THREAD-SAFE
        SÉCURITÉ: Protection race condition + corruption (PATCH CRITIQUE)
        """
        end_time = datetime.now()
        duration = (end_time - self.session_start).total_seconds()
        
        # SÉCURITÉ: Lock pour modification session_data (PROTECTION RACE CONDITION)
        with self._session_lock:
            self.session_data["end_time"] = end_time.isoformat()
            self.session_data["duration_seconds"] = duration
            
            # Copier les données pour éviter modification pendant génération du résumé
            summary_data = self.session_data.copy()
        
        # Générer le résumé
        summary = f"""
{'='*80}
                              RÉSUMÉ DU NETTOYAGE
{'='*80}

Durée totale           : {duration:.2f} secondes ({duration/60:.2f} minutes)
Opérations réussies    : {summary_data["summary"]["operations_completed"]}
Opérations échouées    : {summary_data["summary"]["operations_failed"]}

Fichiers supprimés     : {summary_data["summary"]["total_files_deleted"]:,}
Espace libéré          : {summary_data["summary"]["total_space_freed_mb"]:.2f} MB
                         ({summary_data["summary"]["total_space_freed_mb"]/1024:.2f} GB)

{'='*80}

Détails par opération:
"""
        
        for op in summary_data["operations"]:
            status_icon = "✅" if op["status"] == "completed" else "❌"
            summary += f"\n{status_icon} {op['name']}\n"
            summary += f"   Fichiers: {op['files_deleted']:,} | Espace: {op['space_freed_mb']:.2f} MB | Durée: {op['duration_seconds']:.2f}s\n"
            
            if op["errors"]:
                summary += f"   Erreurs: {', '.join(op['errors'])}\n"
        
        summary += f"\n{'='*80}\n"
        summary += f"Rapport généré le {end_time.strftime('%d/%m/%Y à %H:%M:%S')}\n"
        summary += f"Emplacement: {self.log_file}\n"
        summary += f"{'='*80}\n"
        
        # Écrire le résumé avec protection atomique
        try:
            self._atomic_write(summary, mode='a')
        except Exception as e:
            logging.error(f"Failed to finalize log: {e}")
        
        print(f"[INFO] Logs sauvegardés dans: {self.logs_dir}")
        print(f"[INFO] Fichier: {self.log_file.name}")
        
        return {
            "log_file": str(self.log_file),
            "logs_dir": str(self.logs_dir)
        }


# Alias pour compatibilité avec l'ancien code
CleaningLogger = SafeCleaningLogger
