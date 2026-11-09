@echo off
chcp 65001 >nul
REM Этап 5: Mermaid и PNG
cd /d "%~dp0.."
echo === 1. curl ===
python src\main.py tests\stage5_curl.json
echo.
echo === 2. nano ===
python src\main.py tests\stage5_nano.json
echo.
echo === 3. jq ===
python src\main.py tests\stage5_jq.json
echo.
echo === 4. Тестовый граф с циклом ===
python src\main.py tests\stage5_cycle.json
echo.
echo === 5. Ошибка: папки для картинки нет ===
python src\main.py tests\stage5_bad_path.json
echo.
pause
