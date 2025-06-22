import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Visa Gold 1234567890123456", "Visa Gold 1234 56** **** 3456"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Maestro 1234567812345678", "Maestro 1234 56** **** 5678"),
        ("МИР 1234567890123456", "МИР 1234 56** **** 3456"),
        ("Счет 123", "Счет **123"),
        ("Карта 123", "Карта 123"),
        ("", ""),
        ("   ", ""),
    ],
)
def test_mask_account_card(input_str: str , expected: str)-> None:
    assert mask_account_card(input_str) == expected


@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2023-01-15T12:30:00", "15.01.2023"),
        ("2022-12-31T23:59:59", "31.12.2022"),
        ("2021-02-28", "28.02.2021"),
        ("", ""),
        ("   ", ""),
        ("2023-01", "2023-01"),
        ("invalid-date", "invalid-date"),
    ],
)
def test_get_date(date_str: str, expected: str) -> None :
    assert get_date(date_str) == expected
