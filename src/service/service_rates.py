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

    def get_rate(self, id: int=None) -> Result[RatesDTO, ObjectNotFoundError | InitialError]:
        try:
            rate = self.dao.get_by_id(id=id)
            if not rate:
                return Err(ObjectNotFoundError(obj="rate", field=id))
            rate.basecurrenceid = asdict(self.dao_currencies.get_by_id(rate.basecurrenceid))
            rate.targetcurrenceid = asdict(self.dao_currencies.get_by_id(rate.targetcurrenceid))
            return Ok(rate)
        except Exception as e:
            logging.debug(f"Ошибка: {e}")
            return Err(InitialError())

    def get_rates(self) -> Result[list[RatesDTO], ObjectNotFoundError | InitialError]:
        try:
            rates = self.dao.get_all()
            if not rates:
                return Err(ObjectNotFoundError(obj="rates"))
            for i in range(len(rates)):
                rates[i].basecurrence = asdict(self.dao_currencies.get_by_id(rates[i].basecurrenceid))
                rates[i].targetcurrence = asdict(self.dao_currencies.get_by_id(rates[i].targetcurrenceid))
            return Ok(rates)
        except Exception as e:
            logging.debug(f"Ошибка: {e}")
            return Err(InitialError())
        
            
    def post_rate(self, dto: RatesDTO) -> Result[RatesDTO, InitialError | ObjectAlreadyExists]:
        dto.basecurrenceid = self.dao_currencies.get_id_by_code(dto.basecurrencecode)
        dto.targetcurrenceid = self.dao_currencies.get_id_by_code(dto.basecurrencecode)
        rate = self.dao.get_by_ids(
            basecurrencyid=dto.basecurrenceid, targetcurrencyid=dto.targetcurrenceid
        )
        if rate:
            return Err(ObjectAlreadyExists(
                obj="rates", field=f"({dto.basecurrenceid}, {dto.targetcurrenceid})"))
        
        rate_id = self.dao.post(dto)
        if not rate_id:
            logging.debug(f"Ошибка сервера")
            return Err(InitialError())
        dto.id = rate_id
        bc = self.dao_currencies.get_by_code(dto.basecurrencecode)
        tc = self.dao_currencies.get_by_code(dto.targetcurrencecode)
        if not bc or not tc:
            return Err(ObjectNotFoundError(
                obj="rates", field=f"({dto.basecurrencecode}, {dto.targetcurrencecode})"))
        dto.basecurrence = asdict(bc)
        dto.targetcurrence= asdict(tc)
        return Ok(dto)