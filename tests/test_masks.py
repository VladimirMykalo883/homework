import pytest

from masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567812345678", "1234 56** **** 5678"),
        ("1111 2222 3333 4444", "1111 22** **** 4444"),
        ("1234-5678-1234-5678", "1234 56** **** 5678"),
        ("123", "123"),
        ("", ""),
        (None, ""),
        ("abcd", "abcd"),
        ("12345678", "1234 56** **** 5678"),
    ],
)
def test_get_mask_card_number(card_number, expected):
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "account, expected",
    [
        ("12345678901234567890", "**7890"),
        ("9876 5432 1098 7654", "**7654"),
        ("1234", "**1234"),
        ("12", "**12"),
        ("", "**"),
        (None, ""),
        ("abc", "**abc"),
    ],
)
def test_get_mask_account(account, expected):
    assert get_mask_account(account) == expected
