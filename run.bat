@echo off
chcp 65001 >nul
REM Запуск программы. Можно передать путь к конфигу.
cd /d "%~dp0"
python src\main.py %*
