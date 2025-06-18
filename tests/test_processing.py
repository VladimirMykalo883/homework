import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-15"},
        {"id": 2, "state": "CANCELED", "date": "2023-01-14"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-16"},
        {"id": 4, "state": "PENDING", "date": "2023-01-13"},
    ]


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3]),
        ("CANCELED", [2]),
        ("PENDING", [4]),
        ("UNKNOWN", []),
    ],
)
def test_filter_by_state(sample_transactions, state, expected_ids):
    result = filter_by_state(sample_transactions, state)
    assert [t["id"] for t in result] == expected_ids


@pytest.mark.parametrize(
    "reverse, expected_first_id",
    [
        (False, 4),
        (True, 3),
    ],
)
def test_sort_by_date(sample_transactions, reverse, expected_first_id):
    result = sort_by_date(sample_transactions, reverse=reverse)
    assert result[0]["id"] == expected_first_id
