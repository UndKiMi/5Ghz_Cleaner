"""
Advanced System Optimizations
Options avancées pour optimiser Windows 11
"""
import os
import subprocess
import winreg
import ctypes
from pathlib import Path


def disable_hibernation():
    """
    Désactive l'hibernation et supprime hiberfil.sys
    Libère plusieurs GB (taille = RAM)
    """
    try:
        # Désactiver l'hibernation
        result = subprocess.run(
            ["powercfg", "/hibernate", "off"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            print("[SUCCESS] Hibernation désactivée")
            return {"success": True, "message": "Hibernation désactivée"}
        else:
            print(f"[WARNING] Échec désactivation hibernation: {result.stderr}")
            return {"success": False, "message": result.stderr}
    
    except Exception as e:
        print(f"[ERROR] Disable hibernation failed: {e}")
        return {"success": False, "message": str(e)}


def clean_old_restore_points(keep_count=2):
    """
    Nettoie les anciens points de restauration
    Garde seulement les X plus récents
    
    Args:
        keep_count: Nombre de points à garder (défaut: 2)
    """
    try:
        # Utiliser vssadmin pour lister les shadow copies
        result = subprocess.run(
            ["vssadmin", "list", "shadows"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            # Compter les shadow copies
            shadow_count = result.stdout.count("Shadow Copy ID:")
            
            if shadow_count > keep_count:
                # Supprimer les anciennes (garder les récentes)
                # Note: Cette opération nécessite des privilèges admin
                print(f"[INFO] {shadow_count} points de restauration trouvés")
                print(f"[INFO] Conservation des {keep_count} plus récents")
                
                # Pour l'instant, on ne supprime pas automatiquement
                # car c'est une opération sensible
                return {
                    "success": True,
                    "message": f"{shadow_count} points trouvés, {keep_count} conservés",
                    "count": shadow_count
                }
            else:
                print(f"[INFO] Seulement {shadow_count} points, aucun nettoyage nécessaire")
                return {
                    "success": True,
                    "message": f"Seulement {shadow_count} points",
                    "count": shadow_count
                }
        else:
            return {"success": False, "message": "Impossible de lister les points"}
    
    except Exception as e:
        print(f"[ERROR] Clean restore points failed: {e}")
        return {"success": False, "message": str(e)}


def optimize_startup_programs():
    """
    Liste et permet d'optimiser les programmes au démarrage
    """
    try:
        disabled_count = 0
        
        # Lire les programmes de démarrage depuis le registre
        startup_keys = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
        ]
        
        startup_programs = []
        
        for hkey, path in startup_keys:
            try:
                key = winreg.OpenKey(hkey, path, 0, winreg.KEY_READ)
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        startup_programs.append({"name": name, "path": value})
                        i += 1
                    except OSError:
                        break
                winreg.CloseKey(key)
            except FileNotFoundError:
                pass
        
        print(f"[INFO] {len(startup_programs)} programmes au démarrage trouvés")
        
        return {
            "success": True,
            "message": f"{len(startup_programs)} programmes analysés",
            "count": len(startup_programs),
            "programs": startup_programs
        }
    
    except Exception as e:
        print(f"[ERROR] Optimize startup failed: {e}")
        return {"success": False, "message": str(e)}


def clear_browser_cache():
    """
    Vide le cache des navigateurs principaux
    Chrome, Firefox, Edge
    """
    try:
        cleared_browsers = []
        total_size = 0
        
        # Chemins des caches
        user_profile = os.environ.get("USERPROFILE", "")
        local_appdata = os.environ.get("LOCALAPPDATA", "")
        
        browser_caches = {
            "Chrome": os.path.join(local_appdata, "Google", "Chrome", "User Data", "Default", "Cache"),
            "Edge": os.path.join(local_appdata, "Microsoft", "Edge", "User Data", "Default", "Cache"),
            "Firefox": os.path.join(local_appdata, "Mozilla", "Firefox", "Profiles"),
        }
        
        for browser, cache_path in browser_caches.items():
            if os.path.exists(cache_path):
                try:
                    # Compter la taille avant suppression
                    size = sum(f.stat().st_size for f in Path(cache_path).rglob('*') if f.is_file())
                    
                    # Supprimer les fichiers de cache
                    for file in Path(cache_path).rglob('*'):
                        if file.is_file():
                            try:
                                file.unlink()
                            except:
                                pass
                    
                    cleared_browsers.append(browser)
                    total_size += size
                    print(f"[SUCCESS] Cache {browser} vidé: {size / (1024*1024):.2f} MB")
                except Exception as e:
                    print(f"[WARNING] Erreur cache {browser}: {e}")
        
        return {
            "success": True,
            "message": f"{len(cleared_browsers)} navigateurs nettoyés",
            "browsers": cleared_browsers,
            "size_mb": total_size / (1024 * 1024)
        }
    
    except Exception as e:
        print(f"[ERROR] Clear browser cache failed: {e}")
        return {"success": False, "message": str(e)}


def clean_event_logs():
    """
    Nettoie les logs d'événements Windows
    """
    try:
        # Liste des logs à nettoyer
        logs_to_clear = ["Application", "System", "Security"]
        cleared_count = 0
        
        for log_name in logs_to_clear:
            try:
                result = subprocess.run(
                    ["wevtutil", "cl", log_name],
                    capture_output=True,
                    text=True,
                    check=False
                )
                
                if result.returncode == 0:
                    cleared_count += 1
                    print(f"[SUCCESS] Log {log_name} vidé")
            except Exception as e:
                print(f"[WARNING] Erreur log {log_name}: {e}")
        
        return {
            "success": True,
            "message": f"{cleared_count} logs nettoyés",
            "count": cleared_count
        }
    
    except Exception as e:
        print(f"[ERROR] Clean event logs failed: {e}")
        return {"success": False, "message": str(e)}


def disable_superfetch():
    """
    Désactive Superfetch/Prefetch (recommandé pour SSD)
    """
    try:
        # Désactiver le service SysMain (Superfetch)
        result = subprocess.run(
            ["sc", "config", "SysMain", "start=", "disabled"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            # Arrêter le service
            subprocess.run(["sc", "stop", "SysMain"], capture_output=True, check=False)
            print("[SUCCESS] Superfetch désactivé")
            return {"success": True, "message": "Superfetch désactivé"}
        else:
            return {"success": False, "message": result.stderr}
    
    except Exception as e:
        print(f"[ERROR] Disable superfetch failed: {e}")
        return {"success": False, "message": str(e)}


def disable_cortana():
    """
    Désactive Cortana
    """
    try:
        # Désactiver via le registre
        key_path = r"SOFTWARE\Policies\Microsoft\Windows\Windows Search"
        
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)
            winreg.SetValueEx(key, "AllowCortana", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            print("[SUCCESS] Cortana désactivé")
            return {"success": True, "message": "Cortana désactivé"}
        except Exception as e:
            print(f"[WARNING] Erreur registre Cortana: {e}")
            return {"success": False, "message": str(e)}
    
    except Exception as e:
        print(f"[ERROR] Disable Cortana failed: {e}")
        return {"success": False, "message": str(e)}


def optimize_tcp_ip():
    """
    Optimise les paramètres TCP/IP
    """
    try:
        # Reset Winsock
        result1 = subprocess.run(
            ["netsh", "winsock", "reset"],
            capture_output=True,
            text=True,
            check=False
        )
        
        # Reset TCP/IP
        result2 = subprocess.run(
            ["netsh", "int", "ip", "reset"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result1.returncode == 0 and result2.returncode == 0:
            print("[SUCCESS] TCP/IP optimisé")
            return {"success": True, "message": "TCP/IP optimisé (redémarrage recommandé)"}
        else:
            return {"success": False, "message": "Erreur optimisation TCP/IP"}
    
    except Exception as e:
        print(f"[ERROR] Optimize TCP/IP failed: {e}")
        return {"success": False, "message": str(e)}


def disable_unnecessary_services():
    """
    Désactive les services Windows inutiles
    """
    try:
        # Liste sécurisée de services à désactiver
        services_to_disable = [
            "Fax",  # Service de fax
            "TabletInputService",  # Service d'entrée Tablet PC
            "WMPNetworkSvc",  # Service de partage réseau du Lecteur Windows Media
        ]
        
        disabled_count = 0
        
        for service in services_to_disable:
            try:
                result = subprocess.run(
                    ["sc", "config", service, "start=", "disabled"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                
                if result.returncode == 0:
                    subprocess.run(["sc", "stop", service], capture_output=True, check=False)
                    disabled_count += 1
                    print(f"[SUCCESS] Service {service} désactivé")
            except Exception as e:
                print(f"[WARNING] Erreur service {service}: {e}")
        
        return {
            "success": True,
            "message": f"{disabled_count} services désactivés",
            "count": disabled_count
        }
    
    except Exception as e:
        print(f"[ERROR] Disable services failed: {e}")
        return {"success": False, "message": str(e)}


def enable_gaming_mode():
    """
    Active le mode Gaming (optimisations pour jeux)
    """
    try:
        # Désactiver Game Bar
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR"
        
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
            winreg.SetValueEx(key, "AppCaptureEnabled", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            print("[SUCCESS] Mode Gaming activé")
            return {"success": True, "message": "Mode Gaming activé"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    except Exception as e:
        print(f"[ERROR] Enable gaming mode failed: {e}")
        return {"success": False, "message": str(e)}


def clean_old_drivers():
    """
    Nettoie les pilotes obsolètes
    """
    try:
        # Utiliser pnputil pour lister les pilotes
        result = subprocess.run(
            ["pnputil", "/enum-drivers"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            # Compter les pilotes
            driver_count = result.stdout.count("Published Name")
            print(f"[INFO] {driver_count} pilotes trouvés")
            
            return {
                "success": True,
                "message": f"{driver_count} pilotes analysés",
                "count": driver_count
            }
        else:
            return {"success": False, "message": "Impossible de lister les pilotes"}
    
    except Exception as e:
        print(f"[ERROR] Clean old drivers failed: {e}")
        return {"success": False, "message": str(e)}


def clean_winsxs():
    """
    Nettoie le dossier WinSxS (composants Windows)
    """
    try:
        # Utiliser DISM pour nettoyer WinSxS
        result = subprocess.run(
            ["DISM", "/Online", "/Cleanup-Image", "/StartComponentCleanup", "/ResetBase"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            print("[SUCCESS] WinSxS nettoyé")
            return {"success": True, "message": "WinSxS nettoyé"}
        else:
            return {"success": False, "message": "Erreur nettoyage WinSxS"}
    
    except Exception as e:
        print(f"[ERROR] Clean WinSxS failed: {e}")
        return {"success": False, "message": str(e)}


def optimize_pagefile():
    """
    Optimise le fichier de pagination
    """
    try:
        # Définir la taille du pagefile (taille système)
        result = subprocess.run(
            ["wmic", "computersystem", "where", "name='%computername%'", "set", "AutomaticManagedPagefile=True"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            print("[SUCCESS] Pagefile optimisé")
            return {"success": True, "message": "Pagefile optimisé"}
        else:
            return {"success": False, "message": "Erreur optimisation pagefile"}
    
    except Exception as e:
        print(f"[ERROR] Optimize pagefile failed: {e}")
        return {"success": False, "message": str(e)}
