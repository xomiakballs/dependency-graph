@echo off
chcp 65001 >nul
REM Этап 4: порядок загрузки зависимостей
cd /d "%~dp0.."
echo === 1. Простой граф: D, B, C, A ===
python src\main.py tests\stage3_simple.json
echo.
echo === 2. Цепочка: E, D, C, B, A ===
python src\main.py tests\stage3_chain.json
echo.
echo === 3. Граф с циклом A - B - D - A ===
python src\main.py tests\stage3_cycle.json
echo.
echo === 4. Пакет зависит сам от себя ===
python src\main.py tests\stage3_self.json
echo.
echo === 5. Пакет без зависимостей ===
python src\main.py tests\stage3_alone.json
echo.
echo === 6. curl, Alpine 3.12 x86 (сравнение с apk) ===
python src\main.py tests\stage4_curl_312.json
echo.
echo === 7. curl, Alpine 3.20 x86_64 ===
python src\main.py tests\stage3_curl.json
echo.
pause
