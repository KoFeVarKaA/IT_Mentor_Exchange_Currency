from result import Result, Ok, Err

from src.dao.dao_currencies import DaoCurrencies
from src.errors import InitialError, ObjectNotFoundError
from src.dto.dto_currencies import CurrenciesDTO


# Принимаем от контроллера, делаем запрос в бд и возвращаем данные, либо ошибку
class CurrenciesService():
    def __init__(self):
        self.dao = DaoCurrencies
        
    def post_currencies(self, dto: CurrenciesDTO) -> Result[None, InitialError]:
        currency_id = self.dao.post(dto)

        if currency_id == None:
            return Err(InitialError())
        return Ok(currency_id)
            

    def get_currency(self, id: int) -> Result[None, None]:
        pass

    def get_currencies(self) -> Result[list[CurrenciesDTO], ObjectNotFoundError | InitialError]:
        try:
            currencies = self.dao.get_all()
            if not currencies:
                return Err(ObjectNotFoundError(obj="currencies"))
            return currencies
        except:
            return Err(InitialError())

    def update_currency(self, id: int, data: dict) -> Result[None, None]:
        pass
    
    def delete_currency(self, id: int) -> Result[None, None]:
        pass