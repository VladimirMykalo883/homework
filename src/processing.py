from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по указанному статусу.

    Args:
        transactions: Список словарей с транзакциями
        state: Статус для фильтрации (по умолчанию 'EXECUTED')

    Returns:
        Отфильтрованный список транзакций
    """
    if not isinstance(transactions, list):
        return []

    return [t for t in transactions if isinstance(t, dict) and str(t.get("state", "")).upper() == str(state).upper()]


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате.

    Args:
        transactions: Список словарей с транзакциями
        reverse: Порядок сортировки (True - новые сначала, False - старые сначала)

    Returns:
        Отсортированный список транзакций
    """
    if not isinstance(transactions, list):
        return []

    def get_date(item: Dict[str, Any]) -> datetime:
        """Вспомогательная функция для извлечения даты."""
        date_str = item.get("date", "")
        try:
            return datetime.fromisoformat(date_str) if date_str else datetime.min
        except (ValueError, TypeError):
            return datetime.min

    return sorted([t for t in transactions if isinstance(t, dict)], key=get_date, reverse=reverse)
