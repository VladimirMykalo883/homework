import pytest
from unittest.mock import patch
import json
#from pathlib import Path
from utils import read_json_file

# Фикстура для временного файла
@pytest.fixture
def temp_json_file(tmp_path):
    def _create_file(data):
        file_path = tmp_path / "test_operations.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        return file_path
    return _create_file

# Тест на успешное чтение JSON
def test_read_valid_json(temp_json_file):
    """Проверяет чтение корректного JSON с конвертацией amount в float."""
    test_data = [
        {
            "id": 441945886,
            "operationAmount": {
                "amount": "31957.58",
                "currency": {"name": "руб.", "code": "RUB"}
            },
            "description": "Перевод организации"
        }
    ]
    file_path = temp_json_file(test_data)

    result = read_json_file(file_path)
    assert len(result) == 1
    assert result[0]["id"] == 441945886
    assert result[0]["amount"] == 31957.58  # Конвертация в float
    assert result[0]["currency_name"] == "руб."
    assert result[0]["currency_code"] == "RUB"
# Тест на обработку ошибок JSON
@patch("builtins.open", side_effect=json.JSONDecodeError("Ошибка", "test", 0))
def test_invalid_json(mock_file):
    """Проверяет обработку битого JSON."""
    result = read_json_file("invalid.json")
    assert result == []

# Тест на отсутствие файла
@patch("builtins.open", side_effect=FileNotFoundError())
def test_file_not_found(mock_file):
    """Проверяет обработку отсутствующего файла."""
    result = read_json_file("nonexistent.json")
    assert result == []


# Параметризованный тест для amount
@pytest.mark.parametrize("amount_input, expected", [
    ("100", 100.0),
    ("1 000.50", 1000.5),
    ("3 195", 3195.0),
    (None, None),
    ("invalid", None)
])
def test_amount_conversion(temp_json_file, amount_input, expected):
    """Проверяет конвертацию amount в float для разных форматов."""
    test_data = [{"operationAmount": {"amount": amount_input, "currency": {"name": "USD"}}}]
    file_path = temp_json_file(test_data)

    result = read_json_file(file_path)
    assert result[0]["amount"] == expected
