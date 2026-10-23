@echo off
setlocal
cd /d "%~dp0"
python scripts\integrar_voz.py %*
