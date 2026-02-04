import json
import logging

from result import Err, Ok
from src.errors import InitialError, ObjectAlreadyExists, ObjectNotFoundError
from src.response import Responses
from src.controller.controller_base import BaseController
from src.schema.currencies import CurrenciesCreateSchema
from src.service.service_currencies import CurrenciesService
from src.dto.dto_currencies import CurrenciesDTO

# Валидируем и передаем сервису, а затем возвращаем ответ
class CurrenciesController(BaseController):
    def __init__(
            self,
            service: CurrenciesService,
        ):
        self.service = service


    def do_GET(
            self, path
        ) -> list[dict]:
        result = self.service.get_currencies()

        if result.is_err():
            if isinstance(result.unwrap_err(), ObjectNotFoundError):
                logging.error("Ошибка. База данных currencies пуста")
                return Responses.not_found_err(result.unwrap_err().message)
            
            elif isinstance(result.unwrap_err(), InitialError):
                logging.error(f"Ошибка базы данных или сервера")
                return Responses.initial_err(result.unwrap_err().message)
            
        return Responses.success(data=result.unwrap())


    def do_POST(
            self, 
            path,
            data: dict,
            ):
        try:
            dto = CurrenciesDTO(
                code=data["code"],
                fullname=data["name"],
                sing=data["sing"]
            )
        except KeyError:
            logging.error("Ошибка ввода. Отсутствует нужное поле формы")
            return Responses.input_err(
                message="Отсутствует нужное поле формы. Поля формы:name, code, sing")
        
        result = self.service.post_currencies(dto)
        if result.is_err():
            if isinstance(result.unwrap_err(), ObjectAlreadyExists):
                logging.error(f"Ошибка. Объект {data["name"]} уже существует")
                return Responses.not_found_err(result.unwrap_err().message)
            
            elif isinstance(result.unwrap_err(), InitialError):
                logging.error(f"Ошибка базы данных или сервера")
                return Responses.initial_err(result.unwrap_err().message)
            
        return Responses.success(message=f"Валюта с id {result.value} успешно создана")
