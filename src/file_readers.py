import csv
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Union

import pandas as pd  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)


def read_transactions_from_csv(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Read financial transactions from CSV file with strict type conversion.

    Args:
        file_path: Path to CSV file with transactions data

    Returns:
        List of dictionaries with transaction data where:
        - 'id' is converted to int (or None if invalid)
        - 'amount' is converted to float (or None if invalid)

    Example output:
        [{
            "id": 441945886,          # int
            "state": "EXECUTED",
            "amount": 31957.58,       # float
            ...
        }]
    """
    try:
        logger.info(f"Reading CSV file: {file_path}")
        transactions: List[Dict[str, Any]] = []

        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")

            for row in reader:
                processed: Dict[str, Any] = {}

                #               # Convert id to int
                if "id" in row:
                    try:
                        processed["id"] = int(float(row["id"]))
                    except (ValueError, TypeError):
                        processed["id"] = None

                #               #Convert amount to Optional[float]
                if "amount" in row:
                    try:
                        amount_str = row["amount"].replace(",", ".").strip()
                        processed["amount"] = float(amount_str) if amount_str else None
                    except (ValueError, TypeError):
                        processed["amount"] = None

                #               # Preserve other fields as-is
                for key, value in row.items():
                    if key not in ["id", "amount"]:
                        processed[key] = value if value != "" else None

                transactions.append(processed)

            logger.info(f"Successfully read {len(transactions)} transactions")
            return transactions

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return []
    except csv.Error as e:
        logger.error(f"CSV parsing error: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return []


def read_transactions_from_excel(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Read financial transactions from Excel file with strict type conversion.

    Args:
        file_path: Path to Excel file (.xlsx)

    Returns:
        List of dictionaries with:
        - 'id' as int (or None)
        - 'amount' as float (or None)
    """
    try:
        logger.info(f"Reading Excel file: {file_path}")

        # Явное преобразование Path в str
        file_path_str = str(file_path)

        #       # Явное указание типов для converters
        converters: Dict[str, Callable[[Any], Union[int, float, None]]] = {
            "id": lambda x: (int(float(x)) if str(x).strip().replace(".", "", 1).isdigit() else None),
            "amount": lambda x: (
                float(str(x).replace(",", "."))
                if str(x).strip().replace(",", ".").replace(".", "", 1).isdigit()
                else None
            ),
        }
        df = pd.read_excel(  # type: ignore[call-overload]
            file_path_str,
            converters=converters,
            engine="openpyxl",
            dtype_backend="numpy_nullable",  # Добавьте этот параметр
        )

        # Ensure proper null handling
        transactions: List[Dict[str, Any]] = []
        for _, row in df.iterrows():
            processed = {
                "id": int(row["id"]) if pd.notna(row.get("id")) else None,
                "amount": float(row["amount"]) if pd.notna(row.get("amount")) else None,
                **{k: v if pd.notna(v) else None for k, v in row.items() if k not in ["id", "amount"]},
            }
            transactions.append(processed)

        logger.info(f"Successfully read {len(transactions)} transactions")
        return transactions

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return []
    except pd.errors.EmptyDataError:
        logger.error("File is empty")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return []
