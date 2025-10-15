# ============================================================================
# 5GH'z Cleaner - Automated Build Script
# Version: 1.6.0
# Author: UndKiMi
# License: CC BY-NC-SA 4.0
# ============================================================================

param(
    [switch]$Clean,
    [switch]$Debug,
    [switch]$OneDir,
    [switch]$NoUPX,
    [switch]$SkipTests
)

# ============================================================================
# CONFIGURATION
# ============================================================================

$AppName = "5Ghz_Cleaner"
$Version = "1.6.0"
$BuildDir = "build"
$DistDir = "dist"
$SpecFile = "$AppName.spec"
$SpecTemplate = "$AppName.spec.template"

# Colors
$ColorSuccess = "Green"
$ColorError = "Red"
$ColorWarning = "Yellow"
$ColorInfo = "Cyan"

# ============================================================================
# FUNCTIONS
# ============================================================================

function Write-Step {
    param([string]$Message)
    Write-Host "`n[STEP] $Message" -ForegroundColor $ColorInfo
    Write-Host ("=" * 70) -ForegroundColor $ColorInfo
}

function Write-Success {
    param([string]$Message)
    Write-Host "  [OK] $Message" -ForegroundColor $ColorSuccess
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "  [ERROR] $Message" -ForegroundColor $ColorError
}

function Write-Warning-Custom {
    param([string]$Message)
    Write-Host "  [!] $Message" -ForegroundColor $ColorWarning
}

# ============================================================================
# BANNER
# ============================================================================

Clear-Host
Write-Host @"

  ╔═══════════════════════════════════════════════════════════════════╗
  ║                                                                   ║
  ║              5GH'z CLEANER - BUILD SCRIPT v$Version              ║
  ║                                                                   ║
  ║  Windows 11 Cleaning & Optimization Tool                         ║
  ║  Author: UndKiMi | License: CC BY-NC-SA 4.0                      ║
  ║                                                                   ║
  ╚═══════════════════════════════════════════════════════════════════╝

"@ -ForegroundColor $ColorInfo

# ============================================================================
# PRE-BUILD CHECKS
# ============================================================================

Write-Step "Pre-Build Checks"

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Success "Python found: $pythonVersion"
} catch {
    Write-Error-Custom "Python not found! Install Python 3.11+"
    exit 1
}

# Check PyInstaller
try {
    $pyinstallerVersion = pyinstaller --version 2>&1
    Write-Success "PyInstaller found: $pyinstallerVersion"
} catch {
    Write-Warning-Custom "PyInstaller not found. Installing..."
    pip install pyinstaller
}

# Check if spec template exists
if (-not (Test-Path $SpecTemplate)) {
    Write-Error-Custom "Spec template not found: $SpecTemplate"
    exit 1
}
Write-Success "Spec template found: $SpecTemplate"

# ============================================================================
# CLEAN BUILD
# ============================================================================

if ($Clean) {
    Write-Step "Cleaning Previous Build"
    
    if (Test-Path $BuildDir) {
        Remove-Item -Recurse -Force $BuildDir
        Write-Success "Removed: $BuildDir"
    }
    
    if (Test-Path $DistDir) {
        Remove-Item -Recurse -Force $DistDir
        Write-Success "Removed: $DistDir"
    }
    
    if (Test-Path $SpecFile) {
        Remove-Item -Force $SpecFile
        Write-Success "Removed: $SpecFile"
    }
    
    Get-ChildItem -Filter "*.pyc" -Recurse | Remove-Item -Force
    Get-ChildItem -Filter "__pycache__" -Recurse | Remove-Item -Recurse -Force
    Write-Success "Removed Python cache files"
}

# ============================================================================
# PREPARE SPEC FILE
# ============================================================================

Write-Step "Preparing Build Configuration"

# Copy template to spec file
Copy-Item $SpecTemplate $SpecFile -Force
Write-Success "Created spec file from template"

# Modify spec file based on parameters
$specContent = Get-Content $SpecFile -Raw

if ($Debug) {
    $specContent = $specContent -replace "CONSOLE_ENABLED = False", "CONSOLE_ENABLED = True"
    Write-Success "Debug mode enabled (console visible)"
}

if ($OneDir) {
    $specContent = $specContent -replace "ONE_FILE = True", "ONE_FILE = False"
    Write-Success "One-directory mode enabled (faster startup)"
}

if ($NoUPX) {
    $specContent = $specContent -replace "UPX_ENABLED = True", "UPX_ENABLED = False"
    Write-Success "UPX compression disabled"
}

Set-Content $SpecFile $specContent -NoNewline

# ============================================================================
# RUN TESTS (Optional)
# ============================================================================

if (-not $SkipTests) {
    Write-Step "Running Tests"
    
    # Test imports
    Write-Host "  Testing critical imports..."
    $testResult = python -c "
import sys
try:
    import flet
    import backend.cleaner
    import backend.security_core
    import frontend.app
    print('OK')
except Exception as e:
    print(f'ERROR: {e}')
    sys.exit(1)
"
    
    if ($testResult -eq "OK") {
        Write-Success "All imports successful"
    } else {
        Write-Error-Custom "Import test failed: $testResult"
        exit 1
    }
    
    # Verify signature
    Write-Host "  Verifying code signature..."
    python backend/signature_manager.py --verify
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Signature verification passed"
    } else {
        Write-Warning-Custom "Signature verification failed (continuing anyway)"
    }
}

# ============================================================================
# BUILD
# ============================================================================

Write-Step "Building Executable"

Write-Host "  Running PyInstaller..."
pyinstaller $SpecFile --clean

if ($LASTEXITCODE -ne 0) {
    Write-Error-Custom "Build failed!"
    exit 1
}

Write-Success "Build completed successfully!"

# ============================================================================
# POST-BUILD
# ============================================================================

Write-Step "Post-Build Tasks"

# Check if exe exists
$exePath = if ($OneDir) { "$DistDir\$AppName\$AppName.exe" } else { "$DistDir\$AppName.exe" }

if (Test-Path $exePath) {
    $exeSize = (Get-Item $exePath).Length / 1MB
    Write-Success "Executable created: $exePath ($([math]::Round($exeSize, 2)) MB)"
} else {
    Write-Error-Custom "Executable not found: $exePath"
    exit 1
}

# Generate checksums
Write-Host "  Generating checksums..."
$hash = Get-FileHash $exePath -Algorithm SHA256
$hashValue = $hash.Hash

$checksumFile = "$DistDir\CHECKSUMS_BUILD.txt"
@"
5GH'z Cleaner v$Version - Build Checksums
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

Executable: $AppName.exe
SHA-256: $hashValue

Verify with:
  Get-FileHash "$AppName.exe" -Algorithm SHA256

"@ | Out-File $checksumFile -Encoding UTF8

Write-Success "Checksums saved: $checksumFile"

# Copy documentation
Write-Host "  Copying documentation..."
Copy-Item "README.md" "$DistDir\" -Force -ErrorAction SilentlyContinue
Copy-Item "LICENSE" "$DistDir\" -Force -ErrorAction SilentlyContinue
Copy-Item "docs\reports\CHECKSUMS.txt" "$DistDir\" -Force -ErrorAction SilentlyContinue
Write-Success "Documentation copied"

# ============================================================================
# SUMMARY
# ============================================================================

Write-Step "Build Summary"

Write-Host @"

  Build Configuration:
    - Version:      $Version
    - Mode:         $(if ($OneDir) { "One Directory" } else { "One File" })
    - Console:      $(if ($Debug) { "Enabled (Debug)" } else { "Disabled" })
    - UPX:          $(if ($NoUPX) { "Disabled" } else { "Enabled" })
    - Size:         $([math]::Round($exeSize, 2)) MB
    
  Output:
    - Executable:   $exePath
    - Checksums:    $checksumFile
    
  Next Steps:
    1. Test the executable
    2. Run security scan
    3. Create release package
    4. Upload to GitHub Releases

"@ -ForegroundColor $ColorSuccess

Write-Host @"
  ╔═══════════════════════════════════════════════════════════════════╗
  ║                    BUILD COMPLETED SUCCESSFULLY!                  ║
  ╚═══════════════════════════════════════════════════════════════════╝

"@ -ForegroundColor $ColorSuccess

# ============================================================================
# USAGE EXAMPLES
# ============================================================================

<#
USAGE EXAMPLES:

# Standard build (one file, no console, with UPX)
.\build.ps1

# Clean build
.\build.ps1 -Clean

# Debug build (with console)
.\build.ps1 -Debug

# One directory build (faster startup)
.\build.ps1 -OneDir

# Build without UPX compression
.\build.ps1 -NoUPX

# Skip tests
.\build.ps1 -SkipTests

# Combine options
.\build.ps1 -Clean -Debug -OneDir

#>
