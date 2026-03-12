import sqlite3
from typing import Callable, Any
import logging

from result import Err

from src.errors import InitialError

def exception_handler(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        
        except sqlite3.Error:
            logging.exception("Ошибка базы данных")
            return Err(InitialError())

        except Exception as e:
            logging.debug(f"Ошибка: {e}")
            return Err(InitialError())
    return wrapper
