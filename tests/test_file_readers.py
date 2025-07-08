import pytest
from pathlib import Path
from file_readers import read_transactions_from_csv, read_transactions_from_excel


@pytest.fixture
def sample_csv_file(tmp_path):
    file_path = tmp_path / "test.csv"
    csv_content = """id,state,date,amount,currency
1,EXECUTED,2023-01-15,100.0,USD
2,CANCELED,2023-01-14,200.0,RUB"""
    file_path.write_text(csv_content)
    return file_path


@pytest.fixture
def sample_excel_file(tmp_path):
    file_path = tmp_path / "test.xlsx"
    import pandas as pd
    df = pd.DataFrame({
        'id': [1, 2],
        'state': ['EXECUTED', 'CANCELED'],
        'date': ['2023-01-15', '2023-01-14'],
        'amount': [100.0, 200.0],
        'currency': ['USD', 'RUB']
    })
    df.to_excel(file_path, index=False)
    return file_path

def test_read_transactions_from_csv(sample_csv_file):
    transactions = read_transactions_from_csv(sample_csv_file)
    assert len(transactions) == 2
    assert transactions[0]['id'] == '1'
    assert transactions[0]['state'] == 'EXECUTED'
    assert transactions[1]['amount'] == '200.0'

def test_read_transactions_from_excel(sample_excel_file):
    transactions = read_transactions_from_excel(sample_excel_file)
    assert len(transactions) == 2
    assert transactions[0]['id'] == 1
    assert transactions[0]['state'] == 'EXECUTED'
    assert transactions[1]['amount'] == 200.0


def test_read_nonexistent_file():
    assert read_transactions_from_csv("nonexistent.csv") == []
    assert read_transactions_from_excel("nonexistent.xlsx") == []