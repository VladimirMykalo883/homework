from __future__ import annotations

import re
from typing import Optional


def get_mask_card_number(card_number: Optional[str]) -> str:
    """
    Маскирует номер банковской карты в формате XXXX XX** **** XXXX.

    Args:
        card_number: Номер карты в любом формате (может содержать пробелы, дефисы)

    Returns:
        Маскированная строка или оригинал, если номер слишком короткий или некорректный
    """
    if not isinstance(card_number, str) or not card_number.strip():
        return ""

    digits = re.sub(r"\D", "", card_number)
    if len(digits) < 8 or not digits.isdigit():
        return card_number

    return f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"


def get_mask_account(account_number: Optional[str]) -> str:
    """
    Маскирует номер банковского счета в формате **XXXX.

    Args:
        account_number: Номер счета в любом формате

    Returns:
        Маскированная строка (последние 4 цифры) или ** для некорректных данных
    """
    if account_number is None:
        return ""

    if not isinstance(account_number, str):
        return "**"

    cleaned = account_number.strip()
    if not cleaned:
        return "**"

    digits = re.sub(r"\D", "", cleaned)
    return f"**{digits[-4:]}" if digits else f"**{cleaned}"
