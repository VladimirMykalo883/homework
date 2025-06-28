import logging
from pathlib import Path


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
    read_json_file("data/operations.json")
    get_mask_card_number("1234567812345678")
    get_mask_account("12345678901234567890")

    # Тесты вызовов ошибок
    read_json_file("data/operations1.json")
    get_mask_card_number("12345678123456789")
    get_mask_account("1234567890123456789")

    # Тестовые вызовы с русским текстом
    read_json_file("data/operations.json")
    print(get_mask_card_number("Visa Platinum 7000792289606361"))
    print(get_mask_account("Счет 73654108430135874305"))
