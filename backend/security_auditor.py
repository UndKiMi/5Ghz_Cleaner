"""
Module d'audit de sécurité automatique
Scanne les permissions, vérifie l'intégrité, détecte les modifications suspectes
Génère des rapports de sécurité complets

LECTURE SEULE: Ne modifie JAMAIS les permissions ou fichiers
"""
import os
import stat
import hashlib
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import importlib.util


class SecurityAuditor:
    """
    Auditeur de sécurité automatique en lecture seule.
    
    Features:
    - Scan des permissions de fichiers critiques
    - Vérification de l'intégrité des modules Python
    - Détection des modifications suspectes récentes
    - Génération de rapports de sécurité
    - Vérification de la signature des fichiers
    
    IMPORTANT: Toutes les opérations sont en LECTURE SEULE
    """
    
    def __init__(self):
        """Initialise l'auditeur de sécurité"""
        self.app_root = Path(__file__).parent.parent
        self.logger = logging.getLogger(__name__)
        
        # Fichiers critiques à auditer
        self.critical_files = [
            "main.py",
            "backend/security_core.py",
            "backend/cleaner.py",
            "backend/logger.py",
            "backend/signature_manager.py",
            "backend/system_commands.py",
            "config/settings.py",
            "config/constants.py",
        ]
        
        # Modules critiques à vérifier
        self.critical_modules = [
            "backend.security_core",
            "backend.cleaner",
            "backend.logger",
            "backend.signature_manager",
            "backend.system_commands",
            "config.settings",
        ]
    
    def scan_file_permissions(self) -> Dict:
        """
        Scanne les permissions des fichiers critiques.
        
        Vérifie:
        - Fichiers manquants
        - Permissions world-writable (risque)
        - Permissions exécutables suspectes
        
        Returns:
            Rapport des permissions avec issues détectées
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "files_checked": 0,
            "issues_found": 0,
            "warnings": 0,
            "details": []
        }
        
        for file_path in self.critical_files:
            full_path = self.app_root / file_path
            
            # Vérifier existence
            if not full_path.exists():
                report["issues_found"] += 1
                report["details"].append({
                    "file": file_path,
                    "issue": "File missing",
                    "severity": "critical",
                    "recommendation": "Restore file from backup or reinstall"
                })
                continue
            
            report["files_checked"] += 1
            
            try:
                # Obtenir les permissions
                file_stat = full_path.stat()
                mode = file_stat.st_mode
                
                # Vérifier si modifiable par tous (world-writable)
                if mode & stat.S_IWOTH:
                    report["issues_found"] += 1
                    report["details"].append({
                        "file": file_path,
                        "issue": "World-writable permissions detected",
                        "severity": "high",
                        "permissions": oct(mode)[-3:],
                        "recommendation": "Restrict write permissions to owner only"
                    })
                
                # Vérifier si exécutable (suspect pour fichiers Python)
                if mode & stat.S_IXUSR and file_path.endswith('.py'):
                    report["warnings"] += 1
                    report["details"].append({
                        "file": file_path,
                        "issue": "Executable permission on Python file",
                        "severity": "low",
                        "permissions": oct(mode)[-3:],
                        "recommendation": "Remove execute permission if not needed"
                    })
                
            except Exception as e:
                report["warnings"] += 1
                report["details"].append({
                    "file": file_path,
                    "issue": f"Failed to check permissions: {e}",
                    "severity": "medium"
                })
        
        return report
    
    def verify_module_integrity(self) -> Dict:
        """
        Vérifie l'intégrité des modules Python critiques.
        
        Vérifie:
        - Modules importables
        - Pas d'erreurs d'import
        - Modules non corrompus
        
        Returns:
            Rapport d'intégrité des modules
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "modules_checked": 0,
            "issues_found": 0,
            "details": []
        }
        
        for module_name in self.critical_modules:
            try:
                # Vérifier que le module peut être trouvé
                spec = importlib.util.find_spec(module_name)
                
                if spec is None:
                    report["issues_found"] += 1
                    report["details"].append({
                        "module": module_name,
                        "issue": "Module not found",
                        "severity": "critical",
                        "recommendation": "Check if file exists and Python path is correct"
                    })
                    continue
                
                # Vérifier que le module peut être importé
                try:
                    __import__(module_name)
                    report["modules_checked"] += 1
                    report["details"].append({
                        "module": module_name,
                        "status": "OK",
                        "severity": "none"
                    })
                except Exception as import_error:
                    report["issues_found"] += 1
                    report["details"].append({
                        "module": module_name,
                        "issue": f"Import failed: {import_error}",
                        "severity": "critical",
                        "recommendation": "Check module syntax and dependencies"
                    })
                    
            except Exception as e:
                report["issues_found"] += 1
                report["details"].append({
                    "module": module_name,
                    "issue": f"Verification failed: {e}",
                    "severity": "high"
                })
        
        return report
    
    def detect_suspicious_modifications(self, hours_threshold: int = 24) -> Dict:
        """
        Détecte les modifications suspectes récentes.
        
        Args:
            hours_threshold: Seuil en heures pour considérer une modification comme récente
        
        Returns:
            Rapport des modifications suspectes
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "threshold_hours": hours_threshold,
            "suspicious_count": 0,
            "details": []
        }
        
        cutoff_time = datetime.now() - timedelta(hours=hours_threshold)
        
        for file_path in self.critical_files:
            full_path = self.app_root / file_path
            
            if not full_path.exists():
                continue
            
            try:
                # Obtenir la date de modification
                mtime = datetime.fromtimestamp(full_path.stat().st_mtime)
                age_hours = (datetime.now() - mtime).total_seconds() / 3600
                
                if mtime > cutoff_time:
                    report["suspicious_count"] += 1
                    report["details"].append({
                        "file": file_path,
                        "modified": mtime.isoformat(),
                        "age_hours": round(age_hours, 2),
                        "severity": "medium" if age_hours < 1 else "low",
                        "warning": f"Modified {age_hours:.1f} hours ago",
                        "recommendation": "Verify if this modification was intentional"
                    })
                    
            except Exception as e:
                report["details"].append({
                    "file": file_path,
                    "issue": f"Failed to check modification time: {e}",
                    "severity": "low"
                })
        
        return report
    
    def verify_signature_integrity(self) -> Dict:
        """
        Vérifie l'intégrité via le système de signature.
        
        Returns:
            Rapport de vérification de signature
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "signature_valid": False,
            "details": []
        }
        
        try:
            from backend.signature_manager import signature_manager
            
            # Charger la signature
            signature = signature_manager.load_signature()
            
            if signature is None:
                report["details"].append({
                    "issue": "No signature file found",
                    "severity": "high",
                    "recommendation": "Generate signature with: py backend/signature_manager.py"
                })
                return report
            
            # Vérifier la signature
            is_valid, errors = signature_manager.verify_signature(signature)
            
            report["signature_valid"] = is_valid
            
            if is_valid:
                report["details"].append({
                    "status": "Signature valid",
                    "severity": "none",
                    "files_signed": len(signature.get("files", {}))
                })
            else:
                report["details"].append({
                    "issue": "Signature validation failed",
                    "severity": "critical",
                    "errors": errors,
                    "recommendation": "Check for unauthorized modifications"
                })
                
        except Exception as e:
            report["details"].append({
                "issue": f"Signature verification failed: {e}",
                "severity": "high"
            })
        
        return report
    
    def check_system_security(self) -> Dict:
        """
        Vérifie la sécurité du système.
        
        Returns:
            Rapport de sécurité système
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "checks": []
        }
        
        # Vérifier les privilèges admin
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            report["checks"].append({
                "check": "Administrator privileges",
                "status": "Yes" if is_admin else "No",
                "severity": "info",
                "note": "Some operations require admin rights"
            })
        except:
            pass
        
        # Vérifier Windows version
        try:
            import platform
            win_version = platform.version()
            report["checks"].append({
                "check": "Windows version",
                "status": win_version,
                "severity": "info"
            })
        except:
            pass
        
        # Vérifier espace disque
        try:
            import shutil
            disk_usage = shutil.disk_usage(self.app_root)
            free_gb = disk_usage.free / (1024**3)
            
            severity = "none"
            if free_gb < 5:
                severity = "high"
            elif free_gb < 10:
                severity = "medium"
            
            report["checks"].append({
                "check": "Free disk space",
                "status": f"{free_gb:.2f} GB",
                "severity": severity,
                "note": "Minimum 10 GB recommended"
            })
        except:
            pass
        
        return report
    
    def generate_security_report(self) -> Dict:
        """
        Génère un rapport de sécurité complet.
        
        Returns:
            Rapport complet avec tous les audits
        """
        self.logger.info("Generating comprehensive security audit report...")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "version": "1.0",
            "audits": {}
        }
        
        # Exécuter tous les audits
        print("\n" + "="*70)
        print("AUDIT DE SECURITE AUTOMATIQUE")
        print("="*70)
        
        print("\n[1/5] Scan des permissions...")
        report["audits"]["permissions"] = self.scan_file_permissions()
        print(f"   Fichiers verifies: {report['audits']['permissions']['files_checked']}")
        print(f"   Problemes trouves: {report['audits']['permissions']['issues_found']}")
        
        print("\n[2/5] Verification de l'integrite des modules...")
        report["audits"]["integrity"] = self.verify_module_integrity()
        print(f"   Modules verifies: {report['audits']['integrity']['modules_checked']}")
        print(f"   Problemes trouves: {report['audits']['integrity']['issues_found']}")
        
        print("\n[3/5] Detection des modifications suspectes...")
        report["audits"]["modifications"] = self.detect_suspicious_modifications()
        print(f"   Modifications recentes: {report['audits']['modifications']['suspicious_count']}")
        
        print("\n[4/5] Verification de la signature...")
        report["audits"]["signature"] = self.verify_signature_integrity()
        print(f"   Signature valide: {report['audits']['signature']['signature_valid']}")
        
        print("\n[5/5] Verification de la securite systeme...")
        report["audits"]["system"] = self.check_system_security()
        print(f"   Verifications: {len(report['audits']['system']['checks'])}")
        
        # Calculer score global
        total_issues = (
            report["audits"]["permissions"]["issues_found"] +
            report["audits"]["integrity"]["issues_found"] +
            report["audits"]["modifications"]["suspicious_count"]
        )
        
        signature_penalty = 0 if report["audits"]["signature"]["signature_valid"] else 10
        total_issues += signature_penalty
        
        report["summary"] = {
            "total_issues": total_issues,
            "status": "PASS" if total_issues == 0 else "FAIL",
            "severity": self._calculate_severity(total_issues),
            "recommendation": self._get_recommendation(total_issues)
        }
        
        # Afficher résumé
        print("\n" + "="*70)
        print("RESUME DE L'AUDIT")
        print("="*70)
        print(f"Problemes totaux: {total_issues}")
        print(f"Statut: {report['summary']['status']}")
        print(f"Severite: {report['summary']['severity']}")
        print(f"Recommandation: {report['summary']['recommendation']}")
        print("="*70)
        
        return report
    
    def _calculate_severity(self, issues_count: int) -> str:
        """Calcule la sévérité basée sur le nombre de problèmes"""
        if issues_count == 0:
            return "NONE"
        elif issues_count <= 2:
            return "LOW"
        elif issues_count <= 5:
            return "MEDIUM"
        elif issues_count <= 10:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def _get_recommendation(self, issues_count: int) -> str:
        """Retourne une recommandation basée sur le nombre de problèmes"""
        if issues_count == 0:
            return "System is secure"
        elif issues_count <= 2:
            return "Review minor issues"
        elif issues_count <= 5:
            return "Address issues soon"
        elif issues_count <= 10:
            return "Address issues immediately"
        else:
            return "URGENT: System may be compromised"


# Instance globale
security_auditor = SecurityAuditor()


if __name__ == "__main__":
    # Exécuter l'audit complet
    report = security_auditor.generate_security_report()
    
    # Sauvegarder le rapport
    report_file = Path(__file__).parent.parent / "security_audit_report.json"
    try:
        import json
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\nRapport sauvegarde: {report_file}")
    except Exception as e:
        print(f"\nErreur sauvegarde rapport: {e}")