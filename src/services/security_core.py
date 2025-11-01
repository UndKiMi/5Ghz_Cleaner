"""
Module de Sécurité Principal - 5GHz Cleaner
Basé sur les recommandations officielles Microsoft
AUCUNE MODIFICATION UTILISATEUR AUTORISÉE
"""
import os
import re
from pathlib import Path

# ============================================================================
# BLOCKLIST SYSTÈME WINDOWS - PROTECTION MAXIMALE
# Basé sur: https://docs.microsoft.com/en-us/windows/win32/fileio/file-system-functionality-comparison
# ============================================================================

class WindowsSecurityCore:
    """Classe de sécurité immuable pour la protection du système Windows"""
    
    # Chemins système ABSOLUMENT INTERDITS (200+ chemins protégés)
    CRITICAL_SYSTEM_PATHS = frozenset({
        # ========== NOYAU WINDOWS (CRITIQUE) ==========
        r'C:\Windows\System32',
        r'C:\Windows\SysWOW64',
        r'C:\Windows\WinSxS',
        r'C:\Windows\servicing',
        r'C:\Windows\System',
        
        # ========== BOOT ET DÉMARRAGE (CRITIQUE) ==========
        r'C:\Windows\Boot',
        r'C:\Boot',
        r'C:\EFI',
        r'C:\Recovery',
        r'C:\Windows\ELAMBKUP',
        r'C:\System Volume Information',
        r'C:\$Recycle.Bin',
        
        # ========== PILOTES ET MATÉRIEL (CRITIQUE) ==========
        r'C:\Windows\System32\drivers',
        r'C:\Windows\System32\DriverStore',
        r'C:\Windows\inf',
        r'C:\Windows\System32\DRVSTORE',
        r'C:\Windows\System32\DriverState',
        
        # ========== POLICES ET RESSOURCES ==========
        r'C:\Windows\Fonts',
        r'C:\Windows\Resources',
        r'C:\Windows\Cursors',
        r'C:\Windows\Media',
        r'C:\Windows\Globalization',
        r'C:\Windows\IME',
        r'C:\Windows\InputMethod',
        
        # ========== ASSEMBLIES ET COMPOSANTS .NET ==========
        r'C:\Windows\assembly',
        r'C:\Windows\Microsoft.NET',
        r'C:\Program Files\dotnet',
        r'C:\Program Files (x86)\dotnet',
        r'C:\Program Files\Reference Assemblies',
        r'C:\Program Files (x86)\Reference Assemblies',
        
        # ========== CONFIGURATION ET REGISTRE (CRITIQUE) ==========
        r'C:\Windows\Registration',
        r'C:\Windows\PolicyDefinitions',
        r'C:\Windows\System32\config',
        r'C:\Windows\System32\GroupPolicy',
        r'C:\Windows\System32\GroupPolicyUsers',
        r'C:\ProgramData\Microsoft\Group Policy',
        
        # ========== APPLICATIONS SYSTÈME WINDOWS ==========
        r'C:\Windows\SystemApps',
        r'C:\Windows\ImmersiveControlPanel',
        r'C:\Windows\ShellExperiences',
        r'C:\Windows\ShellComponents',
        r'C:\Windows\Containers',
        r'C:\Windows\SystemResources',
        r'C:\Windows\FileManager',
        r'C:\Windows\PrintDialog',
        r'C:\Windows\Vss',
        
        # ========== PROGRAMMES (PROTECTION LARGE) ==========
        r'C:\Program Files',
        r'C:\Program Files (x86)',
        r'C:\ProgramData\Microsoft\Windows',
        r'C:\Windows\System32\WindowsPowerShell',
        r'C:\Windows\SysWOW64\WindowsPowerShell',
        
        # ========== UTILISATEURS SYSTÈME ==========
        r'C:\Users\Default',
        r'C:\Users\Public',
        r'C:\Users\All Users',
        r'C:\ProgramData\Default',
        
        # ========== LOGS SYSTÈME CRITIQUES ==========
        r'C:\Windows\Logs\CBS',
        r'C:\Windows\Logs\DISM',
        r'C:\Windows\Logs\DPX',
        r'C:\Windows\Logs\MoSetup',
        r'C:\Windows\Logs\WindowsUpdate',
        r'C:\Windows\Panther',
        r'C:\Windows\System32\LogFiles',
        r'C:\Windows\System32\winevt',
        
        # ========== WINDOWS UPDATE (CRITIQUE) ==========
        r'C:\Windows\SoftwareDistribution\DataStore',
        r'C:\Windows\SoftwareDistribution\SelfUpdate',
        r'C:\Windows\SoftwareDistribution\Download',
        r'C:\Windows\WinSxS\Backup',
        r'C:\Windows\WinSxS\ManifestCache',
        
        # ========== SÉCURITÉ WINDOWS DEFENDER ==========
        r'C:\ProgramData\Microsoft\Windows Defender',
        r'C:\Program Files\Windows Defender',
        r'C:\Program Files\Windows Defender Advanced Threat Protection',
        r'C:\ProgramData\Microsoft\Windows Defender Advanced Threat Protection',
        r'C:\Windows\System32\SecurityHealth',
        
        # ========== ACTIVATION ET LICENCE (CRITIQUE) ==========
        r'C:\Windows\System32\spp',
        r'C:\Windows\ServiceProfiles',
        r'C:\Windows\System32\slmgr',
        r'C:\ProgramData\Microsoft\Windows\ClipSVC',
        
        # ========== MICROSOFT OFFICE (SI INSTALLÉ) ==========
        r'C:\Program Files\Microsoft Office',
        r'C:\Program Files (x86)\Microsoft Office',
        r'C:\ProgramData\Microsoft\Office',
        r'C:\Program Files\Common Files\Microsoft Shared',
        r'C:\Program Files (x86)\Common Files\Microsoft Shared',
        
        # ========== MICROSOFT EDGE ==========
        r'C:\Program Files (x86)\Microsoft\Edge',
        r'C:\Program Files (x86)\Microsoft\EdgeCore',
        r'C:\Program Files (x86)\Microsoft\EdgeUpdate',
        r'C:\Program Files (x86)\Microsoft\EdgeWebView',
        
        # ========== MICROSOFT ONEDRIVE ==========
        r'C:\Program Files\Microsoft OneDrive',
        r'C:\Program Files (x86)\Microsoft OneDrive',
        r'C:\ProgramData\Microsoft OneDrive',
        
        # ========== MICROSOFT TEAMS ==========
        r'C:\Program Files\Microsoft\Teams',
        r'C:\Program Files (x86)\Microsoft\Teams',
        r'C:\ProgramData\Microsoft\Teams',
        
        # ========== WINDOWS STORE ET APPS ==========
        r'C:\Program Files\WindowsApps',
        r'C:\ProgramData\Microsoft\Windows\AppRepository',
        r'C:\Windows\System32\AppLocker',
        
        # ========== HYPER-V ET VIRTUALISATION ==========
        r'C:\ProgramData\Microsoft\Windows\Hyper-V',
        r'C:\Program Files\Hyper-V',
        r'C:\Windows\System32\vmms',
        
        # ========== WSL (WINDOWS SUBSYSTEM FOR LINUX) ==========
        r'C:\Program Files\WSL',
        r'C:\Windows\System32\lxss',
        
        # ========== BITLOCKER (CHIFFREMENT) ==========
        r'C:\Windows\System32\BitLocker',
        r'C:\ProgramData\Microsoft\Crypto',
        
        # ========== CERTIFICATS ET CRYPTOGRAPHIE (CRITIQUE) ==========
        r'C:\Windows\System32\CatRoot',
        r'C:\Windows\System32\CatRoot2',
        r'C:\ProgramData\Microsoft\Crypto\RSA',
        r'C:\ProgramData\Microsoft\Crypto\Keys',
        
        # ========== WINDOWS HELLO ET BIOMÉTRIE ==========
        r'C:\Windows\System32\WinBioDatabase',
        r'C:\Windows\System32\WinBioPlugIns',
        
        # ========== PARE-FEU WINDOWS ==========
        r'C:\Windows\System32\LogFiles\Firewall',
        r'C:\Windows\System32\wfp',
        
        # ========== RÉSEAU ET CONNECTIVITÉ ==========
        r'C:\Windows\System32\NetworkList',
        r'C:\Windows\System32\sru',
        r'C:\ProgramData\Microsoft\Network',
        
        # ========== TÂCHES PLANIFIÉES ==========
        r'C:\Windows\System32\Tasks',
        r'C:\Windows\Tasks',
        
        # ========== APPLICATIONS MICROSOFT COURANTES ==========
        # Visual Studio Code
        r'C:\Program Files\Microsoft VS Code',
        r'C:\Program Files (x86)\Microsoft VS Code',
        
        # Visual Studio
        r'C:\Program Files\Microsoft Visual Studio',
        r'C:\Program Files (x86)\Microsoft Visual Studio',
        r'C:\ProgramData\Microsoft\VisualStudio',
        
        # SQL Server
        r'C:\Program Files\Microsoft SQL Server',
        r'C:\Program Files (x86)\Microsoft SQL Server',
        
        # .NET SDK
        r'C:\Program Files\dotnet\sdk',
        r'C:\Program Files (x86)\dotnet\sdk',
        
        # ========== APPLICATIONS TIERCES CRITIQUES ==========
        # Navigateurs (données utilisateur protégées)
        r'C:\Program Files\Google\Chrome',
        r'C:\Program Files (x86)\Google\Chrome',
        r'C:\Program Files\Mozilla Firefox',
        r'C:\Program Files (x86)\Mozilla Firefox',
        r'C:\Program Files\BraveSoftware',
        
        # Antivirus tiers
        r'C:\Program Files\Avast Software',
        r'C:\Program Files\AVG',
        r'C:\Program Files\Kaspersky Lab',
        r'C:\Program Files\Norton',
        r'C:\Program Files\Bitdefender',
        r'C:\Program Files\ESET',
        r'C:\Program Files\Malwarebytes',
        
        # Suites bureautiques
        r'C:\Program Files\LibreOffice',
        r'C:\Program Files (x86)\LibreOffice',
        
        # Outils système critiques
        r'C:\Program Files\7-Zip',
        r'C:\Program Files\WinRAR',
        r'C:\Program Files\Adobe',
        r'C:\Program Files (x86)\Adobe',
        
        # Drivers GPU
        r'C:\Program Files\NVIDIA Corporation',
        r'C:\Program Files (x86)\NVIDIA Corporation',
        r'C:\Program Files\AMD',
        r'C:\Program Files\Intel',
        
        # ========== PROTECTION SUPPLÉMENTAIRE ==========
        r'C:\Windows\Installer',
        r'C:\Windows\Downloaded Program Files',
        r'C:\Windows\System32\Com',
        r'C:\Windows\System32\Dism',
        r'C:\Windows\System32\Sysprep',
        r'C:\Windows\System32\oobe',
        r'C:\Windows\System32\Recovery',
        r'C:\Windows\System32\restore',
        r'C:\Windows\System32\Speech',
        r'C:\Windows\System32\wbem',
        r'C:\Windows\System32\WindowsInternal.Inbox.Shared',
        r'C:\Windows\System32\WindowsInternal.Inbox.Media.Shared',
        
        # ========== COMPOSANTS WINDOWS ADDITIONNELS ==========
        r'C:\Windows\System32\spool',
        r'C:\Windows\System32\FxsTmp',
        r'C:\Windows\System32\migwiz',
        r'C:\Windows\System32\NDF',
        r'C:\Windows\System32\Printing_Admin_Scripts',
        r'C:\Windows\System32\ras',
        r'C:\Windows\System32\Setup',
        r'C:\Windows\System32\SMI',
        r'C:\Windows\System32\sru',
        r'C:\Windows\System32\Tasks_Migrated',
        r'C:\Windows\System32\TPM',
        r'C:\Windows\System32\Vault',
        r'C:\Windows\System32\WCN',
        r'C:\Windows\System32\WindowsPowerShell\v1.0',
        r'C:\Windows\System32\Winevt\Logs',
        r'C:\Windows\System32\WinMetadata',
        
        # ========== WINDOWS DEFENDER ADDITIONNEL ==========
        r'C:\Windows\System32\WindowsPowerShell\v1.0\Modules\Defender',
        r'C:\Windows\System32\WindowsPowerShell\v1.0\Modules\ConfigDefender',
        
        # ========== MICROSOFT APPLICATIONS ADDITIONNELLES ==========
        # PowerToys
        r'C:\Program Files\PowerToys',
        
        # Windows Terminal
        r'C:\Program Files\WindowsApps\Microsoft.WindowsTerminal',
        
        # Microsoft 365
        r'C:\Program Files\Microsoft 365',
        r'C:\Program Files (x86)\Microsoft 365',
        
        # Outlook
        r'C:\Program Files\Microsoft Office\root\Office16',
        r'C:\Program Files (x86)\Microsoft Office\root\Office16',
        
        # SharePoint
        r'C:\Program Files\Microsoft Office\root\Office16\GROOVE',
        
        # ========== APPLICATIONS TIERCES ADDITIONNELLES ==========
        # Zoom
        r'C:\Program Files\Zoom',
        r'C:\Program Files (x86)\Zoom',
        
        # Slack
        r'C:\Program Files\Slack',
        
        # Discord
        r'C:\Program Files\Discord',
        
        # Skype
        r'C:\Program Files\Microsoft\Skype for Desktop',
        r'C:\Program Files (x86)\Microsoft\Skype for Desktop',
        
        # VLC
        r'C:\Program Files\VideoLAN\VLC',
        r'C:\Program Files (x86)\VideoLAN\VLC',
        
        # OBS Studio
        r'C:\Program Files\obs-studio',
        r'C:\Program Files (x86)\obs-studio',
        
        # Steam
        r'C:\Program Files\Steam',
        r'C:\Program Files (x86)\Steam',
        
        # Epic Games
        r'C:\Program Files\Epic Games',
        r'C:\Program Files (x86)\Epic Games',
        
        # Battle.net
        r'C:\Program Files\Battle.net',
        r'C:\Program Files (x86)\Battle.net',
        
        # ========== OUTILS DÉVELOPPEMENT ==========
        # Git
        r'C:\Program Files\Git',
        r'C:\Program Files (x86)\Git',
        
        # Node.js
        r'C:\Program Files\nodejs',
        r'C:\Program Files (x86)\nodejs',
        
        # Python
        r'C:\Program Files\Python',
        r'C:\Program Files (x86)\Python',
        
        # JetBrains
        r'C:\Program Files\JetBrains',
        r'C:\Program Files (x86)\JetBrains',
        
        # Docker
        r'C:\Program Files\Docker',
        
        # ========== SÉCURITÉ ADDITIONNELLE ==========
        # Windows Security
        r'C:\Windows\System32\smartscreen.exe',
        r'C:\Windows\System32\SecurityHealthSystray.exe',
        
        # Certificats
        r'C:\Windows\System32\CertEnroll',
        r'C:\Windows\System32\certenroll',
        
        # ========== VIRTUALISATION ADDITIONNELLE ==========
        # VirtualBox
        r'C:\Program Files\Oracle\VirtualBox',
        r'C:\Program Files (x86)\Oracle\VirtualBox',
        
        # VMware
        r'C:\Program Files\VMware',
        r'C:\Program Files (x86)\VMware',
        
        # ========== BASES DE DONNÉES ==========
        # MySQL
        r'C:\Program Files\MySQL',
        r'C:\Program Files (x86)\MySQL',
        
        # PostgreSQL
        r'C:\Program Files\PostgreSQL',
        r'C:\Program Files (x86)\PostgreSQL',
        
        # MongoDB
        r'C:\Program Files\MongoDB',
        
        # ========== SERVEURS WEB ==========
        # Apache
        r'C:\Program Files\Apache Software Foundation',
        r'C:\Program Files (x86)\Apache Software Foundation',
        
        # XAMPP
        r'C:\xampp',
        
        # ========== PROTECTION DONNÉES UTILISATEUR ==========
        # Documents par défaut
        r'C:\Users\Public\Documents',
        r'C:\Users\Public\Pictures',
        r'C:\Users\Public\Music',
        r'C:\Users\Public\Videos',
        
        # ========== ADOBE CREATIVE CLOUD (AJOUTÉ) ==========
        r'C:\Program Files\Adobe\Adobe Photoshop',
        r'C:\Program Files\Adobe\Adobe Illustrator',
        r'C:\Program Files\Adobe\Adobe Premiere Pro',
        r'C:\Program Files\Adobe\Adobe After Effects',
        r'C:\Program Files\Adobe\Adobe InDesign',
        r'C:\Program Files\Adobe\Adobe Lightroom',
        r'C:\Program Files\Adobe\Adobe XD',
        r'C:\Program Files\Adobe\Adobe Acrobat',
        r'C:\Program Files\Adobe\Adobe Creative Cloud',
        r'C:\Program Files\Common Files\Adobe',
        r'C:\ProgramData\Adobe',
        
        # ========== AUTODESK (AJOUTÉ) ==========
        r'C:\Program Files\Autodesk',
        r'C:\Program Files (x86)\Autodesk',
        r'C:\ProgramData\Autodesk',
        r'C:\Program Files\Common Files\Autodesk Shared',
        r'C:\Program Files\Autodesk\AutoCAD',
        r'C:\Program Files\Autodesk\Maya',
        r'C:\Program Files\Autodesk\3ds Max',
        r'C:\Program Files\Autodesk\Revit',
        
        # ========== CLOUD STORAGE (AJOUTÉ - CRITIQUE) ==========
        # Dropbox
        r'C:\Program Files\Dropbox',
        r'C:\Program Files (x86)\Dropbox',
        
        # Google Drive
        r'C:\Program Files\Google\Drive File Stream',
        r'C:\Program Files (x86)\Google\Drive File Stream',
        
        # iCloud
        r'C:\Program Files\Common Files\Apple\Internet Services',
        r'C:\Program Files (x86)\Common Files\Apple\Internet Services',
        
        # Box
        r'C:\Program Files\Box\Box',
        
        # Nextcloud
        r'C:\Program Files\Nextcloud',
        
        # ========== IDEs ET OUTILS DÉVELOPPEMENT (AJOUTÉ) ==========
        # Android Studio
        r'C:\Program Files\Android\Android Studio',
        r'C:\Program Files (x86)\Android\Android Studio',
        
        # Eclipse
        r'C:\Program Files\Eclipse',
        r'C:\Program Files (x86)\Eclipse',
        
        # IntelliJ IDEA
        r'C:\Program Files\JetBrains\IntelliJ IDEA',
        
        # PyCharm
        r'C:\Program Files\JetBrains\PyCharm',
        
        # WebStorm
        r'C:\Program Files\JetBrains\WebStorm',
        
        # Rider
        r'C:\Program Files\JetBrains\Rider',
        
        # ========== BASES DE DONNÉES ADDITIONNELLES (AJOUTÉ) ==========
        # Redis
        r'C:\Program Files\Redis',
        
        # Elasticsearch
        r'C:\Program Files\Elastic\Elasticsearch',
        
        # Oracle
        r'C:\Program Files\Oracle',
        r'C:\Program Files (x86)\Oracle',
        
        # ========== MACHINES VIRTUELLES ET CONTENEURS (AJOUTÉ) ==========
        # Docker Desktop
        r'C:\Program Files\Docker\Docker',
        r'C:\ProgramData\Docker',
        r'C:\ProgramData\DockerDesktop',
        
        # Kubernetes
        r'C:\Program Files\Kubernetes',
        
        # Minikube
        r'C:\Program Files\Minikube',
        
        # ========== OUTILS GRAPHIQUES ET 3D (AJOUTÉ) ==========
        # Blender
        r'C:\Program Files\Blender Foundation\Blender',
        
        # GIMP
        r'C:\Program Files\GIMP',
        
        # Inkscape
        r'C:\Program Files\Inkscape',
        
        # Unity
        r'C:\Program Files\Unity',
        r'C:\Program Files\Unity Hub',
        
        # Unreal Engine
        r'C:\Program Files\Epic Games\UE_',
        
        # ========== OUTILS AUDIO/VIDEO PRO (AJOUTÉ) ==========
        # Audacity
        r'C:\Program Files\Audacity',
        
        # FL Studio
        r'C:\Program Files\Image-Line\FL Studio',
        
        # Ableton Live
        r'C:\ProgramData\Ableton',
        
        # DaVinci Resolve
        r'C:\Program Files\Blackmagic Design\DaVinci Resolve',
        
        # ========== OUTILS RÉSEAU ET SÉCURITÉ (AJOUTÉ) ==========
        # Wireshark
        r'C:\Program Files\Wireshark',
        
        # PuTTY
        r'C:\Program Files\PuTTY',
        
        # WinSCP
        r'C:\Program Files\WinSCP',
        
        # FileZilla
        r'C:\Program Files\FileZilla FTP Client',
        
        # ========== COMPILATEURS ET RUNTIMES (AJOUTÉ) ==========
        # Java JDK
        r'C:\Program Files\Java',
        r'C:\Program Files (x86)\Java',
        
        # Ruby
        r'C:\Program Files\Ruby',
        
        # Go
        r'C:\Program Files\Go',
        
        # Rust
        r'C:\Program Files\Rust',
        
        # ========== GESTIONNAIRES DE PAQUETS (AJOUTÉ) ==========
        # Chocolatey
        r'C:\ProgramData\chocolatey',
        
        # Scoop
        r'C:\ProgramData\scoop',
        
        # ========== PROTECTION SUPPLÉMENTAIRE CRITIQUE ==========
        # Certificats SSL/TLS
        r'C:\ProgramData\Microsoft\Crypto\RSA\MachineKeys',
        r'C:\ProgramData\Microsoft\Crypto\DSS\MachineKeys',
        
        # Windows Sandbox
        r'C:\ProgramData\Microsoft\Windows\Containers',
        
        # Windows Subsystem for Android
        r'C:\Program Files\Windows Subsystem for Android',
    })
    
    # Dossiers protégés (noms uniquement)
    PROTECTED_FOLDER_NAMES = frozenset({
        'System32', 'SysWOW64', 'WinSxS', 'Boot', 'System', 'inf',
        'Fonts', 'assembly', 'Registration', 'servicing', 'PolicyDefinitions',
        'DriverStore', 'drivers', 'Microsoft.NET', 'SystemApps',
        'ImmersiveControlPanel', 'ShellExperiences', 'ShellComponents',
        'WindowsApps', 'Packages', 'AppReadiness', 'CSC', 'Installer',
        'rescache', 'Resources', 'Cursors', 'config', 'spp',
        'ServiceProfiles', 'NetworkService', 'LocalService',
    })
    
    # Fichiers système CRITIQUES - Ne JAMAIS supprimer
    CRITICAL_SYSTEM_FILES = frozenset({
        # Noyau Windows
        'ntoskrnl.exe', 'hal.dll', 'ntdll.dll', 'kernel32.dll',
        'kernelbase.dll', 'user32.dll', 'gdi32.dll', 'advapi32.dll',
        'shell32.dll', 'ole32.dll', 'oleaut32.dll', 'msvcrt.dll',
        
        # Processus système essentiels
        'explorer.exe', 'csrss.exe', 'services.exe', 'lsass.exe',
        'winlogon.exe', 'svchost.exe', 'dwm.exe', 'taskhost.exe',
        'taskhostw.exe', 'smss.exe', 'wininit.exe', 'fontdrvhost.exe',
        
        # Gestionnaire de session
        'conhost.exe', 'dllhost.exe', 'runtimebroker.exe',
        'sihost.exe', 'ctfmon.exe', 'searchindexer.exe',
        
        # Fichiers de boot
        'bootmgr', 'bootmgfw.efi', 'winload.exe', 'winload.efi',
        'winresume.exe', 'winresume.efi', 'memtest.exe',
        
        # Fichiers de configuration système
        'boot.ini', 'bootstat.dat', 'hiberfil.sys', 'pagefile.sys',
        'swapfile.sys', 'ntuser.dat', 'system.dat', 'usrclass.dat',
        
        # Registre Windows
        'sam', 'security', 'software', 'system', 'default',
        'ntuser.ini', 'ntuser.pol', 'system.ini', 'win.ini',
        
        # Windows Update
        'wuaueng.dll', 'wuapi.dll', 'wuauserv', 'wudriver.dll',
        'wups.dll', 'wups2.dll', 'wuwebv.dll', 'wucltux.dll',
        
        # Windows Defender
        'msmpeng.exe', 'msseces.exe', 'mpcmdrun.exe', 'mpsigstub.exe',
        'mpengine.dll', 'mpasbase.vdm', 'mpavbase.vdm',
        
        # Pilotes critiques
        'ntfs.sys', 'disk.sys', 'classpnp.sys', 'partmgr.sys',
        'volmgr.sys', 'volsnap.sys', 'mountmgr.sys', 'fltmgr.sys',
        
        # Logs système importants
        'setupapi.dev.log', 'setupapi.app.log', 'windowsupdate.log',
        'cbs.log', 'dism.log', 'panther.log',
        
        # DLLs système additionnelles
        'comctl32.dll', 'comdlg32.dll', 'ws2_32.dll', 'wsock32.dll',
        'netapi32.dll', 'wininet.dll', 'urlmon.dll', 'shlwapi.dll',
        'version.dll', 'psapi.dll', 'imagehlp.dll', 'dbghelp.dll',
        'setupapi.dll', 'cfgmgr32.dll', 'devobj.dll', 'umpnpmgr.dll',
        'rpcrt4.dll', 'secur32.dll', 'crypt32.dll', 'wintrust.dll',
        'bcrypt.dll', 'ncrypt.dll', 'cryptsp.dll', 'rsaenh.dll',
        
        # Processus système additionnels
        'winlogon.exe', 'userinit.exe', 'logonui.exe', 'wininit.exe',
        'spoolsv.exe', 'lsm.exe', 'audiodg.exe', 'wuauclt.exe',
        'taskmgr.exe', 'regedit.exe', 'cmd.exe', 'powershell.exe',
        'mmc.exe', 'control.exe', 'rundll32.exe', 'regsvr32.exe',
        
        # Fichiers réseau
        'tcpip.sys', 'afd.sys', 'netbt.sys', 'tdx.sys',
        'wfplwfs.sys', 'ndis.sys', 'pacer.sys', 'netio.sys',
        
        # Fichiers audio/vidéo système
        'ksecdd.sys', 'ksecpkg.sys', 'ksuser.dll', 'avrt.dll',
        'audioses.dll', 'audioendpointbuilder.dll', 'audiosrv.dll',
        
        # Fichiers graphiques
        'dxgi.dll', 'd3d11.dll', 'd3d12.dll', 'd3d9.dll',
        'dxva2.dll', 'dwmapi.dll', 'dwmcore.dll', 'uxtheme.dll',
        
        # Fichiers de sécurité
        'lsasrv.dll', 'samsrv.dll', 'msv1_0.dll', 'kerberos.dll',
        'schannel.dll', 'credssp.dll', 'wdigest.dll', 'tspkg.dll',
        
        # Fichiers BitLocker
        'fveapi.dll', 'fvecpl.dll', 'fvewiz.dll', 'bdesvc.dll',
        'fvevol.sys', 'fveapibase.dll',
        
        # Fichiers Windows Update additionnels
        'wuaueng.dll', 'wuauclt.exe', 'wuapp.exe', 'wusa.exe',
        'trustedinstaller.exe', 'tiworker.exe', 'dismhost.exe',
        
        # Fichiers PowerShell
        'powershell.exe', 'pwsh.exe', 'powershell_ise.exe',
        'system.management.automation.dll',
        
        # Fichiers .NET
        'mscorlib.dll', 'clr.dll', 'clrjit.dll', 'mscoree.dll',
        'mscoreei.dll', 'fusion.dll', 'clrcompression.dll',
        
        # Fichiers COM/DCOM
        'ole32.dll', 'oleaut32.dll', 'combase.dll', 'rpcss.dll',
        'dcomlaunch', 'comsvcs.dll', 'clbcatq.dll',
        
        # Fichiers impression
        'spoolss.dll', 'localspl.dll', 'win32spl.dll', 'printui.dll',
        'winspool.drv', 'compstui.dll',
    })
    
    # Extensions ABSOLUMENT PROTÉGÉES
    PROTECTED_EXTENSIONS = frozenset({
        # Exécutables et bibliothèques
        '.exe', '.dll', '.sys', '.drv', '.ocx', '.cpl', '.scr',
        
        # Pilotes et installation
        '.inf', '.cat', '.pnf', '.msi', '.msu', '.cab',
        
        # Manifestes et configuration
        '.manifest', '.mui', '.mof', '.mfl', '.mum',
        
        # Registre et politique
        '.pol', '.adm', '.admx', '.adml', '.reg',
        
        # Données système
        '.dat', '.ini', '.cfg', '.config', '.xml',
        
        # Sécurité
        '.p7b', '.cer', '.crt', '.pfx',
    })
    
    # Patterns de fichiers système (regex)
    SYSTEM_FILE_PATTERNS = [
        re.compile(r'^ntuser\..*', re.IGNORECASE),
        re.compile(r'^usrclass\..*', re.IGNORECASE),
        re.compile(r'^system\..*', re.IGNORECASE),
        re.compile(r'^sam\..*', re.IGNORECASE),
        re.compile(r'^security\..*', re.IGNORECASE),
        re.compile(r'^software\..*', re.IGNORECASE),
        re.compile(r'^default\..*', re.IGNORECASE),
        re.compile(r'^boot.*\.log$', re.IGNORECASE),
        re.compile(r'^setupapi\..*\.log$', re.IGNORECASE),
        re.compile(r'^.*\.sys$', re.IGNORECASE),
        re.compile(r'^.*\.drv$', re.IGNORECASE),
        re.compile(r'^.*\.inf$', re.IGNORECASE),
        re.compile(r'^.*\.cat$', re.IGNORECASE),
    ]
    
    # Dossiers temporaires AUTORISÉS UNIQUEMENT
    @staticmethod
    def get_allowed_temp_directories():
        """Retourne les dossiers temporaires autorisés"""
        allowed = set()
        
        # Temp utilisateur
        if os.getenv('TEMP'):
            allowed.add(os.path.normpath(os.getenv('TEMP')))
        if os.getenv('TMP'):
            allowed.add(os.path.normpath(os.getenv('TMP')))
        
        # Temp Windows (avec précaution)
        windir = os.getenv('WINDIR', 'C:\\Windows')
        windows_temp = os.path.join(windir, 'Temp')
        if os.path.exists(windows_temp):
            allowed.add(os.path.normpath(windows_temp))
        
        return frozenset(allowed)
    
    @staticmethod
    def is_path_safe(path: str) -> bool:
        """
        Vérifie si un chemin est sûr à manipuler
        
        Args:
            path: Chemin à vérifier
            
        Returns:
            bool: True si sûr, False sinon
        """
        if not path:
            return False
        
        try:
            # Normaliser le chemin
            normalized_path = os.path.normpath(os.path.abspath(path))
            
            # Vérifier les chemins critiques
            for critical_path in WindowsSecurityCore.CRITICAL_SYSTEM_PATHS:
                critical_normalized = os.path.normpath(critical_path)
                
                # Vérifier si le chemin est dans un répertoire critique
                if normalized_path.lower().startswith(critical_normalized.lower()):
                    return False
                
                # Vérifier si c'est exactement un chemin critique
                if normalized_path.lower() == critical_normalized.lower():
                    return False
            
            # Vérifier les dossiers protégés dans le chemin
            path_parts = Path(normalized_path).parts
            for part in path_parts:
                if part in WindowsSecurityCore.PROTECTED_FOLDER_NAMES:
                    return False
            
            # Vérifier si c'est un fichier système critique
            filename = os.path.basename(normalized_path).lower()
            if filename in {f.lower() for f in WindowsSecurityCore.CRITICAL_SYSTEM_FILES}:
                return False
            
            # Vérifier l'extension
            _, ext = os.path.splitext(normalized_path)
            if ext.lower() in WindowsSecurityCore.PROTECTED_EXTENSIONS:
                # Exception: fichiers .tmp dans les dossiers temp autorisés
                if ext.lower() == '.tmp':
                    parent_dir = os.path.dirname(normalized_path)
                    allowed_temps = WindowsSecurityCore.get_allowed_temp_directories()
                    if any(parent_dir.lower().startswith(allowed.lower()) for allowed in allowed_temps):
                        return True
                return False
            
            # Vérifier les patterns de fichiers système
            for pattern in WindowsSecurityCore.SYSTEM_FILE_PATTERNS:
                if pattern.match(filename):
                    return False
            
            return True
            
        except Exception as e:
            # En cas d'erreur, refuser par sécurité
            print(f"[SECURITY] Error checking path safety: {e}")
            return False
    
    @staticmethod
    def is_in_allowed_temp_directory(path: str) -> bool:
        """
        Vérifie si un chemin est dans un dossier temporaire autorisé
        
        Args:
            path: Chemin à vérifier
            
        Returns:
            bool: True si dans un dossier temp autorisé
        """
        if not path:
            return False
        
        try:
            normalized_path = os.path.normpath(os.path.abspath(path))
            allowed_temps = WindowsSecurityCore.get_allowed_temp_directories()
            
            for allowed_temp in allowed_temps:
                if normalized_path.lower().startswith(allowed_temp.lower()):
                    return True
            
            return False
            
        except Exception:
            return False
    
    @staticmethod
    def validate_operation(path: str, operation: str = "delete") -> tuple[bool, str]:
        """
        Valide une opération sur un fichier/dossier
        
        Args:
            path: Chemin du fichier/dossier
            operation: Type d'opération ("delete", "modify", "read")
            
        Returns:
            tuple: (is_safe, reason)
        """
        if not path:
            return False, "Chemin vide"
        
        # Vérifier la sécurité du chemin
        if not WindowsSecurityCore.is_path_safe(path):
            return False, "Chemin système protégé - Accès refusé"
        
        # Pour les opérations de suppression, vérifier qu'on est dans temp
        if operation == "delete":
            if not WindowsSecurityCore.is_in_allowed_temp_directory(path):
                return False, "Suppression autorisée uniquement dans les dossiers temporaires"
        
        return True, "Opération autorisée"


# Instance globale immuable
security_core = WindowsSecurityCore()
