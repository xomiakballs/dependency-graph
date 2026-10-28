@echo off
REM Запуск программы. Можно передать путь к конфигу.
cd /d "%~dp0"
python src\main.py %*
