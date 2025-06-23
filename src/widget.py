from __future__ import annotations

import re
from datetime import datetime
from typing import Optional

from decorators import log
from masks import get_mask_account, get_mask_card_number


@log(filename="widget_operations.log")
def mask_account_card(payment_info: Optional[str]) -> str:
    """Улучшенная маскировка платежной информации.

    Обрабатывает как кредитные карты, так и банковские счета.

    Аргументы:
        payment_info (Optional[str]): строка с информацией о платеже.

    Возвращает:
        str: замаскированная информация о платеже.
    """
    if not payment_info or not isinstance(payment_info, str):
        return ""

    cleaned_info = payment_info.strip()
    if not cleaned_info:
        return ""

    # Извлечение всех чисел из строки
    numbers = re.findall(r"\d+", cleaned_info)
    if not numbers:
        return cleaned_info  # Возвращаем оригинальную строку, если чисел нет

    number = "".join(numbers)  # Объединяем найденные числа
    bank_part = re.sub(r"\d+", "", cleaned_info).strip()
    # Часть строки без чисел

    if "счет" in cleaned_info.lower():
        masked = get_mask_account(number)  # Маскируем номер счета
    else:
        masked = get_mask_card_number(number)  # Маскируем номер карты

    # Возвращаем результат
    return f"{bank_part} {masked}" if bank_part else masked


def get_date(date_str: Optional[str]) -> str:
    """Форматирование даты с улучшенной обработкой ошибок.

    Преобразует строку даты в формат "дд.мм.гггг".

    Аргументы:
        date_str (Optional[str]): строка с датой.

    Возвращает:
        str: отформатированная дата или оригинальная строка в случае ошибки.
    """
    if not date_str or not isinstance(date_str, str):
        return ""

    cleaned_date = date_str.strip()
    if not cleaned_date:
        return ""

    try:
        # Парсинг первой части даты
        dt = datetime.strptime(cleaned_date[:10], "%Y-%m-%d")
        return dt.strftime("%d.%m.%Y")  # Форматируем дату в нужный вид
    except ValueError:
        return cleaned_date  # Возвращаем оригинальную дату в случае ошибки
