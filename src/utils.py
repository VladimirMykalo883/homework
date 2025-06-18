import json
from pathlib import Path
from typing import Any, Dict, List, TypedDict, Union  # Добавили недостающие импорты


class Transaction(TypedDict, total=False):
    id: int
    state: str
    date: str
    operationAmount: Dict[str, Any]
    description: str
    from_: str
    to: str


def read_json_file(file_path: Union[str, Path]) -> List[Transaction]:
    """
    Читает JSON-файл и возвращает список транзакций.

    Args:
        file_path: Путь к JSON-файлу (строка или Path объект)

    Returns:
        Список транзакций. Если файл не найден или некорректен,
        возвращается пустой список.

    Examples:
        >>> read_json_file("data/operations.json")
        [{'id': 441945886, 'state': 'EXECUTED', ...}]

        >>> read_json_file("invalid.json")
        []
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
        print(f"Error reading file {file_path}: {e}")
        return []
