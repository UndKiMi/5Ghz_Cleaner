"""
5Gh'z Cleaner - Main Entry Point
Windows Cleaning & Optimisation Tool

Author: UndKiMi
Repository: https://github.com/UndKiMi/5Ghz_Cleaner
"""
import sys
import flet as ft
from backend.elevation import elevate
from frontend.app import main


if __name__ == "__main__":
    print("=" * 60)
    print("5Gh'z Cleaner - Windows Cleaning & Optimisation Tool")
    print("Author: UndKiMi")
    print("=" * 60)
    print()
    
    # Request administrator privileges
    print("[INFO] Checking administrator privileges...")
    elevate()
    print("[INFO] Administrator privileges confirmed")
    print()
    
    # Launch Flet application
    print("[INFO] Launching Flet application...")
    ft.app(target=main)
    print()
    print("[INFO] Application closed")
    print("=" * 60)
