"""Визуализация графа зависимостей: текст Mermaid и картинка PNG."""

import base64
import urllib.request

MERMAID_URL = "https://mermaid.ink/img/"
TIMEOUT_SECONDS = 60


def node_ids(graph):
    """Даёт каждому пакету короткое имя для Mermaid: n0, n1, n2..."""
    ids = {}
    for name, deps in graph.items():
        for package in [name] + deps:
            if package not in ids:
                ids[package] = "n" + str(len(ids))
    return ids


def to_mermaid(graph):
    """Формирует текстовое описание графа на языке Mermaid."""
    ids = node_ids(graph)
    lines = ["graph TD"]
    for package, node in ids.items():
        lines.append("    " + node + '["' + package + '"]')
    for name, deps in graph.items():
        for dep in deps:
            lines.append("    " + ids[name] + " --> " + ids[dep])
    return "\n".join(lines) + "\n"


def save_png(mermaid_text, path):
    """Получает PNG-картинку графа через сервис mermaid.ink и сохраняет."""
    code = base64.urlsafe_b64encode(mermaid_text.encode("utf-8"))
    url = MERMAID_URL + code.decode("ascii") + "?type=png"
    request = urllib.request.Request(url, headers={"User-Agent": "dep-graph"})
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        data = response.read()
    with open(path, "wb") as file:
        file.write(data)