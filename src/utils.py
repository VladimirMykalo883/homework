import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Union  # Добавили недостающие импорты

logger = logging.getLogger("utils")


def read_json_file(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список транзакций в формате:
    {
        "id": int,
        "state": str,
        "date": str,
        "amount": float,
        "currency_name": str,
        "currency_code": str,
        "from": Optional[str],  # Может отсутствовать
        "to": str,
        "description": str
    }
    """
    try:
        logger.info(f"Чтение файла: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            if not isinstance(data, list):
                logger.warning("Файл не содержит список транзакций!")
                return []

            transactions = []
            for item in data:
                if not isinstance(item, dict):
                    continue  # Пропускаем некорректные записи

                # Обработка operationAmount
                operation_amount = item.get("operationAmount", {})
                if not isinstance(operation_amount, dict):
                    logger.warning("Пропуск транзакции: некорректный operationAmount")
                    continue

                # Конвертация amount в float
                amount_raw = operation_amount.get("amount")
                amount = None
                if amount_raw is not None and str(amount_raw).strip():
                    try:
                        # Заменяем запятые на точки и удаляем пробелы
                        amount_str = str(amount_raw).replace(",", "").replace(" ", "")
                        amount = float(amount_str)
                    except (ValueError, TypeError):
                        logger.warning(f"Не удалось конвертировать amount: {amount_raw}")

                currency = operation_amount.get("currency", {})

                transaction = {
                    "id": item.get("id"),
                    "state": item.get("state"),
                    "date": item.get("date"),
                    "amount": amount,  # Теперь это float или None,
                    "currency_name": currency.get("name"),
                    "currency_code": currency.get("code"),
                    "from": item.get("from"),  # Может быть None
                    "to": item.get("to"),
                    "description": item.get("description")
                }
                transactions.append(transaction)

            logger.info(f"Successfully read {len(transactions)} items from {file_path}")
            return transactions

    except Exception as e:

        logger.error(f"Ошибка: {str(e)}", exc_info=True)
        return []
