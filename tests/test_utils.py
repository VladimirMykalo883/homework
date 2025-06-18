from unittest.mock import mock_open, patch

import pytest

from src.utils import read_json_file


def test_read_json_file_valid():
    json_data = '[{"id": 1, "amount": 100}]'
    with patch("builtins.open", mock_open(read_data=json_data)):
        result = read_json_file("dummy_path.json")
        assert result == [{"id": 1, "amount": 100}]


def test_read_json_file_invalid():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = read_json_file("nonexistent.json")
        assert result == []
