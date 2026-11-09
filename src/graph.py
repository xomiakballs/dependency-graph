"""Построение графа зависимостей и работа с тестовым репозиторием."""


def bfs_step(get_deps, queue, visited, graph):
    """Один шаг BFS: берёт пакет из очереди и рекурсивно идёт дальше."""
    if not queue:
        return graph
    current = queue.pop(0)
    graph[current] = get_deps(current)
    for dep in graph[current]:
        if dep not in visited:
            visited.add(dep)
            queue.append(dep)
    return bfs_step(get_deps, queue, visited, graph)


def build_graph(get_deps, start):
    """Строит граф зависимостей пакета start с учётом транзитивности."""
    return bfs_step(get_deps, [start], {start}, {})

class TestRepoError(Exception):
    """Ошибка в файле тестового репозитория."""


def is_package_name(name):
    """Проверяет, что имя пакета состоит из больших латинских букв."""
    return name != "" and all("A" <= char <= "Z" for char in name)


def parse_test_line(line, number):
    """Разбирает строку вида 'A: B C' и возвращает (пакет, зависимости)."""
    where = "в строке " + str(number)
    name, sep, rest = line.partition(":")
    if not sep:
        raise TestRepoError(where + " нет двоеточия")
    name = name.strip()
    deps = rest.split()
    for item in [name] + deps:
        if not is_package_name(item):
            raise TestRepoError(where + " неверное имя пакета: '" + item + "'")
    return name, deps


def load_test_repo(path):
    """Читает файл тестового репозитория в словарь: пакет -> зависимости."""
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError:
        raise TestRepoError("не удалось открыть файл " + path)
    graph = {}
    for number, line in enumerate(lines, start=1):
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue
        name, deps = parse_test_line(line, number)
        graph[name] = deps
    return graph


def visit(graph, name, seen, order):
    """Добавляет в order сначала зависимости пакета name, потом его самого."""
    if name in seen:
        return
    seen.add(name)
    for dep in graph.get(name, []):
        visit(graph, dep, seen, order)
    order.append(name)


def load_order(graph, start):
    """Возвращает порядок загрузки: зависимости раньше зависящих пакетов."""
    order = []
    visit(graph, start, set(), order)
    return order