from __future__ import annotations

import logging
import re
from typing import Optional

logger = logging.getLogger("masks")


def get_mask_card_number(card_number: Optional[str]) -> str:
    """
    Маскирует номер банковской карты в формате XXXX XX** **** XXXX.

    Args:
        card_number: Номер карты в любом формате (может содержать пробелы, дефисы)

    Returns:
        Маскированная строка или оригинал, если номер слишком короткий или некорректный
    """
    try:
        if not isinstance(card_number, str) or not card_number.strip():
            logger.debug("Получена пустая строка или None для номера карты")
            return ""
            # Логируем исходные данные ДО обработки
        logger.debug(f"Получены данные карты: {card_number!r}")  # !r для экранирования спецсимволов

        digits = re.sub(r"\D", "", card_number)
        if len(digits) != 16 or not digits.isdigit():
            logger.warning(f"Invalid card number format: {card_number}")
            return "**"

        logger.debug(f"Успешная маскировка карты: {card_number} ")
        return f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"

    except Exception as e:
        logger.error(f"Error masking card number: {str(e)}", exc_info=True)
        return card_number if card_number else ""


def get_mask_account(account_number: Optional[str]) -> str:
    """
    Маскирует номер банковского счета в формате **XXXX.

    Args:
        account_number: Номер счета в любом формате

    Returns:
        Маскированная строка (последние 4 цифры) или ** для некорректных данных
    """
    try:
        if account_number is None:
            logger.debug("None account number received")
            return ""

        cleaned = account_number.strip()
        if not cleaned:
            logger.debug("Empty account number received")
            return "**"

        digits = re.sub(r"\D", "", cleaned)

        # Проверка длины номера счета (должно быть 20 цифр)
        if len(digits) != 20 or not digits.isdigit():
            logger.warning(f"Invalid account number format (expected 20 digits): {account_number}")
            return "**"

        logger.debug(f"Account masked: {account_number} ")
        return f"**{digits[-4:]}" if digits else f"**{cleaned}"
    except Exception as e:
        logger.error(f"Error masking account: {str(e)}", exc_info=True)
        return account_number if account_number else "**"
