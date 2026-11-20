@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Build Personnel Manager
 echo Building Personnel Manager for Windows 10/11 x64...
py -m pip install --upgrade pip
if errorlevel 1 goto failed
py -m pip install pyinstaller
if errorlevel 1 goto failed
py -m PyInstaller --noconfirm --clean --onefile --windowed --name PersonnelManager app.py
if errorlevel 1 goto failed
echo.
echo Finished: %~dp0dist\PersonnelManager.exe
echo Keep PersonnelManager.exe in a writable folder. The database will be created beside it.
pause
exit /b 0
:failed
echo.
echo Build failed. Install Python 3.10+ 64-bit and ensure the Python launcher is available.
pause
exit /b 1
