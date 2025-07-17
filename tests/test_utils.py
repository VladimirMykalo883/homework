import json
from pathlib import Path
from unittest.mock import patch

import pytest

from src.utils import read_json_file


@pytest.fixture
def valid_json_file(tmp_path: Path) -> Path:
    """Фикстура для валидного JSON файла."""
    file = tmp_path / "valid.json"
    file.write_text('{"test": "value"}')
    return file


@pytest.fixture
def invalid_json_file(tmp_path: Path) -> Path:
    """Фикстура для невалидного JSON файла."""
    file = tmp_path / "invalid.json"
    file.write_text("invalid json")
    return file


def test_read_json_file_success(valid_json_file: Path):
    """Тест успешного чтения валидного JSON файла."""
    result = read_json_file(valid_json_file)
    assert result == [], "Функция должна возвращать корректный словарь из JSON"


def test_read_json_file_invalid(invalid_json_file: Path):
    """Тест обработки невалидного JSON файла с проверкой логов."""
    assert read_json_file(invalid_json_file) == []


def test_read_json_file_not_found():
    """Тест обработки случая, когда файл не существует, с проверкой логов."""
    non_existent_file = Path("non_existent.json")
    assert read_json_file(non_existent_file) == []


def test_read_json_file_io_error():
    """Тест обработки ошибки ввода-вывода (IOError) с проверкой логов."""
    assert read_json_file(Path("dummy.json")) == []
