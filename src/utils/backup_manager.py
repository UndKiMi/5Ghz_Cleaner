"""
Module de gestion des backups avant suppression
Permet un rollback en cas d'erreur
"""
import os
import shutil
import tempfile
import time
from pathlib import Path
from datetime import datetime


class BackupManager:
    """Gestionnaire de backups pour les fichiers supprimés"""
    
    def __init__(self, backup_dir: str = None):
        """
        Initialise le gestionnaire de backups
        
        Args:
            backup_dir: Dossier de backup (auto-créé si None)
        """
        if backup_dir is None:
            # Créer un dossier de backup dans le temp
            self.backup_root = os.path.join(tempfile.gettempdir(), '5ghz_backup')
        else:
            self.backup_root = backup_dir
        
        # Créer un sous-dossier avec timestamp pour cette session
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.session_backup_dir = os.path.join(self.backup_root, f'session_{timestamp}')
        
        # Créer le dossier
        os.makedirs(self.session_backup_dir, exist_ok=True)
        
        # Statistiques
        self.backed_up_files = []
        self.total_size = 0
    
    def backup_file(self, file_path: str) -> tuple[bool, str]:
        """
        Sauvegarde un fichier avant suppression
        
        Args:
            file_path: Chemin du fichier à sauvegarder
            
        Returns:
            tuple: (success, backup_path or error_message)
        """
        try:
            if not os.path.exists(file_path):
                return False, "File does not exist"
            
            # Créer un nom unique pour le backup
            filename = os.path.basename(file_path)
            # Ajouter un hash du chemin complet pour éviter les collisions
            import hashlib
            path_hash = hashlib.md5(file_path.encode()).hexdigest()[:8]
            backup_filename = f"{path_hash}_{filename}"
            
            backup_path = os.path.join(self.session_backup_dir, backup_filename)
            
            # Copier le fichier
            shutil.copy2(file_path, backup_path)
            
            # Enregistrer les métadonnées
            file_size = os.path.getsize(file_path)
            self.backed_up_files.append({
                'original_path': file_path,
                'backup_path': backup_path,
                'size': file_size,
                'timestamp': time.time()
            })
            self.total_size += file_size
            
            return True, backup_path
            
        except Exception as e:
            return False, f"Backup failed: {e}"
    
    def backup_directory(self, dir_path: str) -> tuple[bool, str]:
        """
        Sauvegarde un dossier avant suppression
        
        Args:
            dir_path: Chemin du dossier à sauvegarder
            
        Returns:
            tuple: (success, backup_path or error_message)
        """
        try:
            if not os.path.exists(dir_path):
                return False, "Directory does not exist"
            
            # Créer un nom unique pour le backup
            dirname = os.path.basename(dir_path)
            import hashlib
            path_hash = hashlib.md5(dir_path.encode()).hexdigest()[:8]
            backup_dirname = f"{path_hash}_{dirname}"
            
            backup_path = os.path.join(self.session_backup_dir, backup_dirname)
            
            # Copier le dossier récursivement
            shutil.copytree(dir_path, backup_path)
            
            # Calculer la taille totale
            dir_size = sum(os.path.getsize(os.path.join(dirpath, filename))
                          for dirpath, dirnames, filenames in os.walk(backup_path)
                          for filename in filenames)
            
            # Enregistrer les métadonnées
            self.backed_up_files.append({
                'original_path': dir_path,
                'backup_path': backup_path,
                'size': dir_size,
                'timestamp': time.time(),
                'is_directory': True
            })
            self.total_size += dir_size
            
            return True, backup_path
            
        except Exception as e:
            return False, f"Backup failed: {e}"
    
    def restore_file(self, original_path: str) -> tuple[bool, str]:
        """
        Restaure un fichier depuis le backup
        
        Args:
            original_path: Chemin original du fichier
            
        Returns:
            tuple: (success, message)
        """
        try:
            # Trouver le backup correspondant
            backup_info = None
            for info in self.backed_up_files:
                if info['original_path'] == original_path:
                    backup_info = info
                    break
            
            if backup_info is None:
                return False, "No backup found for this file"
            
            backup_path = backup_info['backup_path']
            
            if not os.path.exists(backup_path):
                return False, "Backup file not found"
            
            # Restaurer le fichier
            if backup_info.get('is_directory', False):
                shutil.copytree(backup_path, original_path)
            else:
                shutil.copy2(backup_path, original_path)
            
            return True, f"File restored from {backup_path}"
            
        except Exception as e:
            return False, f"Restore failed: {e}"
    
    def restore_all(self) -> tuple[int, int]:
        """
        Restaure tous les fichiers backupés
        
        Returns:
            tuple: (success_count, fail_count)
        """
        success = 0
        failed = 0
        
        for info in self.backed_up_files:
            is_success, message = self.restore_file(info['original_path'])
            if is_success:
                success += 1
            else:
                failed += 1
                print(f"[ERROR] Failed to restore {info['original_path']}: {message}")
        
        return success, failed
    
    def cleanup_old_backups(self, days: int = 7):
        """
        Nettoie les backups de plus de X jours
        
        Args:
            days: Nombre de jours à conserver
        """
        try:
            if not os.path.exists(self.backup_root):
                return
            
            current_time = time.time()
            cutoff_time = current_time - (days * 24 * 60 * 60)
            
            for session_dir in os.listdir(self.backup_root):
                session_path = os.path.join(self.backup_root, session_dir)
                
                if not os.path.isdir(session_path):
                    continue
                
                # Vérifier l'âge du dossier
                dir_mtime = os.path.getmtime(session_path)
                
                if dir_mtime < cutoff_time:
                    print(f"[INFO] Removing old backup: {session_dir}")
                    shutil.rmtree(session_path, ignore_errors=True)
                    
        except Exception as e:
            print(f"[WARNING] Failed to cleanup old backups: {e}")
    
    def get_backup_stats(self) -> dict:
        """
        Obtient les statistiques des backups
        
        Returns:
            dict: Statistiques
        """
        return {
            'session_dir': self.session_backup_dir,
            'files_backed_up': len(self.backed_up_files),
            'total_size_bytes': self.total_size,
            'total_size_mb': self.total_size / (1024 * 1024),
            'files': self.backed_up_files
        }
    
    def save_manifest(self):
        """Sauvegarde un manifeste des fichiers backupés"""
        try:
            manifest_path = os.path.join(self.session_backup_dir, 'manifest.txt')
            
            with open(manifest_path, 'w', encoding='utf-8') as f:
                f.write(f"5GH'z Cleaner Backup Manifest\n")
                f.write(f"Session: {os.path.basename(self.session_backup_dir)}\n")
                f.write(f"Total files: {len(self.backed_up_files)}\n")
                f.write(f"Total size: {self.total_size / (1024 * 1024):.2f} MB\n")
                f.write(f"\n{'='*80}\n\n")
                
                for info in self.backed_up_files:
                    f.write(f"Original: {info['original_path']}\n")
                    f.write(f"Backup: {info['backup_path']}\n")
                    f.write(f"Size: {info['size']} bytes\n")
                    f.write(f"Time: {datetime.fromtimestamp(info['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"{'-'*80}\n")
            
            print(f"[INFO] Backup manifest saved: {manifest_path}")
            
        except Exception as e:
            print(f"[WARNING] Failed to save manifest: {e}")


# Instance globale (optionnelle)
_global_backup_manager = None


def get_backup_manager() -> BackupManager:
    """Obtient l'instance globale du backup manager"""
    global _global_backup_manager
    if _global_backup_manager is None:
        _global_backup_manager = BackupManager()
    return _global_backup_manager


# Fonction helper
def backup_before_delete(file_path: str) -> tuple[bool, str]:
    """
    Fonction helper pour backup rapide
    
    Args:
        file_path: Chemin du fichier à sauvegarder
        
    Returns:
        tuple: (success, backup_path or error_message)
    """
    manager = get_backup_manager()
    
    if os.path.isdir(file_path):
        return manager.backup_directory(file_path)
    else:
        return manager.backup_file(file_path)


if __name__ == "__main__":
    # Test du module
    print("=== Backup Manager Test ===\n")
    
    manager = BackupManager()
    print(f"Backup directory: {manager.session_backup_dir}")
    
    # Test backup d'un fichier
    test_file = r"C:\Windows\Temp\test.txt"
    if os.path.exists(test_file):
        success, result = manager.backup_file(test_file)
        print(f"Backup result: {success} - {result}")
    
    # Afficher les stats
    stats = manager.get_backup_stats()
    print(f"\nBackup stats:")
    print(f"  Files: {stats['files_backed_up']}")
    print(f"  Size: {stats['total_size_mb']:.2f} MB")
