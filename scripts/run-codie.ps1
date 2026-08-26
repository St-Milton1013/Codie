[CmdletBinding()]
param(
    [string]$WorkspaceRoot,
    [ValidateRange(1, 65535)]
    [int]$Port = 8765,
    [switch]$NoBrowser
)

$ErrorActionPreference = "Stop"
$repositoryRoot = Split-Path -Parent $PSScriptRoot
$uiIndex = Join-Path $repositoryRoot "ui\dist\index.html"

if ([string]::IsNullOrWhiteSpace($WorkspaceRoot)) {
    $WorkspaceRoot = Join-Path $repositoryRoot "work\local-codie"
}

if (-not (Test-Path -LiteralPath $uiIndex -PathType Leaf)) {
    throw "Codie's UI is not built. Run .\scripts\setup-codie-ui.ps1 once, then retry."
}

$python = $null
$repositoryPython = Join-Path $repositoryRoot ".venv\Scripts\python.exe"
$userCodiePython = Join-Path $env:USERPROFILE ".venvs\codie-py312\Scripts\python.exe"
if (-not [string]::IsNullOrWhiteSpace($env:CODIE_PYTHON)) {
    if (-not (Test-Path -LiteralPath $env:CODIE_PYTHON -PathType Leaf)) {
        throw "CODIE_PYTHON does not point to an existing Python executable."
    }
    $python = $env:CODIE_PYTHON
}
elseif (Test-Path -LiteralPath $repositoryPython -PathType Leaf) {
    $python = $repositoryPython
}
elseif (Test-Path -LiteralPath $userCodiePython -PathType Leaf) {
    $python = $userCodiePython
}
elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $python = "py"
}
elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $python = "python"
}
else {
    throw "Python 3.12 or newer is required to run Codie."
}

$arguments = @()
if ($python -eq "py") {
    $arguments += "-3.12"
}
$arguments += @(
    "-m",
    "codie.local_app",
    "--workspace-root",
    $WorkspaceRoot,
    "--port",
    $Port.ToString()
)
if (-not $NoBrowser) {
    $arguments += "--open-browser"
}

Push-Location -LiteralPath $repositoryRoot
try {
    & $python @arguments
}
finally {
    Pop-Location
}
