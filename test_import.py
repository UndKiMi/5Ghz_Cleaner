"""
Test script to verify all imports work correctly
"""
import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')

print("=" * 50)
print("5Gh'z Cleaner - Import Test")
print("=" * 50)
print()

# Test backend imports
print("Testing backend imports...")
try:
    from backend import cleaner, elevation
    print("[OK] Backend imports successful")
    print(f"   - cleaner module: {cleaner.__name__}")
    print(f"   - elevation module: {elevation.__name__}")
except Exception as e:
    print(f"[FAIL] Backend import failed: {e}")
    sys.exit(1)

print()

# Test frontend imports
print("Testing frontend imports...")
try:
    import flet as ft
    print("[OK] Flet import successful")
except Exception as e:
    print(f"[FAIL] Flet import failed: {e}")
    sys.exit(1)

try:
    from frontend import app
    print("[OK] Frontend imports successful")
    print(f"   - app module: {app.__name__}")
except Exception as e:
    print(f"[FAIL] Frontend import failed: {e}")
    sys.exit(1)

print()

# Test backend functions availability
print("Testing backend functions...")
functions_to_test = [
    'clear_temp',
    'clear_prefetch',
    'clear_recent',
    'clear_thumbnail_cache',
    'clear_crash_dumps',
    'clear_windows_old',
    'clear_windows_update_cache',
    'empty_recycle_bin',
    'stop_services',
    'clear_standby_memory',
    'flush_dns',
    'disable_telemetry',
    'clear_large_logs',
]

all_found = True
for func_name in functions_to_test:
    if hasattr(cleaner, func_name):
        print(f"   [OK] {func_name}")
    else:
        print(f"   [FAIL] {func_name} NOT FOUND")
        all_found = False

if not all_found:
    sys.exit(1)

print()

# Test elevation functions
print("Testing elevation functions...")
if hasattr(elevation, 'is_admin'):
    is_admin = elevation.is_admin()
    print(f"   [OK] is_admin() = {is_admin}")
else:
    print("   [FAIL] is_admin() NOT FOUND")
    sys.exit(1)

if hasattr(elevation, 'elevate'):
    print("   [OK] elevate() found")
else:
    print("   [FAIL] elevate() NOT FOUND")
    sys.exit(1)

print()
print("=" * 50)
print("[SUCCESS] All tests passed!")
print("=" * 50)
print()
print("You can now run the application with:")
print("  py main.py")
print()
