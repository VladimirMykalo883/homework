from __future__ import annotations

import re
from collections import Counter
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
    #   if not isinstance(transactions, list):
    #        return []

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
    #    if not isinstance(transactions, list):
    #        return []

    #    return [t for t in transactions if t.get("state") == state] # И здесь

    def get_date(item: Dict[str, Any]) -> datetime:
        """Вспомогательная функция для извлечения даты."""
        date_str = item.get("date", "")
        try:
            return datetime.fromisoformat(date_str) if date_str else datetime.min
        except (ValueError, TypeError):
            return datetime.min

    return sorted([t for t in transactions if isinstance(t, dict)], key=get_date, reverse=reverse)


def search_by_description(transactions: List[Dict], search_str: str) -> List[Dict]:
    """
    Ищет транзакции, в описании которых встречается заданная строка (с учетом регистра).

    Args:
        transactions: Список словарей с транзакциями
        search_str: Строка для поиска в описании транзакции

    Returns:
        Список транзакций, содержащих search_str в описании
    """
    if not search_str:
        return transactions

    pattern = re.compile(re.escape(search_str), re.IGNORECASE)
    return [
        t for t in transactions if isinstance(t, dict) and t.get("description") and pattern.search(t["description"])
    ]


def count_operations_by_category(transactions: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по заданным категориям.

    Args:
        transactions: Список словарей с транзакциями
        categories: Список категорий для подсчета

    Returns:
        Словарь с количеством операций по каждой категории
    """
    if not transactions or not categories:
        return {}

    descriptions = [
        t.get("description", "").lower() for t in transactions if isinstance(t, dict) and t.get("description")
    ]
    category_counts = Counter(descriptions)

    return {category: category_counts.get(category.lower(), 0) for category in categories}
