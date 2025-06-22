from __future__ import annotations

from typing import Any, Dict, Iterable, Iterator, TypeVar

T = TypeVar("T")


def filter_by_currency(transactions: Iterable[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """Фильтрация транзакций по валюте с проверкой структуры."""
    if not isinstance(currency, str) or len(currency) != 3:
        raise ValueError("Currency code must be 3 characters long")

    for transaction in transactions:
        try:
            if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
                yield transaction
        except AttributeError:
            continue


def transaction_descriptions(transactions: Iterable[Dict[str, Any]]) -> Iterator[str]:
    """Генерация описаний транзакций с проверкой структуры."""
    for transaction in transactions:
        try:
            yield str(transaction["description"])
        except (KeyError, TypeError):
            yield "No description"


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """Генератор номеров карт с валидацией диапазона."""
    if start < 0 or end < 0:
        raise ValueError("Start and end must be positive")
    if start > end:
        raise ValueError("Start must be less than or equal to end")
    if end > 9999999999999999:
        raise ValueError("Card number cannot exceed 16 digits")

    for num in range(start, end + 1):
        num_str = f"{num:016d}"
        yield f"{num_str[:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:16]}"
