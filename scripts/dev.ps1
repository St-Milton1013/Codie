param(
    [Parameter(Position = 0)]
    [ValidateSet("test", "test-verbose", "lint", "format", "typecheck", "schema", "validate", "precommit")]
    [string] $Task = "validate"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$BundledPython = Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

if (Test-Path $BundledPython) {
    $Python = $BundledPython
} else {
    $Python = "python"
}

function Invoke-Step {
    param(
        [string] $Name,
        [scriptblock] $Command
    )

    Write-Host ""
    Write-Host "==> $Name"
    & $Command
}

Push-Location $RepoRoot
try {
    switch ($Task) {
        "test" {
            Invoke-Step "Unit tests" { & $Python -m unittest discover -s tests }
        }
        "test-verbose" {
            Invoke-Step "Verbose unit tests" { & $Python -m unittest discover -s tests -v }
        }
        "lint" {
            Invoke-Step "Ruff lint" { & $Python -m ruff check . }
        }
        "format" {
            Invoke-Step "Ruff format" { & $Python -m ruff format . }
        }
        "typecheck" {
            Invoke-Step "Mypy typecheck" { & $Python -m mypy codie }
        }
        "schema" {
            Invoke-Step "Schema bootstrap guardrail" { & $Python scripts/check_schema.py }
        }
        "precommit" {
            Invoke-Step "Pre-commit hooks" { & $Python -m pre_commit run --all-files }
        }
        "validate" {
            Invoke-Step "Git diff whitespace check" { git diff --check }
            Invoke-Step "Schema bootstrap guardrail" { & $Python scripts/check_schema.py }
            Invoke-Step "Unit tests" { & $Python -m unittest discover -s tests }
        }
    }
} finally {
    Pop-Location
}
