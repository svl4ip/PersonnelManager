@echo off
chcp 65001 >nul
py app.py
if errorlevel 1 pause
