import logging

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
        basecurrencycode=query["from"][0]
        targetcurrencycode=query["to"][0]
        try:
            amount = float(query["amount"][0])
        except:
            logging.error("Ошибка ввода. Неправильный тип данных")
            return Responses.input_err(
                message="Ошибка ввода. Курс обмена должен состоять из чисел")

        if len(basecurrencycode) != 3 or len(targetcurrencycode) != 3:
            logging.error("Ошибка ввода. Неправильный вид валюты")
            return Responses.input_err(
                message="Ошибка ввода. Длина кода валюты должна составлять 3 символа")                

        dto = RatesDTO(
            basecurrencycode = basecurrencycode,
            targetcurrencycode = targetcurrencycode,
            amount = amount
        )
        result = self.service.get_rate(dto=dto)
        result.amount = float(dto.amount)
        result.converted_amount = result.rate * result.amount
        return Responses.success(data=result.to_formatted_dict_exchange())
        
    