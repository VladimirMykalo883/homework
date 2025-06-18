from __future__ import annotations

import os
from decimal import Decimal
from typing import Any, Dict, Optional, Union

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY: Optional[str] = os.getenv("EXCHANGE_RATE_API_KEY")
BASE_URL: str = "https://api.apilayer.com/exchangerates_data/latest"


def convert_to_rub(transaction: Dict[str, Any]) -> Optional[float]:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction: Словарь с данными о транзакции

    Returns:
        Сумма в рублях (float) или None в случае ошибки
    """
    if API_KEY is None:
        raise ValueError("API_KEY is not set in environment variables")

    try:
        operation_amount: Dict[str, Any] = transaction["operationAmount"]
        amount: Union[str, float, Decimal] = operation_amount["amount"]
        currency_info: Dict[str, str] = operation_amount["currency"]
        currency: str = currency_info["code"]

        if currency == "RUB":
            return float(amount)

        response = requests.get(
            BASE_URL,
            params={"base": currency, "symbols": "RUB"},
            headers={"apikey": API_KEY},
            timeout=10,
        )
        response.raise_for_status()

        rates: Dict[str, float] = response.json()["rates"]
        rate: float = rates["RUB"]
        return float(amount) * rate

    except (KeyError, ValueError, requests.RequestException) as e:
        print(f"Error converting currency: {e}")
        return None
