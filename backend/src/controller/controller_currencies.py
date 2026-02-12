
import logging

from src.errors import InitialError, ObjectAlreadyExists, ObjectNotFoundError
from src.response import Responses
from src.controller.controller_base import BaseController
from src.service.service_currencies import CurrenciesService
from src.dto.dto_currencies import CurrenciesDTO

# Валидируем и передаем сервису, а затем возвращаем ответ
class CurrenciesController(BaseController):
    def __init__(
            self,
            service: CurrenciesService,
        ):
        self.service = service

    def do_GET(
            self, path
        ):
        result = self.service.get_currencies()

        if result.is_err():
            if isinstance(result.unwrap_err(), ObjectNotFoundError):
                logging.error("Ошибка. База данных currencies пуста")
                return Responses.not_found_err(result.unwrap_err().message)
            
            elif isinstance(result.unwrap_err(), InitialError):
                logging.error(f"Ошибка базы данных или сервера")
                return Responses.initial_err(result.unwrap_err().message)
        data = [currency.to_formatted_dict() for currency in result.unwrap()]
        return Responses.success(data=data)


    def do_POST(
            self, 
            path,
            data: dict,
            ):
        try:
            code=data["code"][0]
            fullname=data["name"][0]
            sign=data["sign"][0]
            
            available_letters_code = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            available_letters_name = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz "
            if len(sign) != 1:
                logging.error("Ошибка ввода. Неправильный вид валюты")
                return Responses.input_err(
                    message="Ошибка ввода. Знак валюты должен состоять из одного символа")
            if len(code) != 3:
                logging.error("Ошибка ввода. Неправильный вид валюты")
                return Responses.input_err(
                    message="Ошибка ввода. Длина кода валюты должна составлять 3 символа")

            for letter in code:
                if letter not in available_letters_code:
                    logging.error("Ошибка ввода. Присутствуют неожиданные символы")
                    return Responses.input_err(
                        message="Ошибка ввода. Код может состоять только из английский заглавных букв")
            for letter in fullname:
                if letter not in available_letters_name:
                    logging.error("Ошибка ввода. Присутствуют неожиданные символы")
                    return Responses.input_err(
                        message="Ошибка ввода. Имя валюты может содержать только английские буквы")

            dto = CurrenciesDTO(
                code=code,
                fullname=fullname,
                sign=sign
            )
        except KeyError:
            logging.error("Ошибка ввода. Отсутствует нужное поле формы")
            return Responses.input_err(
                message="Отсутствует нужное поле формы")
        
        result = self.service.post_currencies(dto)
        if result.is_err():
            if isinstance(result.unwrap_err(), ObjectAlreadyExists):
                logging.error(f"Ошибка. Объект {data["name"]} уже существует")
                return Responses.already_exists(result.unwrap_err().message)
            
            elif isinstance(result.unwrap_err(), InitialError):
                logging.error(f"Ошибка базы данных или сервера")
                return Responses.initial_err(result.unwrap_err().message)
            
        return Responses.success(data=result.unwrap().to_formatted_dict())
