from dataclasses import asdict
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
        ) -> list[dict]:
        try:
            id = query['id'][0]
        except KeyError:
            logging.error("Ошибка ввода. Код валюты отсутвует")
            return Responses.input_err(message="Код валюты отустсвует в адресе")
        result = self.service.get_currency(id=id)
        if result.is_err():
            if isinstance(result.unwrap_err(), ObjectNotFoundError):
                return Responses.not_found_err(result.unwrap_err().message)
            elif isinstance(result.unwrap_err(), InitialError):
                return Responses.initial_err(result.unwrap_err().message)
        return Responses.success(data=asdict(result.unwrap()))