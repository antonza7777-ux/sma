@echo off
chcp 65001 >nul
title spammesenges V3 - Settings
cd /d "%~dp0"
python "%~dp0configs\settings.py"
pause