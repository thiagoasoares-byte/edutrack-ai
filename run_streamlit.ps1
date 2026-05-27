$venv = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-Not (Test-Path $venv)) {
  Write-Error "Virtual environment not found at $venv. Create it with: python -m venv .venv"
  exit 1
}
& $venv -m streamlit run HOMEPAGE.py
