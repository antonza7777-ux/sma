@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

chcp 65001 >nul
title spammesenges V3 - ALT10
cd /d "%~dp0"

pip install keyboard pyperclip pyautogui >nul 2>&1

python "%~dp0configs\spammer.py" alt10

pause