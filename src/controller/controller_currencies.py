import json

from result import Err, Ok
from src.response import Responses
from src.controller.controller_base import BaseController
from src.schema.currencies import CurrenciesCreateSchema
from src.service.service_currencies import CurrenciesService
from src.dto.dto_currencies import CurrenciesCreateDTO

# Валидируем и передаем сервису, а затем возвращаем ответ
class CurrenciesController(BaseController):
    def __init__(
            self,
            service: CurrenciesService,
        ):
        self.service = service


    def do_GET(
            self,
        ) -> list[dict]:
        result = self.service.get_currencies()
        if result.is_err():
            return Responses.initial_err(message=f"Ошибка {result.unwrap_err()}")
        return result.unwrap()


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
