"""Визуализатор графа зависимостей пакетов Alpine (Вариант №9)."""

import json
import sys

DEFAULT_CONFIG = "config.json"
REQUIRED_KEYS = ["package", "repository", "test_mode", "output_image"]
IMAGE_EXTENSION = ".png"


def load_config(path):
    """Читает JSON-файл конфигурации и возвращает словарь."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Ошибка: файл", path, "не найден")
    except json.JSONDecodeError:
        print("Ошибка:", path, "содержит некорректный JSON")
    sys.exit(1)


def is_text(value):
    """Проверяет, что значение — непустая строка."""
    return isinstance(value, str) and value.strip() != ""


def check_values(config):
    """Проверяет значения параметров и возвращает список ошибок."""
    errors = []
    if not is_text(config["package"]):
        errors.append("package должен быть непустой строкой")
    if not is_text(config["repository"]):
        errors.append("repository должен быть непустой строкой")
    if not isinstance(config["test_mode"], bool):
        errors.append("test_mode должен быть true или false")
    image = config["output_image"]
    if not is_text(image) or not image.endswith(IMAGE_EXTENSION):
        errors.append("output_image должен быть именем файла .png")
    return errors


def check_config(config):
    """Проверяет конфигурацию целиком и возвращает список ошибок."""
    if not isinstance(config, dict):
        return ["конфигурация должна быть объектом { ... }"]
    errors = []
    for key in REQUIRED_KEYS:
        if key not in config:
            errors.append("нет параметра " + key)
    if errors:
        return errors
    return check_values(config)


def main():
    """Точка входа: читает конфиг, печатает параметры и ошибки."""
    args = sys.argv[1:]
    path = args[0] if args else DEFAULT_CONFIG
    config = load_config(path)
    errors = check_config(config)
    if isinstance(config, dict):
        for key, value in config.items():
            print(key, "=", value)
    for error in errors:
        print("Ошибка:", error)
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
