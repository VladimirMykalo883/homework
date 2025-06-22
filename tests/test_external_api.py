from unittest.mock import patch

from src.external_api import convert_to_rub


@patch("requests.get")
def test_convert_to_rub_usd(mock_get):
    mock_get.return_value.json.return_value = {"rates": {"RUB": 75.5}}
    mock_get.return_value.status_code = 200

    transaction = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}

    result = convert_to_rub(transaction)
    assert result == 7550.0
