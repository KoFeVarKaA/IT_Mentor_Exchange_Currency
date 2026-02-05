from dataclasses import asdict
import logging

from src.response import Responses
from src.errors import InitialError, ObjectAlreadyExists, ObjectNotFoundError
from src.service.service_rates import RatesService
from src.controller.controller_base import BaseController


class RatesController(BaseController):
    def __init__(
            self,
            service: RatesService,
        ):
        self.service = service


    def do_GET(
            self, path
        ):
        result = self.service.get_rates()

        if result.is_err():
            if isinstance(result.unwrap_err(), ObjectNotFoundError):
                logging.error("Ошибка. База данных rates пуста")
                return Responses.not_found_err(result.unwrap_err().message)
            
            elif isinstance(result.unwrap_err(), InitialError):
                logging.error(f"Ошибка базы данных или сервера")
                return Responses.initial_err(result.unwrap_err().message)
            
        data = [asdict(rate) for rate in result.unwrap()]
        return Responses.success(data=data)