import logging


from src.dto.dto_rates import RatesDTO
from src.errors import InitialError, ObjectNotFoundError
from src.response import Responses
from src.service.service_rates import RatesService
from src.controller.controller_base import BaseController


class RateController(BaseController):
    def __init__(
            self,
            service: RatesService,
        ):
        self.service = service

    def do_GET(
            self, path, query
        ):
        dto = RatesDTO(
            basecurrencycode="".join(path[2][:3]),
            targetcurrencycode="".join(path[2][3:]),
        )
        if path[2] == '':
            logging.error("Ошибка ввода. Код валюты отсутвует")
            return Responses.input_err(message="Код валюты отустсвует в адресе")

        result = self.service.get_rate(dto=dto)
        return Responses.success(data=result.to_formatted_dict())
        
    
    def do_PATCH(
            self, 
            path,
            data: dict,
            ):
        basecurrencycode = "".join(path[2][:3])
        targetcurrencycode = "".join(path[2][3:])
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
        current_dto = self.service.get_rate(dto)
        current_dto.rate = dto.rate 
        self.service.update_rate(current_dto)
                
        return Responses.success(data=current_dto.to_formatted_dict())
          