import logging
from src.errors import InitialError, ObjectNotFoundError
from src.response import Responses
from src.service.service_currencies import CurrenciesService
from src.controller.controller_base import BaseController


class CurrencyController(BaseController):
    def __init__(
            self,
            service: CurrenciesService,
        ):
        self.service = service


    def do_GET(
            self, path, query
        ) -> dict:
        code = path[2]
        if path[2] == '':
            logging.error("Ошибка ввода. Код валюты отсутвует")
            return Responses.input_err(message="Код валюты отустсвует в адресе")
        
        result = self.service.get_currency(code=code)
        return Responses.success(data=result.to_formatted_dict())