import logging
from pathlib import Path
from utils import read_json_file
from file_readers import read_transactions_from_csv, read_transactions_from_excel


def setup_logging() -> None:
    """Настройка раздельных логгеров для каждого модуля"""
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)

    # Очищаем существующие обработчики (на случай повторного вызова)
    logging.root.handlers.clear()

    # Общий формат для всех логгеров
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Настройка логгера для utils
    utils_logger = logging.getLogger("utils")
    utils_logger.setLevel(logging.DEBUG)
    utils_handler = logging.FileHandler(log_dir / "utils.log", encoding="utf-8", mode="w")  # Явно указываем кодировку
    utils_handler.setFormatter(formatter)
    utils_logger.addHandler(utils_handler)
    utils_logger.setLevel(logging.INFO)

    # Настройка логгера для masks
    masks_logger = logging.getLogger("masks")
    masks_logger.setLevel(logging.DEBUG)
    masks_handler = logging.FileHandler(log_dir / "masks.log", encoding="utf-8", mode="w")  # Явно указываем кодировку
    masks_handler.setFormatter(formatter)
    masks_logger.addHandler(masks_handler)
    masks_logger.setLevel(logging.INFO)

    # Настройка логгера для file_readers
    file_readers_logger = logging.getLogger("file_readers")
    file_readers_logger.setLevel(logging.DEBUG)
    file_readers_handler = logging.FileHandler(log_dir / "file_readers.log", encoding="utf-8", mode="w")
    file_readers_handler.setFormatter(formatter)
    file_readers_logger.addHandler(file_readers_handler)
    file_readers_logger.setLevel(logging.INFO)

    # Дополнительный вывод в консоль с уровнем INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)

if __name__ == "__main__":
    # Настройка логирования должна быть ПЕРВОЙ операцией
    setup_logging()

    # Теперь импортируем модули после настройки логирования
    from src.masks import get_mask_account, get_mask_card_number
    from src.utils import read_json_file

    # Тестовые вызовы
#    read_json_file("data/operations.json")
    get_mask_card_number("1234567812345678")
    get_mask_account("12345678901234567890")

    # Тесты вызовов ошибок
    read_json_file("data/operations1.json")
    get_mask_account("1234567890123456789")

    # Тестовые вызовы с русским текстом
    transactions = read_json_file("data/operations.json")
    print(get_mask_card_number("Visa Platinum 7000792289606361"))
    print(get_mask_account("Счет 73654108430135874305"))
    print("печать из json")
    print(f"Прочитано {len(transactions)} транзакций из json")
    print(transactions[0:5])

    csv_transactions = read_transactions_from_csv("data/transactions.csv")
    print(f"Прочитано {len(csv_transactions)} транзакций из CSV")
    print("Печать из CSV")
    print(csv_transactions[0:5])

    # Чтение из Excel
    excel_transactions = read_transactions_from_excel("data/transactions_excel.xlsx")
    print(f"Прочитано {len(excel_transactions)} транзакций из Excel")
    print("Печать из Exel")
    print(excel_transactions[0:5])
