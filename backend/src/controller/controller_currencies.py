
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
            self, path, query,
        ):
        result = self.service.get_currencies()
        data = [currency.to_formatted_dict() for currency in result]
        return Responses.success(data=data)


    def do_POST(
            self, 
            path,
            data: dict,
            ):
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
        result = self.service.post_currencies(dto)
        return Responses.success(
            data=result.to_formatted_dict(), status_code=201)
