import json

from result import Err, Ok
from src.errors import InitialError, ObjectNotFoundError
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
                return Responses.not_found_err(result.unwrap_err().message)
            elif isinstance(result.unwrap_err(), InitialError):
                return Responses.initial_err(result.unwrap_err().message)
        return Responses.success(data=result.unwrap())


    def do_POST(
            self, 
            data: CurrenciesCreateSchema,
            service: CurrenciesService,
            ):
        dto = data.to_dto()
        result = service.post_currencies(dto)
        if isinstance(result, Err):
            raise Responses.initial_err(message=result.value)
        return Responses.success(message=f"Валюта с id {result.value} успешно создана")
