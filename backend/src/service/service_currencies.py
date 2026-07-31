import logging
from result import Result, Ok, Err

from src.utils.exception_handler import exception_handler
from src.dao.dao_currencies import DaoCurrencies
from src.errors import InitialError, ObjectAlreadyExists, ObjectNotFoundError
from src.dto.dto_currencies import CurrenciesDTO


# Принимаем от контроллера, делаем запрос в бд и возвращаем данные, либо ошибку
class CurrenciesService():
    def __init__(self, dao: DaoCurrencies):
        self.dao = dao

    @exception_handler 
    def post_currencies(self, dto: CurrenciesDTO) -> CurrenciesDTO:
        currency = self.dao.get_by_code(code=dto.code)
        if currency:
            raise ObjectAlreadyExists(obj="currencies", field=dto.code)
        
        currency_id = self.dao.post(dto)
        if not currency_id:
            logging.debug(f"Ошибка сервера")
            raise InitialError()
        dto.id = currency_id
        return dto
            
    @exception_handler
    def get_currency(self, code: str) -> CurrenciesDTO:
        currency = self.dao.get_by_code(code=code)
        if not currency:
            raise ObjectNotFoundError(obj="currency", field=code)
        return currency

    @exception_handler
    def get_currencies(self) -> list[CurrenciesDTO]:
        currencies = self.dao.get_all()
        if not currencies:
            raise ObjectNotFoundError(obj="currencies")
        return currencies

    def update_currency(self, id: int, data: dict):
        pass
    
    def delete_currency(self, id: int):
        pass