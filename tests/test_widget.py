from typing import Dict, List

import pytest

from src.processing import count_operations_by_category, search_by_description
from src.widget import get_date, mask_account_card


# Тесты для mask_account_card
@pytest.mark.parametrize(
    "input_data, expected",
    [
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("МИР 8201420097886664", "МИР 8201 42** **** 6664"),
        ("", ""),
        (None, ""),
        ("Счет **", "Счет **"),
    ],
)
def test_mask_account_card(input_data: str, expected: str) -> None:
    assert mask_account_card(input_data) == expected


# Тесты для get_date
@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("2019-08-26T10:50:58.294041", "26.08.2019"),
        ("2023-12-31", "31.12.2023"),
        ("invalid-date", "invalid-date"),
        ("", ""),
        (None, ""),
    ],
)
def test_get_date(input_date: str, expected: str) -> None:
    assert get_date(input_date) == expected


# Тесты для search_by_description
@pytest.fixture
def sample_transactions() -> List[Dict]:
    return [
        {"description": "Перевод организации", "amount": 100},
        {"description": "Открытие вклада", "amount": 200},
        {"description": "Перевод с карты на карту", "amount": 300},
        {"description": "Покупка в магазине", "amount": 400},
    ]


def test_search_by_description(sample_transactions: List[Dict]) -> None:
    # Поиск по точному совпадению
    result = search_by_description(sample_transactions, "Перевод")
    assert len(result) == 2
    assert all("Перевод" in t["description"] for t in result)

    # Поиск с учетом регистра
    result = search_by_description(sample_transactions, "перевод")
    assert len(result) == 2  # Должен находить независимо от регистра

    # Поиск несуществующего описания
    result = search_by_description(sample_transactions, "Несуществующее")
    assert len(result) == 0


# Тесты для count_operations_by_category
def test_count_operations_by_category(sample_transactions: List[Dict]) -> None:
    categories = ["Перевод организации", "Открытие вклада", "Несуществующая"]
    counts = count_operations_by_category(sample_transactions, categories)

    assert counts == {
        "Перевод организации": 1,
        "Открытие вклада": 1,
        "Несуществующая": 0,
    }

    # Пустые данные
    assert count_operations_by_category([], categories) == {}
    assert count_operations_by_category(sample_transactions, []) == {}
