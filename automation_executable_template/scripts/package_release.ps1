param(
    [Parameter(Mandatory = $true)]
    [string]$Version
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$DistFolder = Join-Path $ProjectRoot "dist\TaskAutomationApp"
if (-not (Test-Path $DistFolder)) {
    throw "Dist não encontrada. Rode scripts/build_windows.ps1 antes."
}

$ReleaseDir = Join-Path $ProjectRoot "release"
New-Item -ItemType Directory -Path $ReleaseDir -Force | Out-Null

$ZipPath = Join-Path $ReleaseDir "TaskAutomationApp-$Version.zip"
if (Test-Path $ZipPath) {
    Remove-Item $ZipPath -Force
}

Compress-Archive -Path $DistFolder\* -DestinationPath $ZipPath -Force
Write-Host "Pacote gerado: $ZipPath"
