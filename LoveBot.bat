@echo off
chcp 65001 >nul
title LoveBot — SkyMine Companion
cd /d "%~dp0"
echo Starting LoveBot...
node index.js
echo.
echo LoveBot stopped. Press any key to exit...
pause >nul
