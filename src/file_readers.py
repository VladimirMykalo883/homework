import csv
import logging
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd

# Настройка логгера для модуля
logger = logging.getLogger("file_readers")

def read_transactions_from_csv(file_path: str | Path) -> List[Dict[str, Any]]:
    """
    Читает финансовые операции из CSV файла и возвращает список транзакций.

    Args:
        file_path: Путь к CSV файлу

    Returns:
        Список словарей с транзакциями. Если файл не найден или некорректен,
        возвращается пустой список.
    """

    logger.info(f"Начало чтения CSV файла: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            transactions = list(reader)
            logger.info(f"Успешно прочитано {len(transactions)} транзакций из CSV файла")
            return transactions
    except FileNotFoundError:
        logger.error(f"CSV файл не найден: {file_path}")
        return []

    except csv.Error as e:
        logger.error(f"Ошибка чтения CSV файла {file_path}: {str(e)}", exc_info=True)
        return []

    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении CSV файла {file_path}: {str(e)}", exc_info=True)
        return []


def read_transactions_from_excel(file_path: str | Path) -> List[Dict[str, Any]]:
    """
    Читает финансовые операции из Excel файла и возвращает список транзакций.

    Args:
        file_path: Путь к Excel файлу

    Returns:
        Список словарей с транзакциями. Если файл не найден или некорректен,
        возвращается пустой список.
    """

    logger.info(f"Начало чтения Excel файла: {file_path}")

    try:
        print(file_path)
        df = pd.read_excel(file_path)
        transactions = df.to_dict('records')
        logger.info(f"Успешно прочитано {len(transactions)} транзакций из Excel файла")
        return transactions

    except FileNotFoundError:
        logger.error(f"Excel файл не найден: {file_path}")
        return []

    except pd.errors.EmptyDataError:
        logger.error(f"Excel файл пуст: {file_path}")
        return []

    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении Excel файла {file_path}: {str(e)}", exc_info=True)
        return []