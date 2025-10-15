"""
Console Colors and Formatting Utilities
Provides colored output for better console readability
"""
import sys
import os

# Enable ANSI colors on Windows
if sys.platform == 'win32':
    os.system('')  # Enable ANSI escape sequences

class Colors:
    """ANSI color codes for console output"""
    # Reset
    RESET = '\033[0m'
    
    # Regular colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bold colors
    BOLD_BLACK = '\033[1;30m'
    BOLD_RED = '\033[1;31m'
    BOLD_GREEN = '\033[1;32m'
    BOLD_YELLOW = '\033[1;33m'
    BOLD_BLUE = '\033[1;34m'
    BOLD_MAGENTA = '\033[1;35m'
    BOLD_CYAN = '\033[1;36m'
    BOLD_WHITE = '\033[1;37m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'


def print_header(text, width=70):
    """Affiche un en-tête coloré"""
    print(f"\n{Colors.BOLD_CYAN}{'=' * width}{Colors.RESET}")
    print(f"{Colors.BOLD_WHITE}{text.center(width)}{Colors.RESET}")
    print(f"{Colors.BOLD_CYAN}{'=' * width}{Colors.RESET}\n")


def print_section(number, total, title):
    """Affiche une section numérotée"""
    print(f"{Colors.BOLD_YELLOW}[{number}/{total}]{Colors.RESET} {Colors.BOLD_WHITE}{title}{Colors.RESET}")


def print_success(message, indent=2):
    """Affiche un message de succès"""
    spaces = ' ' * indent
    print(f"{spaces}{Colors.BOLD_GREEN}[✓]{Colors.RESET} {Colors.GREEN}{message}{Colors.RESET}")


def print_error(message, indent=2):
    """Affiche un message d'erreur"""
    spaces = ' ' * indent
    print(f"{spaces}{Colors.BOLD_RED}[✗]{Colors.RESET} {Colors.RED}{message}{Colors.RESET}")


def print_warning(message, indent=2):
    """Affiche un avertissement"""
    spaces = ' ' * indent
    print(f"{spaces}{Colors.BOLD_YELLOW}[!]{Colors.RESET} {Colors.YELLOW}{message}{Colors.RESET}")


def print_info(message, indent=2):
    """Affiche une information"""
    spaces = ' ' * indent
    print(f"{spaces}{Colors.CYAN}[i]{Colors.RESET} {message}")


def print_separator(width=70):
    """Affiche un séparateur"""
    print(f"{Colors.BOLD_BLACK}{'-' * width}{Colors.RESET}")


def print_banner():
    """Affiche la bannière de démarrage"""
    banner = f"""
{Colors.BOLD_CYAN}╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║              {Colors.BOLD_WHITE}5GH'z CLEANER{Colors.BOLD_CYAN}                                        ║
║        {Colors.WHITE}Windows 11 Cleaning & Optimization Tool{Colors.BOLD_CYAN}              ║
║                                                                   ║
║  {Colors.CYAN}Auteur : {Colors.WHITE}UndKiMi{Colors.CYAN}  │  {Colors.CYAN}Version : {Colors.WHITE}1.6.0{Colors.CYAN}  │  {Colors.CYAN}Licence : {Colors.WHITE}CC BY-NC-SA{Colors.BOLD_CYAN}  ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)
