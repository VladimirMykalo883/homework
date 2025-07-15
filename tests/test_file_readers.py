import pytest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

from pandas import DataFrame

from src.file_readers import (
    read_transactions_from_csv,
    read_transactions_from_excel
)
import pandas as pd
import logging
import csv

# Фикстура для логгера
@pytest.fixture(autouse=True)
def setup_logging():
    logging.basicConfig(level=logging.DEBUG)

# Тесты для CSV
@patch("builtins.open", new_callable=mock_open)
@patch("csv.DictReader")
def test_read_csv_success(mock_dict_reader, mock_file):
    """Тест успешного чтения CSV с конвертацией типов."""
    # Подготовка тестовых данных
    test_data = [
        {"id": "123", "amount": "100.50", "state": "EXECUTED"},
        {"id": "456.0", "amount": "2,000", "state": "PENDING"}
    ]
    mock_dict_reader.return_value = test_data

    # Вызов функции
    result = read_transactions_from_csv("test.csv")

    # Проверки
    assert len(result) == 2
    assert result[0]["id"] == 123
    assert isinstance(result[0]["id"], int)
    assert result[1]["amount"] == 2.0
    assert isinstance(result[1]["amount"], float)

@patch("builtins.open", side_effect=FileNotFoundError)
def test_csv_file_not_found(mock_file):
    """Тест обработки отсутствующего CSV-файла."""
    result = read_transactions_from_csv("missing.csv")
    assert result == []

@patch("builtins.open", new_callable=mock_open)
@patch("csv.DictReader", side_effect=csv.Error)
def test_csv_invalid_format(mock_dict_reader, mock_file):
    """Тест обработки битого CSV."""
    result = read_transactions_from_csv("corrupted.csv")
    assert result == []

# Тесты для Excel
@patch("pandas.read_excel")
def test_read_excel_success(mock_read_excel):
    """Тест успешного чтения Excel с конвертацией типов."""
    # Мокируем DataFrame
    mock_df_value = DataFrame([
        {"id": 1, "amount": 100.50},
        {"id": 2.0, "amount": "200"}
    ])
    mock_read_excel.return_value = mock_df_value

    result = read_transactions_from_excel("test.xlsx")
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert isinstance(result[0]["id"], int)

@patch("pandas.read_excel", side_effect=FileNotFoundError)
def test_excel_file_not_found(mock_read_excel):
    """Тест обработки отсутствующего Excel-файла."""
    result = read_transactions_from_excel("missing.xlsx")
    assert result == []

@patch("pandas.read_excel", side_effect=pd.errors.EmptyDataError)
def test_empty_excel(mock_read_excel):
    """Тест обработки пустого Excel-файла."""
    result = read_transactions_from_excel("empty.xlsx")
    assert result == []

@patch("pandas.read_excel")
def test_excel_invalid_data(mock_read_excel):
    """Тест обработки некорректных данных в Excel."""
    mock_df = MagicMock()
    mock_df.where.return_value.to_dict.return_value = [
        {"id": "invalid", "amount": "text"}
    ]
    mock_read_excel.return_value = mock_df

    result = read_transactions_from_excel("invalid.xlsx")
    assert len(result) == 1
    assert result[0]["id"] is None
    assert result[0]["amount"] is None

@patch("pandas.read_excel", side_effect=Exception("Test error"))
@patch("logging.Logger.error")
def test_excel_error_logging(mock_logger, mock_read_excel):
    """Тест логирования ошибок при чтении Excel."""
    result = read_transactions_from_excel("error.xlsx")
    assert result == []
    mock_logger.assert_called_once()

@patch("builtins.open", side_effect=FileNotFoundError)
def test_csv_file_not_found(mock_file):
    """Тест обработки отсутствующего CSV-файла."""
    result = read_transactions_from_csv("missing.csv")
    assert result == []
    mock_file.assert_called_once_with("missing.csv", 'r', encoding='utf-8')

@patch("builtins.open", new_callable=mock_open, read_data="invalid,data")
@patch("csv.DictReader", side_effect=csv.Error)
def test_csv_invalid_format(mock_dict_reader, mock_file):
    """Тест обработки битого CSV."""
    result = read_transactions_from_csv("corrupted.csv")
    assert result == []

@patch("pandas.read_excel")
def test_excel_invalid_data(mock_read_excel):
    """Тест обработки некорректных данных в Excel."""
    mock_df_dict = DataFrame([
        {"id": "invalid", "amount": "text"}
    ])
    mock_read_excel.return_value = mock_df_dict

    result = read_transactions_from_excel("invalid.xlsx")
    assert len(result) == 0
