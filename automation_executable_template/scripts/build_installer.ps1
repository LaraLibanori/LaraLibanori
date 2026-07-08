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

$IssPath = Join-Path $PSScriptRoot "installer.iss"
if (-not (Test-Path $IssPath)) {
    throw "Arquivo Inno Setup não encontrado: $IssPath"
}

$Iscc = Get-Command ISCC -ErrorAction SilentlyContinue
if (-not $Iscc) {
    throw "ISCC (Inno Setup) não encontrado no PATH."
}

& $Iscc.Source "/DAppVersion=$Version" $IssPath
Write-Host "Instalador gerado em .\release"
