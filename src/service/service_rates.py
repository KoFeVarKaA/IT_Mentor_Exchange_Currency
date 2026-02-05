from dataclasses import asdict
import logging
from result import Result, Ok, Err

from src.dao.dao_currencies import DaoCurrencies
from src.dto.dto_rates import RatesDTO
from src.dao.dao_rates import DaoRates
from src.errors import InitialError, ObjectAlreadyExists, ObjectNotFoundError


# Принимаем от контроллера, делаем запрос в бд и возвращаем данные, либо ошибку
class RatesService():
    def __init__(self):
        self.dao = DaoRates
        self.dao_currencies = DaoCurrencies
        
    def post_rates(self, dto: RatesDTO) -> Result[RatesDTO, InitialError | ObjectAlreadyExists]:
        rate = self.dao.get_by_code(code=dto.code)
        if rate:
            return Err(ObjectAlreadyExists(obj="rates", field=dto.code))
        
        rate_id = self.dao.post(dto)
        if not rate_id:
            logging.debug(f"Ошибка сервера")
            return Err(InitialError())
        dto.id = rate_id
        return Ok(dto)
            

    def get_rate(self, id: int) -> Result[RatesDTO, ObjectNotFoundError | InitialError]:
        try:
            rate = self.dao.get_by_id(id=id)
            if not rate:
                return Err(ObjectNotFoundError(obj="rate", field=id))
            return Ok(rate)
        except Exception as e:
            logging.debug(f"Ошибка: {e}")
            return Err(InitialError())


    def get_rates(self) -> Result[list[RatesDTO], ObjectNotFoundError | InitialError]:
        try:
            rates = self.dao.get_all()
            if not rates:
                return Err(ObjectNotFoundError(obj="rates"))
            for i in len(rates):
                rates[i].basecurrenceid = asdict(self.dao_currencies.get_by_id(rates[i].basecurrenceid))
                rates[i].targetcurrenceid = asdict(self.dao_currencies.get_by_id(rates[i].targetcurrenceid))
            return Ok(rates)
        except Exception as e:
            logging.debug(f"Ошибка: {e}")
            return Err(InitialError())