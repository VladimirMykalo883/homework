import json
from pathlib import Path
from typing import Any, Dict, List, TypedDict, Union  # Добавили недостающие импорты

import logging

logger = logging.getLogger('utils')

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
        logger.info(f"Reading file: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                logger.info(f"Successfully read {len(data)} items from {file_path}")
                return data
            else:
                logger.warning(f"File {file_path} does not contain a list, returning empty list")
                return []
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}", exc_info=True)
        return []
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in file: {file_path}", exc_info=True)
        return []
    except Exception as e:
        logger.error(f"Unexpected error reading file {file_path}: {str(e)}", exc_info=True)
        return []