@echo off
if exist ".venv\Scripts\python.exe" (
  .venv\Scripts\python.exe -m streamlit run HOMEPAGE.py
) else (
  echo Virtual environment not found. Create it with:
  echo    python -m venv .venv
)
pause
