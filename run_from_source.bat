@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  py -3.12 -m venv .venv
  if errorlevel 1 goto :error
)
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
if errorlevel 1 goto :error
python -m pip install -r requirements.txt
if errorlevel 1 goto :error
start "" "%~dp0.venv\Scripts\pythonw.exe" "%~dp0main.py"
if errorlevel 1 goto :error
exit /b 0
:error
echo.
echo An error occurred. Read the message above.
pause
exit /b 1
