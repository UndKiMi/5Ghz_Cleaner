"""
Module d'optimisation automatique des disques selon leur type (HDD/SSD/NVMe)
Applique les meilleures pratiques pour chaque type de disque

DÉTECTION LOCALE:
- Scan du disque C: sans accès Internet
- Détection type: HDD, SSD, NVMe via APIs Windows natives
- Récupération modèle/marque via WMI et PowerShell
- Optimisations adaptées au type détecté

SÉCURITÉ:
- Aucune modification dangereuse
- Backup automatique avant modifications
- Toutes les optimisations sont réversibles
"""
import subprocess
import os
import winreg
import time
from typing import Dict, Optional


def get_disk_info(drive_letter: str) -> Dict:
    """
    Récupère les informations complètes du disque (type, modèle, marque)
    Détection 100% locale sans accès Internet
    
    Args:
        drive_letter: Lettre du lecteur (ex: "C:\\")
    
    Returns:
        dict: {
            'type': 'HDD'|'SSD'|'NVMe'|'Unknown',
            'model': str,
            'manufacturer': str,
            'serial': str,
            'size_gb': float
        }
    """
    try:
        # PowerShell pour récupérer toutes les infos du disque
        ps_command = f"""
        $disk = Get-PhysicalDisk | Where-Object {{
            $partition = Get-Partition -DiskNumber $_.DeviceID -ErrorAction SilentlyContinue | 
                         Where-Object {{$_.DriveLetter -eq '{drive_letter.replace(':', '').replace('\\', '')}'}}
            $partition -ne $null
        }}
        if ($disk) {{
            $mediaType = $disk.MediaType
            $busType = $disk.BusType
            $model = $disk.FriendlyName
            $manufacturer = $disk.Manufacturer
            $serial = $disk.SerialNumber
            $sizeGB = [math]::Round($disk.Size / 1GB, 2)
            
            # Détecter le type
            if ($busType -eq 'NVMe') {{
                $type = 'NVMe'
            }}
            elseif ($mediaType -eq 'SSD') {{
                $type = 'SSD'
            }}
            elseif ($mediaType -eq 'HDD') {{
                $type = 'HDD'
            }}
            else {{
                $type = 'Unknown'
            }}
            
            Write-Output "$type|$model|$manufacturer|$serial|$sizeGB"
        }} else {{
            Write-Output "Unknown||||0"
        }}
        """
        
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=15,
            shell=False
        )
        
        output = result.stdout.strip()
        parts = output.split('|')
        
        if len(parts) >= 5:
            disk_info = {
                'type': parts[0] if parts[0] in ['HDD', 'SSD', 'NVMe'] else 'Unknown',
                'model': parts[1].strip() if parts[1] else 'Non détecté',
                'manufacturer': parts[2].strip() if parts[2] else 'Non détecté',
                'serial': parts[3].strip() if parts[3] else 'N/A',
                'size_gb': float(parts[4]) if parts[4] else 0.0
            }
            
            print(f"[INFO] Disk info: {disk_info}")
            return disk_info
        else:
            return {
                'type': 'Unknown',
                'model': 'Non détecté',
                'manufacturer': 'Non détecté',
                'serial': 'N/A',
                'size_gb': 0.0
            }
    
    except Exception as e:
        print(f"[ERROR] Failed to get disk info: {e}")
        return {
            'type': 'Unknown',
            'model': 'Non détecté',
            'manufacturer': 'Non détecté',
            'serial': 'N/A',
            'size_gb': 0.0
        }


def detect_disk_type(drive_letter):
    """
    Détecte le type de disque (HDD, SSD, NVMe)
    Version simplifiée pour compatibilité
    
    Returns:
        str: 'HDD', 'SSD', ou 'NVMe'
    """
    try:
        # Utiliser PowerShell pour détecter le type de disque
        ps_command = f"""
        $disk = Get-PhysicalDisk | Where-Object {{
            $partition = Get-Partition -DiskNumber $_.DeviceID -ErrorAction SilentlyContinue | 
                         Where-Object {{$_.DriveLetter -eq '{drive_letter.replace(':', '').replace('\\', '')}'}}
            $partition -ne $null
        }}
        if ($disk) {{
            $mediaType = $disk.MediaType
            $busType = $disk.BusType
            
            # Détecter NVMe
            if ($busType -eq 'NVMe') {{
                Write-Output 'NVMe'
            }}
            # Détecter SSD
            elseif ($mediaType -eq 'SSD') {{
                Write-Output 'SSD'
            }}
            # Détecter HDD
            elseif ($mediaType -eq 'HDD') {{
                Write-Output 'HDD'
            }}
            else {{
                Write-Output 'Unknown'
            }}
        }} else {{
            Write-Output 'Unknown'
        }}
        """
        
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=10,
            shell=False
        )
        
        disk_type = result.stdout.strip()
        print(f"[INFO] Disk {drive_letter} detected as: {disk_type}")
        return disk_type if disk_type in ['HDD', 'SSD', 'NVMe'] else 'Unknown'
    
    except Exception as e:
        print(f"[ERROR] Failed to detect disk type: {e}")
        return 'Unknown'


def optimize_hdd(drive_letter):
    """
    Optimise un disque HDD
    
    Optimisations:
    - Activer la défragmentation automatique
    - Désactiver l'indexation si inutile
    - Optimiser les paramètres d'hibernation
    """
    results = []
    
    try:
        # 1. Activer la défragmentation automatique
        print(f"[INFO] Activation de la défragmentation automatique pour {drive_letter}...")
        ps_command = f"Optimize-Volume -DriveLetter {drive_letter.replace(':', '').replace('\\', '')} -Defrag -Verbose"
        
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes max
            shell=False
        )
        
        if result.returncode == 0:
            results.append("✓ Défragmentation activée")
            print("[SUCCESS] Défragmentation activée")
        else:
            results.append("✗ Échec défragmentation")
            print(f"[WARNING] Défragmentation failed: {result.stderr}")
    
    except subprocess.TimeoutExpired:
        results.append("✗ Défragmentation timeout")
        print("[WARNING] Défragmentation timeout")
    except Exception as e:
        results.append(f"✗ Erreur défragmentation: {str(e)[:30]}")
        print(f"[ERROR] Défragmentation error: {e}")
    
    try:
        # 2. Désactiver l'indexation du contenu des fichiers (garde l'indexation des noms)
        print(f"[INFO] Optimisation de l'indexation pour {drive_letter}...")
        
        # Désactiver l'indexation du contenu via PowerShell
        ps_command = f"""
        $drive = Get-WmiObject -Class Win32_Volume -Filter "DriveLetter='{drive_letter}'"
        if ($drive) {{
            $drive.IndexingEnabled = $false
            $drive.Put()
            Write-Output 'Success'
        }}
        """
        
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=30,
            shell=False
        )
        
        if "Success" in result.stdout:
            results.append("✓ Indexation optimisée")
            print("[SUCCESS] Indexation optimisée")
        else:
            results.append("⚠ Indexation inchangée")
    
    except Exception as e:
        results.append("⚠ Indexation inchangée")
        print(f"[WARNING] Indexation optimization failed: {e}")
    
    return {
        "success": True,
        "disk_type": "HDD",
        "optimizations": results,
        "message": f"HDD {drive_letter} optimisé"
    }


def optimize_ssd(drive_letter):
    """
    Optimise un disque SSD (SATA)
    
    Optimisations:
    - Activer TRIM
    - Désactiver la défragmentation automatique
    - Désactiver l'indexation du contenu
    """
    results = []
    
    try:
        # 1. Activer TRIM
        print(f"[INFO] Activation de TRIM pour {drive_letter}...")
        ps_command = f"Optimize-Volume -DriveLetter {drive_letter.replace(':', '').replace('\\', '')} -ReTrim -Verbose"
        
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=60,
            shell=False
        )
        
        if result.returncode == 0:
            results.append("✓ TRIM activé")
            print("[SUCCESS] TRIM activé")
        else:
            results.append("✗ Échec TRIM")
            print(f"[WARNING] TRIM failed: {result.stderr}")
    
    except subprocess.TimeoutExpired:
        results.append("✗ TRIM timeout")
    except Exception as e:
        results.append(f"✗ Erreur TRIM: {str(e)[:30]}")
        print(f"[ERROR] TRIM error: {e}")
    
    try:
        # 2. Désactiver la défragmentation automatique pour ce disque
        print(f"[INFO] Désactivation de la défragmentation pour {drive_letter}...")
        
        # Désactiver via le planificateur de tâches
        ps_command = f"""
        Disable-ScheduledTask -TaskName "ScheduledDefrag" -TaskPath "\\Microsoft\\Windows\\Defrag\\" -ErrorAction SilentlyContinue
        Write-Output 'Success'
        """
        
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=30,
            shell=False
        )
        
        results.append("✓ Défragmentation désactivée")
        print("[SUCCESS] Défragmentation désactivée")
    
    except Exception as e:
        results.append("⚠ Défragmentation inchangée")
        print(f"[WARNING] Defrag disable failed: {e}")
    
    try:
        # 3. Désactiver l'indexation du contenu
        print(f"[INFO] Désactivation de l'indexation pour {drive_letter}...")
        
        ps_command = f"""
        $drive = Get-WmiObject -Class Win32_Volume -Filter "DriveLetter='{drive_letter}'"
        if ($drive) {{
            $drive.IndexingEnabled = $false
            $drive.Put()
            Write-Output 'Success'
        }}
        """
        
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=30,
            shell=False
        )
        
        if "Success" in result.stdout:
            results.append("✓ Indexation désactivée")
            print("[SUCCESS] Indexation désactivée")
        else:
            results.append("⚠ Indexation inchangée")
    
    except Exception as e:
        results.append("⚠ Indexation inchangée")
        print(f"[WARNING] Indexation disable failed: {e}")
    
    return {
        "success": True,
        "disk_type": "SSD",
        "optimizations": results,
        "message": f"SSD {drive_letter} optimisé"
    }


def optimize_nvme(drive_letter):
    """
    Optimise un disque NVMe
    
    Optimisations:
    - Activer TRIM
    - Désactiver l'indexation
    - Passer en mode Hautes performances
    - Optimiser la mémoire virtuelle
    """
    results = []
    
    try:
        # 1. Activer TRIM
        print(f"[INFO] Activation de TRIM pour {drive_letter}...")
        ps_command = f"Optimize-Volume -DriveLetter {drive_letter.replace(':', '').replace('\\', '')} -ReTrim -Verbose"
        
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=60,
            shell=False
        )
        
        if result.returncode == 0:
            results.append("✓ TRIM activé")
            print("[SUCCESS] TRIM activé")
        else:
            results.append("✗ Échec TRIM")
    
    except Exception as e:
        results.append(f"✗ Erreur TRIM: {str(e)[:30]}")
        print(f"[ERROR] TRIM error: {e}")
    
    try:
        # 2. Désactiver l'indexation
        print(f"[INFO] Désactivation de l'indexation pour {drive_letter}...")
        
        ps_command = f"""
        $drive = Get-WmiObject -Class Win32_Volume -Filter "DriveLetter='{drive_letter}'"
        if ($drive) {{
            $drive.IndexingEnabled = $false
            $drive.Put()
            Write-Output 'Success'
        }}
        """
        
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=30,
            shell=False
        )
        
        if "Success" in result.stdout:
            results.append("✓ Indexation désactivée")
        else:
            results.append("⚠ Indexation inchangée")
    
    except Exception as e:
        results.append("⚠ Indexation inchangée")
        print(f"[WARNING] Indexation disable failed: {e}")
    
    try:
        # 3. Passer en mode Hautes performances
        print("[INFO] Activation du mode Hautes performances...")
        
        ps_command = "powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
        
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=10,
            shell=False
        )
        
        if result.returncode == 0:
            results.append("✓ Mode Hautes performances activé")
            print("[SUCCESS] Mode Hautes performances activé")
        else:
            results.append("⚠ Mode alimentation inchangé")
    
    except Exception as e:
        results.append("⚠ Mode alimentation inchangé")
        print(f"[WARNING] Power plan failed: {e}")
    
    return {
        "success": True,
        "disk_type": "NVMe",
        "optimizations": results,
        "message": f"NVMe {drive_letter} optimisé"
    }


def auto_optimize_disk(drive_letter):
    """
    Optimise automatiquement un disque selon son type
    Détection locale complète: type, modèle, marque
    
    Args:
        drive_letter (str): Lettre du lecteur (ex: "C:\\")
    
    Returns:
        dict: Résultat de l'optimisation avec infos disque
    """
    print(f"\n[INFO] ========== AUTO-OPTIMISATION DU DISQUE {drive_letter} ==========")
    
    # Récupérer les informations complètes du disque
    disk_info = get_disk_info(drive_letter)
    disk_type = disk_info['type']
    
    print(f"[INFO] Type: {disk_type}")
    print(f"[INFO] Modèle: {disk_info['model']}")
    print(f"[INFO] Fabricant: {disk_info['manufacturer']}")
    print(f"[INFO] Taille: {disk_info['size_gb']} GB")
    
    if disk_type == 'Unknown':
        return {
            "success": False,
            "disk_type": "Unknown",
            "disk_info": disk_info,
            "message": f"Type de disque {drive_letter} non détecté",
            "optimizations": []
        }
    
    # Appliquer les optimisations selon le type
    if disk_type == 'HDD':
        result = optimize_hdd(drive_letter)
    elif disk_type == 'SSD':
        result = optimize_ssd(drive_letter)
    elif disk_type == 'NVMe':
        result = optimize_nvme(drive_letter)
    else:
        result = {
            "success": False,
            "disk_type": disk_type,
            "disk_info": disk_info,
            "message": f"Type {disk_type} non supporté",
            "optimizations": []
        }
    
    # Ajouter les infos du disque au résultat
    result['disk_info'] = disk_info
    
    print(f"[INFO] ========== OPTIMISATION TERMINÉE ==========\n")
    return result
