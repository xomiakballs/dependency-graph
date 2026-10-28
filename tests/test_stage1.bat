@echo off
REM Этап 1: вывод параметров и обработка ошибок конфига
cd /d "%~dp0.."
echo === 1. Правильный config.json ===
python src\main.py config.json
echo.
echo === 2. Файла нет ===
python src\main.py tests\net_takogo.json
echo.
echo === 3. Некорректный JSON ===
python src\main.py tests\broken.json
echo.
echo === 4. Не объект ===
python src\main.py tests\not_object.json
echo.
echo === 5. Нет параметра package ===
python src\main.py tests\no_package.json
echo.
echo === 6. Неверные значения ===
python src\main.py tests\bad_values.json
pause
