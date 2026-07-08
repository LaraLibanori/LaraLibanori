param(
    [Parameter(Mandatory = $false)]
    [string]$BuildEpoch
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python não encontrado no PATH."
}

if ([string]::IsNullOrWhiteSpace($BuildEpoch)) {
    throw "Informe -BuildEpoch (Unix epoch) para build reproduzível."
}

$env:PYTHONHASHSEED = "0"
$env:SOURCE_DATE_EPOCH = $BuildEpoch

python -m pip install --upgrade pip
python -m pip install -r .\requirements.lock

# Se usar Playwright no projeto real, descomente:
# python -m playwright install chromium

python -m PyInstaller --clean .\build.spec
Write-Host "Build concluído em .\dist\TaskAutomationApp com SOURCE_DATE_EPOCH=$BuildEpoch"
