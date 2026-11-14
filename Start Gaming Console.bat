@echo off
title Phone Gamepad
cd /d "%~dp0"
echo Getting things ready (first time can take a minute)...
python -m pip install -q -r requirements.txt
if errorlevel 1 (
  echo.
  echo Could not install the needed parts. Check your internet connection and try again.
  pause
  exit /b
)
cls
python server.py
pause
