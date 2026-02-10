import logging

from result import Result

from src.dto.dto_rates import RatesDTO
from src.errors import InitialError, ObjectNotFoundError
from src.response import Responses
from src.service.service_rates import RatesService
from src.controller.controller_base import BaseController


class ExchangeController(BaseController):
    def __init__(
            self,
            service: RatesService,
        ):
        self.service = service

    def do_GET(
            self, path, query
        ):
        try:
            dto = RatesDTO(
                basecurrencycode=query["from"][0],
                targetcurrencycode=query["to"][0],
                amount=query["amount"][0]
            )
        except KeyError:
            logging.error("Ошибка ввода. Отсутствует нужное поле формы")
            return Responses.input_err(
                message="Отсутствует нужное поле формы")
        
        result = self.service.get_rate(dto=dto)
        if result.is_err():
            if isinstance(result.unwrap_err(), ObjectNotFoundError):
                return Responses.not_found_err(result.unwrap_err().message)
            elif isinstance(result.unwrap_err(), InitialError):
                return Responses.initial_err(result.unwrap_err().message)
        result = result.unwrap()
        result.amount = float(dto.amount)
        result.converted_amount = result.rate * result.amount
        return Responses.success(data=result.to_formatted_dict_exchange())
    
    