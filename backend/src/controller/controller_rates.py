
import logging

from src.dto.dto_rates import RatesDTO
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
            self, path, query,
        ):
        result = self.service.get_rates()            
        data = [rate.to_formatted_dict() for rate in result]
        return Responses.success(data=data)
    
    def do_POST(
            self, 
            path,
            data: dict,
            ):
        basecurrencycode=data["baseCurrencyCode"][0]
        targetcurrencycode=data["targetCurrencyCode"][0]
        try:
            rate = float(data["rate"][0])
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
            rate = rate
        )
        
        result = self.service.post_rate(dto)
        return Responses.success(
                data=result.to_formatted_dict(), status_code=201)
