"""
Elevation module for requesting administrator privileges
"""
import sys
import ctypes


def is_admin():
    """Check if the current process has administrator privileges"""
    try:
        result = ctypes.windll.shell32.IsUserAnAdmin()
        print(f"[INFO] Administrator check result: {result}")
        return result
    except Exception as e:
        print(f"[WARNING] Failed to check admin privileges: {e}")
        return False


def elevate():
    """Request administrator privileges if not already elevated"""
    try:
        if not is_admin():
            print("[WARNING] Application not running as administrator")
            print("[INFO] Requesting UAC elevation...")
            params = ' '.join([f'"{arg}"' for arg in sys.argv])
            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                sys.executable, 
                params, 
                None, 
                1
            )
            print("[INFO] UAC prompt displayed, waiting for user response...")
            sys.exit(0)
        else:
            print("[SUCCESS] Application running with administrator privileges")
    except Exception as e:
        print(f"[ERROR] Elevation failed: {e}")
        sys.exit(0)
