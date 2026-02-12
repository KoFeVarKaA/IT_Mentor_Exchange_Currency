
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
            
        data = [rate.to_formatted_dict() for rate in result.unwrap()]
        return Responses.success(data=data)
    
    def do_POST(
            self, 
            path,
            data: dict,
            ):
        try:
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
        except KeyError:
            logging.error("Ошибка ввода. Отсутствует нужное поле формы")
            return Responses.input_err(
                message="Отсутствует нужное поле формы")
        
        if len(dto.basecurrencycode) != 3 or len(dto.basecurrencycode) != 3:
            logging.error("Ошибка ввода. Неправильный вид валюты")
            return Responses.input_err(
                message="Ошибка ввода. Длина кода валюты должна составлять 3 символа")
        if not isinstance(dto.rate, float):
            logging.error("Ошибка ввода. Неправильный тип данных")
            return Responses.input_err(
                message="Ошибка ввода. Курс обмена должен состоять из чисел")
        
        result = self.service.post_rate(dto)
        if result.is_err():
            if isinstance(result.unwrap_err(), ObjectNotFoundError):
                logging.error("Ошибка. Запись в currencies не найдена")
                return Responses.not_found_err(result.unwrap_err().message)
            
            elif isinstance(result.unwrap_err(), ObjectAlreadyExists):
                logging.error(f"Ошибка. Объект rates уже существует")
                return Responses.already_exists(result.unwrap_err().message)
            
            elif isinstance(result.unwrap_err(), InitialError):
                logging.error(f"Ошибка базы данных или сервера")
                return Responses.initial_err(result.unwrap_err().message)
        
        return Responses.success(data=result.unwrap().to_formatted_dict())
