import logging
import re
from pathlib import Path
from typing import Dict, List, Optional

from file_readers import read_transactions_from_csv, read_transactions_from_excel
from masks import get_mask_card_number
from processing import count_operations_by_category, filter_by_state, search_by_description, sort_by_date
from src.widget import get_date
from utils import read_json_file


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


def print_transaction(transaction: Dict) -> None:
    """Печатает информацию о транзакции в удобном формате."""
    if not isinstance(transaction, dict):
        return

    date = transaction.get("date", "")
    description = transaction.get("description", "Нет описания")
    from_account = transaction.get("from", "")
    to_account = transaction.get("to", "")
    amount = transaction.get("amount", 0)
    currency = transaction.get("currency_name", "руб.")

    masked_from = mask_account_card(from_account) if from_account else ""
    masked_to = mask_account_card(to_account) if to_account else ""

    print(f"{get_date(date)} {description}")
    if masked_from:
        print(f"{masked_from} -> {masked_to}")
    else:
        print(f"{masked_to}")
    print(f"Сумма: {amount} {currency}\n")


def mask_account_card(payment_info: str) -> str:
    """Улучшенная маскировка платежной информации."""
    if "счет" in payment_info.lower():
        digits = re.sub(r"\D", "", payment_info)
        return f"Счет **{digits[-4:]}" if digits else payment_info
    else:
        return get_mask_card_number(payment_info)


def get_user_input(prompt: str, options: Optional[List[str]] = None) -> str:
    """Получает ввод от пользователя с проверкой."""
    while True:
        user_input = input(prompt).strip()
        if not options or user_input.lower() in [o.lower() for o in options]:
            return user_input
        print(f"Неверный ввод. Допустимые варианты: {', '.join(options)}")


def main() -> None:
    ''' Функция позволяет выбрать источник получения информации,
    фильтрует по статусу, дате, валюте и слову в описнии
    '''

    setup_logging()

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_type = get_user_input("Ваш выбор (1-3): ", ["1", "2", "3"])

    file_paths = {"1": "data/operations.json", "2": "data/transactions.csv", "3": "data/transactions_excel.xlsx"}

    file_path = file_paths[file_type]
    print(f"\nДля обработки выбран файл: {file_path}")

    # Чтение файла
    if file_type == "1":
        transactions = read_json_file(file_path)
    elif file_type == "2":
        transactions = read_transactions_from_csv(file_path)
    else:
        transactions = read_transactions_from_excel(file_path)

        # Фильтрация по статусу
    valid_states = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        state = get_user_input(
            "\nВведите статус, по которому необходимо выполнить фильтрацию.\n"
            f"Доступные для фильтровки статусы: {', '.join(valid_states)}\n"
            "Ваш выбор: ",
            valid_states,
        ).upper()

        if state in valid_states:
            break
        print(f'Статус операции "{state}" недоступен.')

    filtered = filter_by_state(transactions, state)
    print(f"\nОперации отфильтрованы по статусу '{state}'")

    # Сортировка по дате
    sort_answer = get_user_input("\nОтсортировать операции по дате? (Да/Нет): ", ["да", "нет"])
    if sort_answer.lower() == "да":
        order = get_user_input(
            "Отсортировать по возрастанию или по убыванию? (возрастанию/убыванию): ", ["возрастанию", "убыванию"]
        )
        reverse = order.lower() == "убыванию"
        filtered = sort_by_date(filtered, reverse=reverse)

    # Фильтрация по рублям
    rub_answer = get_user_input("\nВыводить только рублевые транзакции? (Да/Нет): ", ["да", "нет"])
    if rub_answer.lower() == "да":
        filtered = [t for t in filtered if t.get("currency_code", "").upper() == "RUB"]

    # Поиск по описанию
    search_answer = get_user_input(
        "\nОтфильтровать список транзакций по определенному слову в описании? (Да/Нет): ", ["да", "нет"]
    )
    if search_answer.lower() == "да":
        search_word = input("Введите слово для поиска в описании: ").strip()
        if search_word:
            filtered = search_by_description(filtered, search_word)

    # Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций в выборке: {len(filtered)}\n")

    if not filtered:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        for transaction in filtered[:5]:  # Ограничим вывод 5 транзакциями для примера
            print_transaction(transaction)

    # Дополнительная статистика
    if filtered:
        categories = list(set(t.get("description", "") for t in filtered))
        counts = count_operations_by_category(filtered, categories)
        print("\nСтатистика по категориям операций:")
        for category, count in counts.items():
            print(f"{category}: {count} операций")


if __name__ == "__main__":
    main()
