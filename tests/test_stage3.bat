@echo off
chcp 65001 >nul
REM Этап 3: граф зависимостей (BFS с рекурсией), тестовый режим
cd /d "%~dp0.."
echo === 1. Простой граф ===
python src\main.py tests\stage3_simple.json
echo.
echo === 2. Цикл A - B - D - A ===
python src\main.py tests\stage3_cycle.json
echo.
echo === 3. Тот же цикл, старт с C ===
python src\main.py tests\stage3_cycle_from_c.json
echo.
echo === 4. Цепочка из 5 пакетов ===
python src\main.py tests\stage3_chain.json
echo.
echo === 5. Пакет зависит сам от себя ===
python src\main.py tests\stage3_self.json
echo.
echo === 6. Пакет без зависимостей ===
python src\main.py tests\stage3_alone.json
echo.
echo === 7. Пакета нет в тестовом репозитории ===
python src\main.py tests\stage3_unknown.json
echo.
echo === 8. Ошибка: маленькая буква ===
python src\main.py tests\stage3_bad_name.json
echo.
echo === 9. Ошибка: нет двоеточия ===
python src\main.py tests\stage3_no_colon.json
echo.
echo === 10. Ошибка: нет файла репозитория ===
python src\main.py tests\stage3_no_file.json
echo.
echo === 11. Реальный репозиторий: curl ===
python src\main.py tests\stage3_curl.json
echo.
pause
