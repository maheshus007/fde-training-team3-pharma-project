# Run AEGIS-PHARMA submission tests (stdlib unittest via test.py)
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TestPy = Join-Path $ScriptDir "test.py"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "python not found on PATH"
    exit 1
}

Write-Host "Running: python `"$TestPy`""
python $TestPy
exit $LASTEXITCODE
