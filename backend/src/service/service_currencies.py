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
        
    def post_currencies(self, dto: CurrenciesDTO) -> Result[CurrenciesDTO, InitialError | ObjectAlreadyExists]:
        currency = self.dao.get_by_code(code=dto.code)
        if currency:
            return Err(ObjectAlreadyExists(obj="currencies", field=dto.code))
        
        currency_id = self.dao.post(dto)
        if not currency_id:
            logging.debug(f"Ошибка сервера")
            return Err(InitialError())
        dto.id = currency_id
        return Ok(dto)
            
    @exception_handler
    def get_currency(self, code: str) -> Result[CurrenciesDTO, ObjectNotFoundError | InitialError]:
        currency = self.dao.get_by_code(code=code)
        if not currency:
            return Err(ObjectNotFoundError(obj="currency", field=code))
        return Ok(currency)

    @exception_handler
    def get_currencies(self) -> Result[list[CurrenciesDTO], ObjectNotFoundError | InitialError]:
        currencies = self.dao.get_all()
        if not currencies:
            return Err(ObjectNotFoundError(obj="currencies"))
        return Ok(currencies)

    def update_currency(self, id: int, data: dict) -> Result[None, None]:
        pass
    
    def delete_currency(self, id: int) -> Result[None, None]:
        pass