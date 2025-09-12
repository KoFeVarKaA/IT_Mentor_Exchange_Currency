import json

from result import Err, Ok
from response import Responses
from src.controller.controller_base import BaseController
from src.schema.currencies import CurrenciesCreateSchema
from src.service.service_currencies import CurrenciesService
from src.dto.dto_currencies import CurrenciesCreateDTO


class CurrenciesController(BaseController):
    def post_currencies(
            self, 
            data: CurrenciesCreateSchema,
            service: CurrenciesService,
            ):
        dto = data.to_dto()
        result = service.post_currencies(dto)
        if isinstance(result, Err):
            raise Responses.initial_err(message=result.value)
        return Responses.success(message=f"Валюта с id {result.value} успешно создана")
