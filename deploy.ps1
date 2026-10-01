# Despliegue completo de Senal Abierta (Windows):
#   build -> csp -> smoke -> package -> deploy -> IndexNow
#
#   powershell -ExecutionPolicy Bypass -File deploy.ps1
#
# Corta en cuanto algo falla; IndexNow es lo unico no bloqueante (el deploy
# ya esta en vivo cuando se notifica).
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

python scripts\build_pages.py
if ($LASTEXITCODE -ne 0) { exit 1 }
python scripts\csp_hashes.py
if ($LASTEXITCODE -ne 0) { exit 1 }
python scripts\smoke_site.py
if ($LASTEXITCODE -ne 0) { exit 1 }
python scripts\package_site.py
if ($LASTEXITCODE -ne 0) { exit 1 }
npx wrangler pages deploy dist --project-name senalabierta --branch=main --commit-dirty=true
if ($LASTEXITCODE -ne 0) { exit 1 }

python scripts\indexnow_ping.py
if ($LASTEXITCODE -ne 0) { Write-Warning "IndexNow fallo (el deploy YA esta en vivo)" }
Write-Output "DEPLOY OK"
