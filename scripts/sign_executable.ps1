# Script de signature d'exécutable avec certificat auto-signé
param(
    [Parameter(Mandatory=$true)]
    [string]$FilePath,
    
    [string]$CertPath = ".\cert\5GHz_Cleaner_Dev.pfx",
    [string]$Password = "5GHzCleaner2024!"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Signature d'exécutable" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier que le fichier existe
if (-not (Test-Path $FilePath)) {
    Write-Host "❌ ERREUR: Fichier introuvable: $FilePath" -ForegroundColor Red
    exit 1
}

# Vérifier que le certificat existe
if (-not (Test-Path $CertPath)) {
    Write-Host "❌ ERREUR: Certificat introuvable: $CertPath" -ForegroundColor Red
    Write-Host "Exécutez d'abord: .\create_self_signed_cert.ps1" -ForegroundColor Yellow
    exit 1
}

Write-Host "Fichier à signer: $FilePath" -ForegroundColor White
Write-Host "Certificat: $CertPath" -ForegroundColor White
Write-Host ""

# Vérifier si signtool est disponible
$signtool = Get-Command signtool.exe -ErrorAction SilentlyContinue

if (-not $signtool) {
    Write-Host "⚠️  signtool.exe non trouvé" -ForegroundColor Yellow
    Write-Host "Installation du Windows SDK requise" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Alternative: Utilisation de Set-AuthenticodeSignature" -ForegroundColor Cyan
    
    # Charger le certificat
    $cert = Get-PfxCertificate -FilePath $CertPath -Password (ConvertTo-SecureString -String $Password -AsPlainText -Force)
    
    # Signer avec PowerShell
    $result = Set-AuthenticodeSignature -FilePath $FilePath -Certificate $cert -TimestampServer "http://timestamp.digicert.com"
    
    if ($result.Status -eq "Valid") {
        Write-Host "✅ Fichier signé avec succès!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Vérification:" -ForegroundColor Cyan
        $sig = Get-AuthenticodeSignature -FilePath $FilePath
        Write-Host "  Status: $($sig.Status)" -ForegroundColor White
        Write-Host "  Signer: $($sig.SignerCertificate.Subject)" -ForegroundColor White
        Write-Host "  Timestamp: $($sig.TimeStamperCertificate.NotAfter)" -ForegroundColor White
    } else {
        Write-Host "❌ Échec de la signature: $($result.Status)" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✓ signtool.exe trouvé: $($signtool.Source)" -ForegroundColor Green
    Write-Host ""
    
    # Signer avec signtool
    Write-Host "Signature en cours..." -ForegroundColor Yellow
    $signArgs = @(
        "sign",
        "/f", $CertPath,
        "/p", $Password,
        "/tr", "http://timestamp.digicert.com",
        "/td", "SHA256",
        "/fd", "SHA256",
        "/v",
        $FilePath
    )
    
    & signtool.exe $signArgs
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Fichier signé avec succès!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "❌ Échec de la signature (code: $LASTEXITCODE)" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "SIGNATURE TERMINÉE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANT:" -ForegroundColor Yellow
Write-Host "  - Certificat AUTO-SIGNÉ (développement)" -ForegroundColor Yellow
Write-Host "  - Windows SmartScreen affichera un avertissement" -ForegroundColor Yellow
Write-Host "  - Pour la production: certificat officiel requis" -ForegroundColor Yellow
Write-Host ""
