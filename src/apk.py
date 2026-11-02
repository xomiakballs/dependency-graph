"""Получение данных о пакетах из репозитория Alpine Linux (apk)."""

import io
import tarfile
import urllib.error
import urllib.request

TIMEOUT_SECONDS = 30
INDEX_NAME = "APKINDEX"

VERSION_SIGNS = "<>=~"
CONFLICT_SIGN = "!"


def download_index(url):
    """Скачивает APKINDEX.tar.gz и возвращает текст файла APKINDEX."""
    with urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS) as response:
        data = response.read()
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        index_file = archive.extractfile(INDEX_NAME)
        return index_file.read().decode("utf-8")

def parse_index(text):
    """Разбирает текст APKINDEX в словарь: имя пакета -> его поля."""
    packages = {}
    for block in text.split("\n\n"):
        fields = {}
        for line in block.splitlines():
            key, sep, value = line.partition(":")
            if sep:
                fields[key] = value
        if "P" in fields:
            packages[fields["P"]] = fields
    return packages


def strip_version(name):
    """Отрезает от имени условие на версию: zlib>=1.2 -> zlib."""
    for i, char in enumerate(name):
        if char in VERSION_SIGNS:
            return name[:i]
    return name


def build_providers(packages):
    """Строит словарь: что предоставляется -> имя пакета."""
    providers = {}
    for name, fields in packages.items():
        for item in fields.get("p", "").split():
            providers[strip_version(item)] = name
    for name in packages:
        providers[name] = name
    return providers


def direct_dependencies(packages, providers, name):
    """Возвращает список прямых зависимостей пакета (имена пакетов)."""
    result = []
    for item in packages[name].get("D", "").split():
        if item.startswith(CONFLICT_SIGN):
            continue
        dep = providers.get(strip_version(item))
        if dep and dep != name and dep not in result:
            result.append(dep)
    return result


class RepositoryError(Exception):
    """Ошибка получения данных из репозитория пакетов."""


def load_index(url):
    """Скачивает и разбирает индекс. При ошибке выбрасывает RepositoryError."""
    try:
        return parse_index(download_index(url))
    except (tarfile.TarError, KeyError):
        raise RepositoryError("по адресу " + url + " лежит не APKINDEX.tar.gz")
    except (OSError, ValueError) as error:
        raise RepositoryError("не удалось скачать " + url + ": " + str(error))