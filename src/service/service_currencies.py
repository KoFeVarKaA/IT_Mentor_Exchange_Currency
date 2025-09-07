from result import Result, Ok, Err

from dao.dao_currencies import DaoCurrencies
from errors import Errors
from src.dto.dto_currencies import CurrenciesCreateDTO


class CurrenciesService():
    def __init__(self):
        self.dao = DaoCurrencies
        
    def post_currencies(self, dto: CurrenciesCreateDTO) -> Result[None, None]:
        currency_id = self.dao.post(dto)

        if currency_id == None:
            return Err(Errors.something_goes_wrong())
        return Ok(currency_id)
            

    def get_currency(self, id: int) -> Result[None, None]:
        pass

    def get_currencies(self, ) -> Result[None, None]:
        pass
    
    def update_currency(self, id: int, data: dict) -> Result[None, None]:
        pass
    
    def delete_currency(self, id: int) -> Result[None, None]:
        pass