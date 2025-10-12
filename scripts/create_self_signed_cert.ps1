# Script de création d'un certificat auto-signé pour le développement
# Pour la production, utilisez un certificat code signing officiel

param(
    [string]$CertName = "5GHz Cleaner Development",
    [string]$OutputPath = ".\cert"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Création d'un certificat auto-signé" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Créer le dossier de sortie
if (-not (Test-Path $OutputPath)) {
    New-Item -ItemType Directory -Path $OutputPath | Out-Null
}

# Créer le certificat auto-signé
Write-Host "[1/4] Création du certificat..." -ForegroundColor Yellow
$cert = New-SelfSignedCertificate `
    -Type CodeSigningCert `
    -Subject "CN=$CertName, O=UndKiMi, C=FR" `
    -KeyAlgorithm RSA `
    -KeyLength 4096 `
    -HashAlgorithm SHA256 `
    -NotAfter (Get-Date).AddYears(5) `
    -CertStoreLocation "Cert:\CurrentUser\My" `
    -KeyUsage DigitalSignature `
    -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3")

Write-Host "✓ Certificat créé: $($cert.Thumbprint)" -ForegroundColor Green

# Exporter le certificat (clé publique)
Write-Host "[2/4] Export du certificat public..." -ForegroundColor Yellow
$certPath = Join-Path $OutputPath "5GHz_Cleaner_Dev.cer"
Export-Certificate -Cert $cert -FilePath $certPath -Type CERT | Out-Null
Write-Host "✓ Certificat exporté: $certPath" -ForegroundColor Green

# Exporter le certificat avec clé privée (protégé par mot de passe)
Write-Host "[3/4] Export du certificat avec clé privée..." -ForegroundColor Yellow
$pfxPath = Join-Path $OutputPath "5GHz_Cleaner_Dev.pfx"
$password = ConvertTo-SecureString -String "5GHzCleaner2024!" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath $pfxPath -Password $password | Out-Null
Write-Host "✓ PFX exporté: $pfxPath" -ForegroundColor Green
Write-Host "  Mot de passe: 5GHzCleaner2024!" -ForegroundColor Cyan

# Installer le certificat dans Trusted Root (pour le développement)
Write-Host "[4/4] Installation dans Trusted Root..." -ForegroundColor Yellow
$store = New-Object System.Security.Cryptography.X509Certificates.X509Store("Root", "CurrentUser")
$store.Open("ReadWrite")
$store.Add($cert)
$store.Close()
Write-Host "✓ Certificat installé dans Trusted Root" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "CERTIFICAT CRÉÉ AVEC SUCCÈS" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Informations du certificat:" -ForegroundColor Cyan
Write-Host "  Thumbprint: $($cert.Thumbprint)" -ForegroundColor White
Write-Host "  Subject: $($cert.Subject)" -ForegroundColor White
Write-Host "  Valide jusqu'à: $($cert.NotAfter)" -ForegroundColor White
Write-Host ""
Write-Host "Fichiers créés:" -ForegroundColor Cyan
Write-Host "  $certPath" -ForegroundColor White
Write-Host "  $pfxPath" -ForegroundColor White
Write-Host ""
Write-Host "IMPORTANT:" -ForegroundColor Yellow
Write-Host "  - Ce certificat est AUTO-SIGNÉ (développement uniquement)" -ForegroundColor Yellow
Write-Host "  - Pour la PRODUCTION, obtenez un certificat officiel" -ForegroundColor Yellow
Write-Host "  - Coût: 300-500€/an (DigiCert, Sectigo, etc.)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Pour signer un fichier:" -ForegroundColor Cyan
Write-Host "  signtool sign /f '$pfxPath' /p '5GHzCleaner2024!' /tr http://timestamp.digicert.com /td SHA256 /fd SHA256 fichier.exe" -ForegroundColor White
Write-Host ""
