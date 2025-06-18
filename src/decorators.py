from __future__ import annotations

import datetime
from functools import wraps
from typing import Any, Callable, Optional, TypeVar

T = TypeVar("T")
LOG_FORMAT = "{timestamp} - {level} - {func_name} - {message}"


def log(
    filename: Optional[str] = None, log_errors: bool = True, log_success: bool = True
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Декоратор для логирования с настройками."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            timestamp = datetime.datetime.now().isoformat()
            func_name = func.__qualname__

            try:
                result = func(*args, **kwargs)
                if log_success:
                    message = LOG_FORMAT.format(
                        timestamp=timestamp,
                        level="INFO",
                        func_name=func_name,
                        message=f"Args: {args}, Kwargs: {kwargs}",
                    )
                    _log_message(message, filename)
                return result
            except Exception as e:
                if log_errors:
                    message = LOG_FORMAT.format(
                        timestamp=timestamp,
                        level="ERROR",
                        func_name=func_name,
                        message=f"{
                            type(e).__name__}: {
                            str(e)} Args: {args}, Kwargs: {kwargs}",
                    )
                    _log_message(message, filename)
                raise

        return wrapper

    return decorator


def _log_message(message: str, filename: Optional[str] = None) -> None:
    """Логирование сообщения с обработкой ошибок."""
    try:
        if filename:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        else:
            print(message)
    except Exception as e:
        print(f"Logging failed: {str(e)}")
