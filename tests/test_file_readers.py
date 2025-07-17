import csv
import logging
from typing import Any
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest
from pandas import DataFrame

from src.file_readers import read_transactions_from_csv, read_transactions_from_excel


@pytest.fixture(autouse=True)
def setup_logging() -> None:
    logging.basicConfig(level=logging.DEBUG)


# Тесты для CSV
@patch("builtins.open", new_callable=mock_open)
@patch("csv.DictReader")
def test_read_csv_success(mock_dict_reader: MagicMock, mock_open_func: MagicMock) -> None:
    """Тест успешного чтения CSV с конвертацией типов."""
    test_data = [
        {"id": "123", "amount": "100.50", "state": "EXECUTED"},
        {"id": "456.0", "amount": "2,000", "state": "PENDING"},
    ]
    mock_dict_reader.return_value = test_data

    result = read_transactions_from_csv("test.csv")

    assert len(result) == 2
    assert result[0]["id"] == 123
    assert isinstance(result[0]["id"], int)
    assert result[1]["amount"] == 2.0
    assert isinstance(result[1]["amount"], float)
    mock_open_func.assert_called_once_with("test.csv", "r", encoding="utf-8")


@patch("builtins.open", side_effect=FileNotFoundError)
def test_csv_file_not_found(mock_open_func: MagicMock) -> None:
    """Тест обработки отсутствующего CSV-файла."""
    result = read_transactions_from_csv("missing.csv")
    assert result == []
    mock_open_func.assert_called_once_with("missing.csv", "r", encoding="utf-8")


@patch("builtins.open", new_callable=mock_open, read_data="invalid,data")
@patch("csv.DictReader", side_effect=csv.Error)
def test_csv_invalid_format(mock_dict_reader: MagicMock, mock_open_func: MagicMock) -> None:
    """Тест обработки битого CSV."""
    result = read_transactions_from_csv("corrupted.csv")
    assert result == []
    mock_open_func.assert_called_once_with("corrupted.csv", "r", encoding="utf-8")


# Тесты для Excel
@patch("pandas.read_excel")
def test_read_excel_success(mock_read_excel: MagicMock) -> None:
    """Тест успешного чтения Excel с конвертацией типов."""
    mock_df = DataFrame([{"id": 1, "amount": 100.50}, {"id": 2.0, "amount": "200"}])
    mock_read_excel.return_value = mock_df

    result = read_transactions_from_excel("test.xlsx")

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert isinstance(result[0]["id"], int)
    mock_read_excel.assert_called_once()


@patch("pandas.read_excel", side_effect=FileNotFoundError)
def test_excel_file_not_found(mock_read_excel: MagicMock) -> None:
    """Тест обработки отсутствующего Excel-файла."""
    result = read_transactions_from_excel("missing.xlsx")
    assert result == []
    mock_read_excel.assert_called_once()


@patch("pandas.read_excel", side_effect=pd.errors.EmptyDataError)
def test_empty_excel(mock_read_excel: MagicMock) -> None:
    """Тест обработки пустого Excel-файла."""
    result = read_transactions_from_excel("empty.xlsx")
    assert result == []
    mock_read_excel.assert_called_once()


@patch("pandas.read_excel")
def test_excel_invalid_data(mock_read_excel: MagicMock) -> None:
    """Тест обработки некорректных данных в Excel."""
    mock_df = DataFrame([{"id": "invalid", "amount": "text"}])
    mock_read_excel.return_value = mock_df

    result = read_transactions_from_excel("invalid.xlsx")
    assert len(result) == 0  # Ожидаем пустой список для некорректных данных
    mock_read_excel.assert_called_once()


@patch("pandas.read_excel", side_effect=Exception("Test error"))
@patch("logging.Logger.error")
def test_excel_error_logging(mock_logger: MagicMock, mock_read_excel: MagicMock) -> None:
    """Тест логирования ошибок при чтении Excel."""
    result = read_transactions_from_excel("error.xlsx")
    assert result == []
    mock_logger.assert_called_once()
