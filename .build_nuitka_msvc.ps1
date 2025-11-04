# Build Nuitka avec MSVC - 5GHz Cleaner
# Optimisé pour réduire les faux positifs Windows Defender

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Build Nuitka avec MSVC - 5GHz Cleaner" -ForegroundColor Cyan
Write-Host "  Réduction faux positifs: 40-60% -> 5-15%" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier que MSVC est installé
Write-Host "[1/4] Vérification MSVC..." -ForegroundColor Yellow
$msvcPath = Get-Command cl.exe -ErrorAction SilentlyContinue
if (-not $msvcPath) {
    Write-Host "[ERREUR] MSVC non trouvé. Ouvrir Developer Command Prompt for VS 2022" -ForegroundColor Red
    Write-Host "Puis relancer ce script depuis cette console." -ForegroundColor Yellow
    pause
    exit 1
}
Write-Host "  [OK] MSVC trouvé: $($msvcPath.Source)" -ForegroundColor Green
Write-Host ""

# Nettoyer ancien exe
Write-Host "[2/4] Nettoyage..." -ForegroundColor Yellow
if (Test-Path "5GHz_Cleaner.exe") {
    Remove-Item -Force "5GHz_Cleaner.exe"
    Write-Host "  [OK] Ancien exe supprimé" -ForegroundColor Green
}
Write-Host ""

# Build Nuitka
Write-Host "[3/4] Compilation Nuitka (10-15 minutes)..." -ForegroundColor Yellow
Write-Host "  Ne fermez pas cette fenêtre !" -ForegroundColor Red
Write-Host ""

py -m nuitka `
    --standalone `
    --onefile `
    --msvc=latest `
    --windows-console-mode=attach `
    --company-name=UndKiMi `
    --product-name="5GHz Cleaner" `
    --file-version=1.7.0.0 `
    --product-version=1.7.0 `
    --file-description="Windows 11 Cleaning Tool" `
    --copyright="Copyright (c) 2025 UndKiMi" `
    --enable-plugin=anti-bloat `
    --assume-yes-for-downloads `
    --include-data-dir=libs=libs `
    --include-data-dir=assets=assets `
    --include-data-dir=config=config `
    --output-filename=5GHz_Cleaner.exe `
    --output-dir=dist_nuitka `
    main.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERREUR] Build échoué (code: $LASTEXITCODE)" -ForegroundColor Red
    pause
    exit 1
}

# Déplacer exe et nettoyer
Write-Host ""
Write-Host "[4/4] Finalisation..." -ForegroundColor Yellow
Move-Item -Force "dist_nuitka\5GHz_Cleaner.exe" "."
Remove-Item -Recurse -Force "dist_nuitka"
Write-Host "  [OK] Exe déplacé et fichiers temporaires supprimés" -ForegroundColor Green
Write-Host ""

# Hash SHA256
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  BUILD REUSSI !" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
$hash = (Get-FileHash -Path "5GHz_Cleaner.exe" -Algorithm SHA256).Hash
$size = [math]::Round((Get-Item "5GHz_Cleaner.exe").Length / 1MB, 2)
Write-Host "Fichier: 5GHz_Cleaner.exe" -ForegroundColor White
Write-Host "Taille: $size MB" -ForegroundColor White
Write-Host "SHA256: $hash" -ForegroundColor White
Write-Host ""
Write-Host "Taux faux positifs attendu: 5-15% (vs 40-60% PyInstaller)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
pause
