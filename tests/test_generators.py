from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:  # Добавлены аннотации типов:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
    ]


def test_filter_by_currency(sample_transactions: List[Dict[str, Any]]) -> None:  # Добавлены аннотации типов
    usd_transactions = filter_by_currency(sample_transactions, "USD")
    assert next(usd_transactions)["id"] == 939719570
    assert next(usd_transactions)["id"] == 142264268

    with pytest.raises(StopIteration):
        next(usd_transactions)


@pytest.mark.parametrize("currency, expected_count", [("USD", 2), ("RUB", 1), ("EUR", 0)])
def test_filter_by_currency_parametrized(
    sample_transactions: List[Dict[str, Any]], currency: str, expected_count: int
) -> None:  # Добавлены аннотации типов
    filtered = list(filter_by_currency(sample_transactions, currency))
    assert len(filtered) == expected_count


def test_transaction_descriptions(sample_transactions: List[Dict[str, Any]]) -> None:  # Добавлены аннотации типов
    descriptions = transaction_descriptions(sample_transactions)
    assert next(descriptions) == "Перевод организации"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод со счета на счет"


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (9999999999999997, 9999999999999999, ["9999 9999 9999 9997", "9999 9999 9999 9998", "9999 9999 9999 9999"]),
        (5, 5, ["0000 0000 0000 0005"]),
    ],
)
def test_card_number_generator(start: int, end: int, expected: List[str]) -> None:  # Добавлены аннотации типов
    generator = card_number_generator(start, end)
    assert list(generator) == expected
