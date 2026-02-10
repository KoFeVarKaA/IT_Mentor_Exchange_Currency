import logging
from dataclasses import asdict

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
        try:
            dto = RatesDTO(
                basecurrencycode="".join(path[2][:3]),
                targetcurrencycode="".join(path[2][3:]),
            )
        except (KeyError, IndexError):
            logging.error("Ошибка ввода. Отсутствует нужное поле формы")
            return Responses.input_err(
                message="Отсутствует нужное поле формы")
        if path[2] == '':
            logging.error("Ошибка ввода. Код валюты отсутвует")
            return Responses.input_err(message="Код валюты отустсвует в адресе")
        
        result = self.service.get_rate(dto=dto)
        if result.is_err():
            if isinstance(result.unwrap_err(), ObjectNotFoundError):
                return Responses.not_found_err(result.unwrap_err().message)
            elif isinstance(result.unwrap_err(), InitialError):
                return Responses.initial_err(result.unwrap_err().message)
        return Responses.success(data=result.unwrap().to_formatted_dict())
    
    def do_PATCH(
            self, 
            path,
            data: dict,
            ):
        try:
            dto = RatesDTO(
                basecurrencycode = "".join(path[2][:3]),
                targetcurrencycode = "".join(path[2][3:]),
                rate = float(data["rate"][0])
            )
        except (IndexError, KeyError):
            logging.error("Ошибка ввода. Код валюты отсутвует")
            return Responses.input_err(message="Код валюты отустсвует в адресе")
        result = self.service.get_rate(dto)
        if result.is_err():
            if isinstance(result.unwrap_err(), ObjectNotFoundError):
                return Responses.not_found_err(result.unwrap_err().message)
            elif isinstance(result.unwrap_err(), InitialError):
                return Responses.initial_err(result.unwrap_err().message)
            
        current_dto = result.unwrap()
        current_dto.rate = dto.rate 
        result = self.service.update_rate(current_dto)
        if result.is_err():
            if isinstance(result.unwrap_err(), InitialError):
                return Responses.initial_err(result.unwrap_err().message)
            
        return Responses.success(data=current_dto.to_formatted_dict())