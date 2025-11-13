"""
Global settings and configuration for 5GHz Cleaner
Centralized configuration to avoid hardcoded values
"""
import os
import sys
import io

# ============================================================================
# SYSTEM CONFIGURATION
# ============================================================================

# Configure UTF-8 encoding for Windows console (centralized)
def configure_console_encoding():
    """Configure console encoding to UTF-8 for Windows"""
    try:
        if sys.platform == 'win32':
            # Configurer la console Windows pour UTF-8
            import ctypes
            kernel32 = ctypes.windll.kernel32
            # SetConsoleOutputCP(65001) = UTF-8
            kernel32.SetConsoleOutputCP(65001)
            kernel32.SetConsoleCP(65001)
        
        # Reconfigurer sys.stdout et sys.stderr avec UTF-8
        if hasattr(sys.stdout, 'buffer'):
            try:
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
            except (AttributeError, ValueError, OSError):
                pass
        if hasattr(sys.stderr, 'buffer'):
            try:
                sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)
            except (AttributeError, ValueError, OSError):
                pass
    except (AttributeError, ValueError, OSError, ImportError):
        # Already configured, not applicable, or buffer closed
        pass

# System paths (dynamic, not hardcoded)
SYSTEM_DRIVE = os.getenv('SystemDrive', 'C:')
SYSTEM_ROOT = os.getenv('SystemRoot', os.path.join(SYSTEM_DRIVE, 'Windows'))
SYSTEM32 = os.path.join(SYSTEM_ROOT, 'System32')
PROGRAM_FILES = os.getenv('ProgramFiles', os.path.join(SYSTEM_DRIVE, 'Program Files'))
PROGRAM_FILES_X86 = os.getenv('ProgramFiles(x86)', os.path.join(SYSTEM_DRIVE, 'Program Files (x86)'))
PROGRAM_DATA = os.getenv('ProgramData', os.path.join(SYSTEM_DRIVE, 'ProgramData'))

# ============================================================================
# APPLICATION SETTINGS
# ============================================================================

APP_NAME = "5GH'z Cleaner"
APP_VERSION = "MAJOR_UPDATE"
APP_AUTHOR = "UndKiMi"
APP_LICENSE = "CC BY-NC-SA 4.0"

# Windows version requirements
MIN_WINDOWS_BUILD = 22000  # Windows 11 minimum

# ============================================================================
# TIMEOUTS AND LIMITS
# ============================================================================

# Command timeouts (in seconds)
TIMEOUT_SC_COMMAND = 10  # Increased from 5 to 10
TIMEOUT_REG_COMMAND = 15  # Increased from 10 to 15
TIMEOUT_WMIC_COMMAND = 10  # Increased from 5 to 10
TIMEOUT_NVIDIA_SMI = 5

# File age limits (in hours/days)
MIN_FILE_AGE_HOURS = 2  # Don't delete files younger than 2 hours
MIN_UPDATE_CACHE_AGE_DAYS = 14  # Don't delete update cache younger than 14 days
MIN_PREFETCH_AGE_DAYS = 30  # Don't delete prefetch files younger than 30 days

# Size limits
MAX_SAFE_FILE_SIZE_MB = 500  # Don't delete files larger than 500 MB
MIN_DISK_SPACE_GB = 5  # Minimum free disk space required
MIN_RESTORE_POINT_SPACE_GB = 10  # Minimum space for restore point

# ============================================================================
# LOGGING SETTINGS
# ============================================================================

LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_TO_FILE = True
LOG_TO_CONSOLE = True

# ============================================================================
# SECURITY SETTINGS
# ============================================================================

VERIFY_SIGNATURE_ON_STARTUP = False  # Set to True to enable signature verification
ENABLE_TELEMETRY_CHECK = True  # Enable telemetry verification
STRICT_SECURITY_MODE = True  # Enable strict security checks

# ============================================================================
# UI SETTINGS
# ============================================================================

# Window dimensions
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 1019
WINDOW_MIN_WIDTH = 876
WINDOW_MIN_HEIGHT = 1019

# Animation settings
ANIMATION_DURATION_MS = 300
SHIELD_PULSE_INTERVAL_SEC = 2.0

# ============================================================================
# CLEANING OPTIONS (DEFAULT)
# ============================================================================

DEFAULT_CLEANING_OPTIONS = {
    "clear_standby_memory": True,
    "flush_dns": True,
    "disable_telemetry": False,
    "clear_large_logs": True,
    "empty_recycle_bin": False,  # Requires explicit confirmation
    "clear_windows_old": False,  # Requires explicit confirmation
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_system_path(*parts):
    """
    Get a system path dynamically based on system drive
    
    Args:
        *parts: Path components to join
        
    Returns:
        str: Full system path
    """
    return os.path.join(SYSTEM_DRIVE, *parts)

def get_windows_path(*parts):
    """
    Get a Windows directory path dynamically
    
    Args:
        *parts: Path components to join with Windows directory
        
    Returns:
        str: Full Windows path
    """
    return os.path.join(SYSTEM_ROOT, *parts)

def get_program_files_path(*parts):
    """
    Get a Program Files path dynamically
    
    Args:
        *parts: Path components to join with Program Files
        
    Returns:
        str: Full Program Files path
    """
    return os.path.join(PROGRAM_FILES, *parts)

# NOTE: Do NOT call configure_console_encoding() here automatically
# It should be called explicitly in main.py before any other imports
# to avoid "I/O operation on closed file" errors
