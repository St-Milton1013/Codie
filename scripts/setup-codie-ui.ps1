[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$repositoryRoot = Split-Path -Parent $PSScriptRoot
$uiRoot = Join-Path $repositoryRoot "ui"

if (-not (Get-Command npm.cmd -ErrorAction SilentlyContinue)) {
    throw "npm is required to build the declared Codie UI dependencies."
}

Write-Host "Installing Codie's locked UI development dependencies..."
Push-Location -LiteralPath $uiRoot
try {
    npm.cmd ci
    npm.cmd run build
}
finally {
    Pop-Location
}

Write-Host "Codie UI is ready at $uiRoot\dist"
