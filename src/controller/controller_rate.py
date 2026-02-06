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
            basecurrencecode, targetcurrencecode = "".join(path[2][:3]), "".join(path[2][3:]) 
        except KeyError:
            logging.error("Ошибка ввода. Код валюты отсутвует")
            return Responses.input_err(message="Код валюты отустсвует в адресе")
        result = self.service.get_rate(
            basecurrencecode=basecurrencecode, targetcurrencecode=targetcurrencecode
        )
        if result.is_err():
            if isinstance(result.unwrap_err(), ObjectNotFoundError):
                return Responses.not_found_err(result.unwrap_err().message)
            elif isinstance(result.unwrap_err(), InitialError):
                return Responses.initial_err(result.unwrap_err().message)
        return Responses.success(data=self.format_rates_dto(result.unwrap()))
    
    def format_rates_dto(self, rates_dto: RatesDTO):
        return {
            "id": rates_dto.id,
            "baseCurrency": rates_dto.basecurrence,
            "targetCurrency": rates_dto.targetcurrence,
            "rate": rates_dto.rate
        }
    
    def do_PATCH(
            self, 
            path,
            data: dict,
            ):
        try:
            dto = RatesDTO(
                basecurrencecode = "".join(path[2][:3]),
                targetcurrencecode = "".join(path[2][3:]) 
            )
        except IndexError:
            logging.error("Ошибка ввода. Код валюты отсутвует")
            return Responses.input_err(message="Код валюты отустсвует в адресе")
        result = self.service.get_rate(
            basecurrencecode=dto.basecurrencecode, targetcurrencecode=dto.targetcurrencecode
        )
        if result.is_err():
            if isinstance(result.unwrap_err(), ObjectNotFoundError):
                return Responses.not_found_err(result.unwrap_err().message)
            elif isinstance(result.unwrap_err(), InitialError):
                return Responses.initial_err(result.unwrap_err().message)
            
        dto = result.unwrap()
        dto.rate = data["rate"][0]
        result = self.service.update_rate(dto)
        if result.is_err():
            if isinstance(result.unwrap_err(), InitialError):
                return Responses.initial_err(result.unwrap_err().message)
            
        return Responses.success(data=self.format_rates_dto(dto))