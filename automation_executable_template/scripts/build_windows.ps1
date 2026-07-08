Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python não encontrado no PATH."
}

python -m pip install --upgrade pip
python -m pip install -r .\requirements.lock

# Se usar Playwright no projeto real, descomente:
# python -m playwright install chromium

python -m PyInstaller --clean .\build.spec
Write-Host "Build concluído em .\dist\TaskAutomationApp"
