import functools
import sqlite3
from typing import Callable, Any, ParamSpec, TypeVar
import logging

from result import Err, Result

from src.response import Responses
from src.errors import InitialError, ObjectNotFoundError

P = ParamSpec('P')
T = TypeVar('T')

def exception_handler(func: Callable[P, T]) -> Callable[P, T]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return func(*args, **kwargs) # type: ignore
        
        except sqlite3.Error:
            logging.exception("Ошибка базы данных")
            raise InitialError()

        except Exception as e:
            logging.debug(f"Ошибка: {e}")
            raise InitialError()
    return wrapper

def handle_errors_controller(func: Callable[P, T]) -> Callable[P, Any]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except (IndexError, KeyError) as e:
            logging.error(f"Ошибка ввода. Код валюты отсутствует: {e}")
            return Responses.input_err(message="Код валюты отсутствует в адресе")
        
        except ValueError as e:
            logging.error(f"Ошибка ввода: {e}")
            return Responses.input_err(message=str(e))
        
        except ObjectNotFoundError as e:
            logging.error(f"Объект не найден: {e}")
            return Responses.not_found_err(e.message)
        
        except InitialError as e:
            logging.error(f"Инициализационная ошибка: {e}")
            return Responses.initial_err(e.message)
        
        except Exception as e:
            logging.error(f"Неожиданная ошибка: {e}")
            return Responses.initial_err(message="Внутренняя ошибка сервера")
    return wrapper

class ControllerErrorsHandlertype(type):
    @staticmethod
    def wrap_method(func: Callable) -> Callable:
        @functools.wraps(func) 
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            
            except (IndexError, KeyError) as e:
                logging.error(f"Ошибка ввода. Код валюты отсутствует: {e}")
                return Responses.input_err(message="Код валюты отсутствует в адресе")
            
            except ValueError as e:
                logging.error(f"Ошибка ввода: {e}")
                return Responses.input_err(message=str(e))

            except ObjectNotFoundError as e:
                logging.error(f"Объект не найден: {e}")
                return Responses.not_found_err(e.message)

            except InitialError as e:
                logging.error(f"Инициализационная ошибка: {e}")
                return Responses.initial_err(e.message)

            except Exception as e:
                logging.error(f"Неожиданная ошибка: {e}")
                return Responses.initial_err(message="Внутренняя ошибка сервера")
        return wrapper

    def __new__(cls, name, bases, namespace):
        for attr_name, attr_value in namespace.items():
            if callable(attr_value) and not attr_name.startswith('__'):
                namespace[attr_name] = cls.wrap_method(attr_value)
        return super().__new__(cls, name, bases, namespace)