"""
Backend module for 5Gh'z Cleaner
Contains all cleaning and optimization functions
"""
import os
import sys
import ctypes
import shutil
import subprocess


def run_hidden(cmd):
    """Execute a command without showing a window"""
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.run(
        cmd,
        shell=False,
        startupinfo=si,
        creationflags=subprocess.CREATE_NO_WINDOW,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


def get_recycle_bin_count():
    """Get the number of items in the recycle bin"""
    try:
        c = run_hidden(['PowerShell.exe', '-Command', '(Get-ChildItem -Path "Shell:RecycleBinFolder").Count'])
        return int(c.stdout.decode().strip())
    except:
        return 0


def clear_temp(progress_callback=None):
    """Clear temporary files from user and system temp directories"""
    total = 0
    temp_dirs = [os.getenv('TEMP'), os.path.join(os.getenv('WINDIR'), 'Temp')]
    
    for d in temp_dirs:
        if os.path.exists(d):
            try:
                for f in os.listdir(d):
                    fpath = os.path.join(d, f)
                    try:
                        if os.path.isfile(fpath) or os.path.islink(fpath):
                            os.unlink(fpath)
                        elif os.path.isdir(fpath):
                            shutil.rmtree(fpath)
                        total += 1
                    except:
                        pass
            except:
                pass
    
    return {"temp_deleted": total}


def clear_windows_update_cache(progress_callback=None):
    """Clear Windows Update download cache"""
    folder = os.path.join(os.getenv('WINDIR'), 'SoftwareDistribution', 'Download')
    deleted = 0
    
    if os.path.isdir(folder):
        try:
            for f in os.listdir(folder):
                fpath = os.path.join(folder, f)
                try:
                    if os.path.isfile(fpath) or os.path.islink(fpath):
                        os.unlink(fpath)
                    elif os.path.isdir(fpath):
                        shutil.rmtree(fpath)
                    deleted += 1
                except:
                    pass
            shutil.rmtree(folder, ignore_errors=True)
        except:
            pass
    
    return {"update_deleted": deleted}


def empty_recycle_bin(progress_callback=None):
    """Empty the Windows recycle bin"""
    before = get_recycle_bin_count()
    run_hidden(['PowerShell.exe', '-Command', 'Clear-RecycleBin -Force'])
    return {"recycle_bin_deleted": before}


def stop_services(services, progress_callback=None):
    """Stop specified Windows services"""
    stopped = []
    for s in services:
        if run_hidden(['sc', 'stop', s]).returncode == 0:
            stopped.append(s)
    return {"services_stopped": stopped}


def clear_prefetch(progress_callback=None):
    """Clear Windows prefetch files"""
    folder = os.path.join(os.getenv('WINDIR'), 'Prefetch')
    deleted = 0
    
    if os.path.isdir(folder):
        try:
            for f in os.listdir(folder):
                fpath = os.path.join(folder, f)
                try:
                    if os.path.isfile(fpath):
                        os.unlink(fpath)
                        deleted += 1
                except:
                    pass
        except:
            pass
    
    return {"prefetch_cleared": deleted}


def clear_recent(progress_callback=None):
    """Clear recent files history"""
    folder = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Recent')
    deleted = 0
    
    if os.path.isdir(folder):
        try:
            for f in os.listdir(folder):
                fpath = os.path.join(folder, f)
                try:
                    if os.path.isfile(fpath):
                        os.unlink(fpath)
                        deleted += 1
                except:
                    pass
        except:
            pass
    
    return {"recent_cleared": deleted}


def clear_thumbnail_cache(progress_callback=None):
    """Clear Windows thumbnail cache"""
    folder = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Windows\Explorer')
    deleted = 0
    
    if os.path.isdir(folder):
        try:
            for f in os.listdir(folder):
                if f.startswith("thumbcache") and f.endswith(".db"):
                    fpath = os.path.join(folder, f)
                    try:
                        os.unlink(fpath)
                        deleted += 1
                    except:
                        pass
        except:
            pass
    
    return {"thumbs_cleared": deleted}


def clear_crash_dumps(progress_callback=None):
    """Clear crash dump files"""
    deleted = 0
    
    # Local crash dumps
    folder = os.path.expandvars(r'%LOCALAPPDATA%\CrashDumps')
    if os.path.isdir(folder):
        try:
            for f in os.listdir(folder):
                fpath = os.path.join(folder, f)
                try:
                    if os.path.isfile(fpath):
                        os.unlink(fpath)
                        deleted += 1
                except:
                    pass
        except:
            pass
    
    # Minidump folder
    minidump = os.path.join(os.getenv("WINDIR"), "Minidump")
    if os.path.isdir(minidump):
        try:
            for f in os.listdir(minidump):
                fpath = os.path.join(minidump, f)
                try:
                    if os.path.isfile(fpath):
                        os.unlink(fpath)
                        deleted += 1
                except:
                    pass
        except:
            pass
    
    # Memory dump
    memdump = os.path.join(os.getenv("WINDIR"), "MEMORY.DMP")
    if os.path.isfile(memdump):
        try:
            os.unlink(memdump)
            deleted += 1
        except:
            pass
    
    return {"dumps_deleted": deleted}


def clear_windows_old(progress_callback=None):
    """Remove Windows.old folder from previous installations"""
    folder = os.path.normpath(os.path.join(os.getenv('WINDIR'), '..', 'Windows.old'))
    deleted = 0
    
    if os.path.isdir(folder):
        try:
            shutil.rmtree(folder, ignore_errors=True)
            deleted = 1
        except:
            pass
    
    return {'windows_old_deleted': deleted}


# Advanced functions
def clear_standby_memory(progress_callback=None):
    """Clear standby memory (RAM)"""
    try:
        run_hidden(["powershell", "-Command", "Clear-PhysicalMemoryStandbyList"])
        return {"ram_standby_cleared": True}
    except:
        return {"ram_standby_cleared": False}


def flush_dns(progress_callback=None):
    """Flush DNS cache"""
    try:
        res = run_hidden(["ipconfig", "/flushdns"])
        return {"dns_flushed": res.returncode == 0}
    except:
        return {"dns_flushed": False}


def disable_telemetry(progress_callback=None):
    """Disable Windows telemetry services"""
    diagnostic_svcs = ["DiagTrack", "dmwappushservice"]
    disabled = []
    
    for svc in diagnostic_svcs:
        try:
            run_hidden(["sc", "stop", svc])
            run_hidden(["sc", "config", svc, "start=disabled"])
            disabled.append(svc)
        except:
            pass
    
    return {"diag_disabled": len(disabled)}


def clear_large_logs(progress_callback=None):
    """Clear large log files"""
    log_dirs = [
        os.path.expandvars(r'%WINDIR%\Logs'),
        os.path.expandvars(r'%WINDIR%\Temp'),
        os.path.expandvars(r'%LOCALAPPDATA%\Temp')
    ]
    deleted = 0
    
    for d in log_dirs:
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.lower().endswith(".log"):
                    fpath = os.path.join(d, f)
                    try:
                        if os.path.isfile(fpath):
                            os.unlink(fpath)
                            deleted += 1
                    except:
                        pass
    
    return {"logs_deleted": deleted}


# Services to stop
SERVICES_TO_STOP = ["Fax", "MapsBroker", "WMPNetworkSvc", "Spooler", "RemoteRegistry"]
