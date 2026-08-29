param(
    [string]$Python = "",
    [switch]$Recreate
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$VenvPath = Join-Path $RepoRoot ".venv"

if ([string]::IsNullOrWhiteSpace($Python)) {
    $BundledPython = Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
    if (Test-Path -LiteralPath $BundledPython) {
        $Python = $BundledPython
    } else {
        $Python = "py -3.12"
    }
}

Push-Location $RepoRoot
try {
    if ($Recreate -and (Test-Path -LiteralPath $VenvPath)) {
        $Resolved = (Resolve-Path -LiteralPath $VenvPath).Path
        $Expected = (Join-Path (Resolve-Path -LiteralPath $RepoRoot).Path ".venv")
        if ($Resolved -ne $Expected) {
            throw "Refusing to remove unexpected venv path: $Resolved"
        }
        Remove-Item -LiteralPath $Resolved -Recurse -Force
    }

    if (-not (Test-Path -LiteralPath $VenvPath)) {
        if ($Python -like "py *") {
            $Parts = $Python.Split(" ", 2)
            & $Parts[0] $Parts[1] -m venv .venv
        } else {
            & $Python -m venv .venv
        }
    }

    .\.venv\Scripts\python.exe --version
    .\.venv\Scripts\python.exe -m pip install --upgrade pip
    .\.venv\Scripts\python.exe -m pip install --no-build-isolation -e .[dev]
    .\.venv\Scripts\python.exe -m pip check
    .\.venv\Scripts\python.exe -c "import kaggle_environments, agricola; print('kaggle_environments', kaggle_environments.__version__)"
}
finally {
    Pop-Location
}
