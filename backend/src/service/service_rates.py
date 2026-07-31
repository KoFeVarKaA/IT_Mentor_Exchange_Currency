
import logging
from result import Result, Ok, Err

from src.utils.exception_handler import exception_handler
from src.dao.dao_currencies import DaoCurrencies
from src.dto.dto_rates import RatesDTO
from src.dao.dao_rates import DaoRates
from src.errors import InitialError, ObjectAlreadyExists, ObjectNotFoundError


# Принимаем от контроллера, делаем запрос в бд и возвращаем данные, либо ошибку
class RatesService():
    def __init__(
            self,
            dao : DaoRates,
            dao_currencies : DaoCurrencies
        ):
        self.dao = dao
        self.dao_currencies = dao_currencies            

    @exception_handler 
    def get_rate_id_by_code(self, 
                currencycode: str,
        ) -> str:
        currencyid = self.dao_currencies.get_id_by_code(currencycode)
        if not currencyid:
            raise ObjectNotFoundError(obj="rates", field=currencycode)
        return currencyid
        
    @exception_handler 
    def get_rate(self, 
                dto: RatesDTO
        ) -> RatesDTO:
        def supplement_res(dto: RatesDTO):
            dto.basecurrency = self.dao_currencies.get_by_id(dto.basecurrencyid).to_formatted_dict()
            dto.targetcurrency = self.dao_currencies.get_by_id(dto.targetcurrencyid).to_formatted_dict()
            return dto

        dto.basecurrencyid = self.dao_currencies.get_id_by_code(dto.basecurrencycode)
        dto.targetcurrencyid = self.dao_currencies.get_id_by_code(dto.targetcurrencycode)
        if not dto.basecurrencyid:
            raise ObjectNotFoundError(obj="rates", field=dto.basecurrencyid)
        elif not dto.targetcurrencyid:
            raise ObjectNotFoundError(obj="rates", field=dto.targetcurrencyid)
        
        # Cуществует валютная пара AB - берём её курс
        rate = self.dao.get_by_ids(
            basecurrencyid=dto.basecurrencyid, targetcurrencyid=dto.targetcurrencyid)
        if rate:
            return supplement_res(rate)
        
        # Cуществует валютная пара BA - берем её курс, и считаем обратный, чтобы получить AB
        rate = self.dao.get_by_ids(
            basecurrencyid=dto.targetcurrencyid, targetcurrencyid=dto.basecurrencyid)
        if rate:
            rate.rate = 1 / rate.rate
            return supplement_res(rate)
        
        # Cуществуют валютные пары USD-A и USD-B - вычисляем из этих курсов курс AB
        usd_id = self.dao_currencies.get_id_by_code(code="USD")
        rate1 = self.dao.get_by_ids(
            basecurrencyid=usd_id, targetcurrencyid=dto.basecurrencyid)
        rate2 = self.dao.get_by_ids(
            basecurrencyid=usd_id, targetcurrencyid=dto.targetcurrencyid)
        if rate1 and rate2:
            dto.rate = rate2.rate / rate1.rate
            return supplement_res(dto)
        
        raise ObjectNotFoundError(obj="dto", field=f"({dto.basecurrencycode}, {dto.targetcurrencycode})")

    @exception_handler 
    def get_rates(self) -> list[RatesDTO]:
        rates = self.dao.get_all()
        if not rates:
            raise ObjectNotFoundError(obj="rates")
        for i in range(len(rates)):
            rates[i].basecurrency = self.dao_currencies.get_by_id(rates[i].basecurrencyid).to_formatted_dict()
            rates[i].targetcurrency = self.dao_currencies.get_by_id(rates[i].targetcurrencyid).to_formatted_dict()
        return rates
    
    @exception_handler   
    def post_rate(self, dto: RatesDTO) -> RatesDTO:
        dto.basecurrencyid = self.dao_currencies.get_id_by_code(dto.basecurrencycode)
        dto.targetcurrencyid = self.dao_currencies.get_id_by_code(dto.targetcurrencycode)
        if not dto.basecurrencyid:
            raise ObjectNotFoundError(obj="rates", field=dto.basecurrencyid)
        elif not dto.targetcurrencyid:
            raise ObjectNotFoundError(obj="rates", field=dto.targetcurrencyid)
        rate = self.dao.get_by_ids(
            basecurrencyid=dto.basecurrencyid, targetcurrencyid=dto.targetcurrencyid
        )
        if rate:
            raise ObjectAlreadyExists(
                obj="rates", field=f"({dto.basecurrencyid}, {dto.targetcurrencyid})")

        rate_id = self.dao.post(dto)
        if not rate_id:
            logging.debug(f"Ошибка сервера")
            raise InitialError()
        dto.id = rate_id
        bc = self.dao_currencies.get_by_code(dto.basecurrencycode)
        tc = self.dao_currencies.get_by_code(dto.targetcurrencycode)
        if not bc or not tc:
            raise ObjectNotFoundError(
                obj="rates", field=f"({dto.basecurrencycode}, {dto.targetcurrencycode})")
        dto.basecurrency = bc.to_formatted_dict()
        dto.targetcurrency= tc.to_formatted_dict()
        return dto
    
    @exception_handler
    def update_rate(self, dto: RatesDTO) -> None:
        self.dao.update_rate(dto=dto)
        return None