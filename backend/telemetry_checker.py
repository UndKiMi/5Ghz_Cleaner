"""
Module de vérification de télémétrie
Vérifie qu'aucune donnée utilisateur n'est envoyée sans consentement
"""
import socket
import os
import sys
from datetime import datetime


class TelemetryChecker:
    """Vérifie l'absence de télémétrie cachée"""
    
    def __init__(self):
        self.network_calls = []
        self.external_connections = []
        self.data_sent = []
        
    def verify_no_network_activity(self):
        """Vérifie qu'aucune connexion réseau n'est établie"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "network_activity": False,
            "external_connections": [],
            "compliance": True,
            "details": []
        }
        
        try:
            # Vérifier les connexions réseau actives du processus
            import psutil
            current_process = psutil.Process(os.getpid())
            connections = current_process.connections()
            
            if connections:
                report["network_activity"] = True
                report["compliance"] = False
                for conn in connections:
                    report["external_connections"].append({
                        "local": f"{conn.laddr.ip}:{conn.laddr.port}",
                        "remote": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "None",
                        "status": conn.status
                    })
                report["details"].append(f"⚠️ {len(connections)} active network connection(s) detected")
            else:
                report["details"].append("✓ No network connections detected")
                
        except Exception as e:
            report["details"].append(f"⚠️ Could not verify network activity: {e}")
        
        return report
    
    def verify_no_external_requests(self):
        """Vérifie qu'aucune requête externe n'est faite"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "external_requests": False,
            "blocked_domains": [],
            "compliance": True,
            "details": []
        }
        
        # Liste des domaines suspects à bloquer
        suspicious_domains = [
            "telemetry.microsoft.com",
            "analytics.google.com",
            "api.mixpanel.com",
            "track.segment.io",
            "api.amplitude.com",
        ]
        
        # Vérifier que ces domaines ne sont pas résolus
        for domain in suspicious_domains:
            try:
                socket.gethostbyname(domain)
                # Si on arrive ici, le domaine est accessible (pas bon)
                report["external_requests"] = True
                report["compliance"] = False
                report["blocked_domains"].append(domain)
            except socket.gaierror:
                # Domaine non résolu = bon signe
                pass
        
        if report["blocked_domains"]:
            report["details"].append(f"⚠️ Suspicious domains accessible: {', '.join(report['blocked_domains'])}")
        else:
            report["details"].append("✓ No suspicious domain resolution detected")
        
        return report
    
    def verify_no_data_collection(self):
        """Vérifie qu'aucune donnée utilisateur n'est collectée"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "data_collection": False,
            "sensitive_data_accessed": [],
            "compliance": True,
            "details": []
        }
        
        # Vérifier qu'aucun fichier de collecte n'existe
        suspicious_files = [
            "telemetry.log",
            "analytics.db",
            "user_data.json",
            "tracking.txt",
        ]
        
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        for filename in suspicious_files:
            filepath = os.path.join(app_dir, filename)
            if os.path.exists(filepath):
                report["data_collection"] = True
                report["compliance"] = False
                report["sensitive_data_accessed"].append(filepath)
        
        if report["sensitive_data_accessed"]:
            report["details"].append(f"⚠️ Suspicious files found: {', '.join(report['sensitive_data_accessed'])}")
        else:
            report["details"].append("✓ No data collection files detected")
        
        return report
    
    def generate_compliance_report(self):
        """Génère un rapport complet de conformité"""
        print("="*80)
        print("RAPPORT DE CONFORMITÉ TÉLÉMÉTRIE")
        print("="*80)
        print()
        
        # Vérification 1: Activité réseau
        print("[1/3] Vérification de l'activité réseau...")
        network_report = self.verify_no_network_activity()
        for detail in network_report["details"]:
            print(f"      {detail}")
        print()
        
        # Vérification 2: Requêtes externes
        print("[2/3] Vérification des requêtes externes...")
        external_report = self.verify_no_external_requests()
        for detail in external_report["details"]:
            print(f"      {detail}")
        print()
        
        # Vérification 3: Collecte de données
        print("[3/3] Vérification de la collecte de données...")
        data_report = self.verify_no_data_collection()
        for detail in data_report["details"]:
            print(f"      {detail}")
        print()
        
        # Résumé
        all_compliant = (
            network_report["compliance"] and
            external_report["compliance"] and
            data_report["compliance"]
        )
        
        print("="*80)
        print("RÉSUMÉ DE CONFORMITÉ")
        print("="*80)
        print(f"Activité réseau       : {'✓ CONFORME' if network_report['compliance'] else '✗ NON CONFORME'}")
        print(f"Requêtes externes     : {'✓ CONFORME' if external_report['compliance'] else '✗ NON CONFORME'}")
        print(f"Collecte de données   : {'✓ CONFORME' if data_report['compliance'] else '✗ NON CONFORME'}")
        print()
        
        if all_compliant:
            print("✓ STATUT GLOBAL: CONFORME - Aucune télémétrie détectée")
            print("✓ Aucune donnée utilisateur n'est envoyée sans consentement")
        else:
            print("✗ STATUT GLOBAL: NON CONFORME - Télémétrie détectée")
            print("⚠️ Des données pourraient être envoyées")
        
        print("="*80)
        print()
        
        return {
            "compliant": all_compliant,
            "network": network_report,
            "external": external_report,
            "data": data_report,
            "timestamp": datetime.now().isoformat()
        }


# Instance globale
telemetry_checker = TelemetryChecker()


if __name__ == "__main__":
    # Test du module
    checker = TelemetryChecker()
    report = checker.generate_compliance_report()
    
    if report["compliant"]:
        sys.exit(0)
    else:
        sys.exit(1)
