@echo off
REM Этап 2: прямые зависимости пакета из репозитория Alpine
cd /d "%~dp0.."
echo === 1. curl ===
python src\main.py tests\stage2_curl.json
echo.
echo === 2. python3 ===
python src\main.py tests\stage2_python3.json
echo.
echo === 3. musl - без зависимостей ===
python src\main.py tests\stage2_musl.json
echo.
echo === 4. Несуществующий пакет ===
python src\main.py tests\stage2_unknown_package.json
echo.
echo === 5. Несуществующий сайт ===
python src\main.py tests\stage2_bad_host.json
echo.
echo === 6. По адресу не архив ===
python src\main.py tests\stage2_not_index.json
echo.
echo === 7. Неверный адрес ===
python src\main.py tests\stage2_bad_url.json
echo.
pause
