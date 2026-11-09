"""Визуализатор графа зависимостей пакетов Alpine (Вариант №9)."""

import json
import sys

import apk
import graph
import visual

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


def fail(message):
    """Печатает сообщение об ошибке и завершает программу."""
    print("Ошибка:", message)
    sys.exit(1)


def make_test_source(config):
    """Готовит источник зависимостей из файла тестового репозитория."""
    try:
        repo = graph.load_test_repo(config["repository"])
    except graph.TestRepoError as error:
        fail(error)
    return repo, lambda name: repo.get(name, [])


def make_apk_source(config):
    """Готовит источник зависимостей из репозитория Alpine."""
    try:
        packages = apk.load_index(config["repository"])
    except apk.RepositoryError as error:
        fail(error)
    providers = apk.build_providers(packages)
    return packages, lambda name: apk.direct_dependencies(
        packages, providers, name)


def draw_graph(dependency_graph, image_path):
    """Выводит граф на языке Mermaid и сохраняет его картинку в PNG."""
    mermaid_text = visual.to_mermaid(dependency_graph)
    print("Граф на языке Mermaid:")
    print(mermaid_text)
    try:
        visual.save_png(mermaid_text, image_path)
    except (OSError, ValueError) as error:
        fail("не удалось сохранить изображение графа: " + str(error))
    print("Изображение графа сохранено в файл " + image_path)


def show_graph(config):
    """Строит и выводит полный граф зависимостей пакета."""
    if config["test_mode"]:
        known, get_deps = make_test_source(config)
    else:
        known, get_deps = make_apk_source(config)
    name = config["package"]
    if name not in known:
        fail("пакет " + name + " не найден в репозитории")
    dependency_graph = graph.build_graph(get_deps, name)
    print("Граф зависимостей пакета " + name + ":")
    for package, deps in dependency_graph.items():
        targets = ", ".join(deps) if deps else "(нет зависимостей)"
        print("  " + package + " -> " + targets)
    draw_graph(dependency_graph, config["output_image"])


def main():
    """Точка входа: читает конфиг и выводит граф зависимостей пакета."""
    args = sys.argv[1:]
    path = args[0] if args else DEFAULT_CONFIG
    config = load_config(path)
    errors = check_config(config)
    for error in errors:
        print("Ошибка:", error)
    if errors:
        sys.exit(1)
    show_graph(config)


if __name__ == "__main__":
    main()
