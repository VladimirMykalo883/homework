import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict, List, TypedDict, Union  # Добавили недостающие импорты
import  os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(project_root, 'logs')
os.makedirs(log_dir, exist_ok=True)

file_path = os.path.join(project_root, 'data', 'operations.json')
print(file_path)
print(log_dir, )

# Настройка логгера
logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)

# Очистка старых обработчиков
for h in logger.handlers[:]:
    logger.removeHandler(h)
    h.close()

# Обработчик с ротацией (5 МБ макс, 3 резервные копии)
handler = RotatingFileHandler(
    os.path.join(log_dir, 'utils.log'),
    maxBytes=5*1024*1024,
    backupCount=3,
    encoding='utf-8',
    delay=False  # Отключение буферизации
)

# Формат логов
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Тест
logger.info("=== Тест записи в лог ===")
for handler in logger.handlers:
    handler.flush()  # Принудительная запись

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
     #   >>> read_json_file("data/operations.json")
        [{'id': 441945886, 'state': 'EXECUTED', ...}]

     #   >>> read_json_file("invalid.json")
        []
    """
    result: List[Transaction] = []  # Явное объявление
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.info("Функция выполнена успешно")
            return data if isinstance(data, list) else []
    except Exception(FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
        logger.error(f"Неожиданная ошибка при чтении {file_path} - {str(e)}", exc_info=True)
        return []

if __name__ == "__main__":
    logger.info("Тестовое сообщение для проверки логирования")
    print(f"Лог должен быть записан в: {os.path.join(log_dir, 'utils.log')}")
