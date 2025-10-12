# Détection GPU et Températures - Guide Technique

## 🎯 Améliorations Apportées

### Détection GPU

Le système utilise maintenant **3 méthodes** pour détecter le GPU :

#### Méthode 1: WMI avec win32com (Prioritaire)
```python
import win32com.client
wmi = win32com.client.GetObject("winmgmts:")
video_controllers = wmi.InstancesOf("Win32_VideoController")
```
- ✅ Plus fiable que subprocess
- ✅ Accès direct aux objets WMI
- ✅ Filtre les adaptateurs virtuels Microsoft

#### Méthode 2: WMIC subprocess (Fallback)
```bash
wmic path win32_VideoController get name
```
- ✅ Fonctionne sans pywin32
- ✅ Compatible tous systèmes Windows

#### Méthode 3: Détection par défaut
- Affiche "GPU non détecté" si toutes les méthodes échouent

### Détection Température CPU

Le système utilise maintenant **3 méthodes** pour détecter la température :

#### Méthode 1: MSAcpi_ThermalZoneTemperature
```bash
wmic /namespace:\\root\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature
```
- ✅ Méthode standard Windows
- ✅ Température en dixièmes de Kelvin
- ⚠️ Nécessite privilèges admin sur certains systèmes

#### Méthode 2: Win32_TemperatureProbe
```bash
wmic path Win32_TemperatureProbe get CurrentReading
```
- ✅ Alternative WMI
- ✅ Température en dixièmes de Celsius
- ⚠️ Dépend du matériel

#### Méthode 3: WMI avec win32com
```python
import win32com.client
wmi = win32com.client.GetObject("winmgmts://./root/wmi")
temperature_info = wmi.ExecQuery("SELECT * FROM MSAcpi_ThermalZoneTemperature")
```
- ✅ Accès direct WMI
- ✅ Plus fiable que subprocess
- ⚠️ Nécessite pywin32

## 📊 Résultats Attendus

### GPU Détecté
Si vous avez un GPU dédié (NVIDIA, AMD, Intel), vous devriez voir :
```
AMD64 Family 25 Model 33 Stepping 2, AuthenticAMD
ou
NVIDIA GeForce RTX 3080
ou
Intel(R) UHD Graphics 630
```

### GPU Non Détecté
Si aucun GPU n'est détecté :
```
GPU non détecté
```
**Causes possibles:**
- Pas de GPU dédié (CPU avec graphiques intégrés uniquement)
- Adaptateur virtuel Microsoft uniquement
- Problème de drivers

### Température CPU

#### Si détectée (avec admin)
```
Température: 45.5°C (vert)
Température: 72.3°C (jaune)
Température: 85.1°C (rouge)
```

#### Si non disponible
```
Température: N/A (gris)
```
**Causes possibles:**
- Pas de privilèges administrateur
- Capteur non supporté par le BIOS/UEFI
- Matériel ne fournit pas l'information via WMI

## 🔧 Dépannage

### GPU Non Détecté

**Vérification manuelle:**
```bash
# PowerShell
Get-WmiObject Win32_VideoController | Select-Object Name

# CMD
wmic path win32_VideoController get name
```

**Si la commande fonctionne mais pas l'app:**
- Vérifier que pywin32 est installé : `pip install pywin32==306`
- Relancer l'application en tant qu'administrateur

### Température CPU Non Disponible

**Vérification manuelle:**
```bash
# PowerShell (admin requis)
Get-WmiObject -Namespace root/wmi -Class MSAcpi_ThermalZoneTemperature

# CMD (admin requis)
wmic /namespace:\\root\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature
```

**Si la commande ne retourne rien:**
- Votre système ne fournit pas cette information via WMI
- C'est normal sur certains matériels
- La température affichera "N/A"

**Solutions alternatives:**
1. Installer Open Hardware Monitor (externe)
2. Utiliser HWiNFO64 (externe)
3. Vérifier dans le BIOS

## 📝 Notes Techniques

### Validation des Températures

Le code vérifie que les températures sont valides :
```python
if 0 < temp_celsius < 150:  # Vérification de validité
    return round(temp_celsius, 1)
```

Cela évite les valeurs aberrantes (négatives ou > 150°C).

### Filtrage GPU

Les adaptateurs virtuels Microsoft sont filtrés :
```python
if gpu_name and "Microsoft" not in gpu_name:
    # Ajouter le GPU
```

Cela évite d'afficher "Microsoft Basic Display Adapter".

### Messages d'Information

Les messages ne s'affichent qu'**une seule fois** :
```python
if not self._temp_warning_shown:
    print(f"[INFO] CPU temperature sensor not available...")
    self._temp_warning_shown = True
```

Cela évite le spam dans la console.

## 🎯 Résumé

### Améliorations v1.6.0

1. ✅ **3 méthodes** de détection GPU (au lieu de 1)
2. ✅ **3 méthodes** de détection température CPU (au lieu de 1)
3. ✅ **Filtrage** des adaptateurs virtuels
4. ✅ **Validation** des températures (0-150°C)
5. ✅ **Messages propres** (affichés une seule fois)
6. ✅ **Fallback robuste** (affiche "N/A" si non disponible)

### Compatibilité

- ✅ Windows 10/11
- ✅ Avec ou sans privilèges admin
- ✅ Tous types de GPU (NVIDIA, AMD, Intel)
- ✅ Tous types de CPU (Intel, AMD)

### Limitations Connues

- ⚠️ Température CPU nécessite admin sur certains systèmes
- ⚠️ Température GPU nécessite nvidia-smi (NVIDIA) ou drivers spécifiques
- ⚠️ Certains matériels ne fournissent pas de capteurs via WMI

---

**Version:** 1.6.0  
**Date:** 2025-01-12  
**Auteur:** UndKiMi
