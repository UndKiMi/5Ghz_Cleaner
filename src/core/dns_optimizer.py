"""
DNS Optimizer - Optimisation et nettoyage du cache DNS
Vide proprement le cache DNS Windows pour résoudre les problèmes de connexion
"""
import subprocess
from typing import Dict


class DNSOptimizer:
    """Optimiseur de cache DNS"""
    
    def flush_dns_cache(self) -> Dict:
        """
        Vide le cache DNS Windows
        
        Returns:
            Dict: Résultat de l'opération
        """
        try:
            print("[INFO] Vidage du cache DNS...")
            
            # Exécuter ipconfig /flushdns
            result = subprocess.run(
                ['ipconfig', '/flushdns'],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                timeout=5
            )
            
            if result.returncode == 0:
                print("[SUCCESS] Cache DNS vidé avec succès")
                return {
                    'success': True,
                    'message': 'Cache DNS vidé avec succès',
                    'output': result.stdout
                }
            else:
                print(f"[ERROR] Échec du vidage DNS: {result.stderr}")
                return {
                    'success': False,
                    'error': result.stderr
                }
                
        except subprocess.TimeoutExpired:
            print("[ERROR] Timeout lors du vidage DNS")
            return {
                'success': False,
                'error': 'Timeout'
            }
        except Exception as e:
            print(f"[ERROR] Erreur DNS: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_dns_cache_info(self) -> Dict:
        """
        Récupère les informations sur le cache DNS
        
        Returns:
            Dict: Informations sur le cache DNS
        """
        try:
            result = subprocess.run(
                ['ipconfig', '/displaydns'],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                timeout=5
            )
            
            if result.returncode == 0:
                # Compter le nombre d'entrées
                entries = result.stdout.count('Record Name')
                return {
                    'success': True,
                    'entries_count': entries,
                    'size_estimate_mb': entries * 0.001  # Estimation approximative
                }
            else:
                return {
                    'success': False,
                    'entries_count': 0
                }
                
        except Exception as e:
            print(f"[ERROR] Info DNS: {e}")
            return {
                'success': False,
                'entries_count': 0
            }


# Instance globale
dns_optimizer = DNSOptimizer()
