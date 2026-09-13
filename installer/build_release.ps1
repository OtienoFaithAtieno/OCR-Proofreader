$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue

$python = Join-Path $root ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    throw "Python virtual environment not found at $python"
}

& $python -m PyInstaller --noconfirm --clean --distpath dist --workpath build --specpath installer installer/Proofreader.spec

Write-Host ""
Write-Host "Release build complete. Output folder: $root\dist\Proofreader"
Write-Host "You can now zip the folder for distribution or convert it into an installer."
