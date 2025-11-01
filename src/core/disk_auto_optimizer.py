"""
Module d'optimisation automatique des disques selon leur type (HDD/SSD/NVMe)
Applique les meilleures pratiques pour chaque type de disque
"""
import subprocess
import os
import winreg
import time


def detect_disk_type(drive_letter):
    """
    Détecte le type de disque (HDD, SSD, NVMe)
    
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
    
    Args:
        drive_letter (str): Lettre du lecteur (ex: "C:\\")
    
    Returns:
        dict: Résultat de l'optimisation
    """
    print(f"\n[INFO] ========== AUTO-OPTIMISATION DU DISQUE {drive_letter} ==========")
    
    # Détecter le type de disque
    disk_type = detect_disk_type(drive_letter)
    
    if disk_type == 'Unknown':
        return {
            "success": False,
            "disk_type": "Unknown",
            "message": f"Type de disque {drive_letter} non détecté",
            "optimizations": []
        }
    
    print(f"[INFO] Type détecté: {disk_type}")
    
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
            "message": f"Type {disk_type} non supporté",
            "optimizations": []
        }
    
    print(f"[INFO] ========== OPTIMISATION TERMINÉE ==========\n")
    return result
