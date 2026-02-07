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

    def get_rate_id_by_code(self, 
                currencycode: str,
        ) -> Result[RatesDTO, ObjectNotFoundError | InitialError]:
        try:
            currencyid = self.dao_currencies.get_id_by_code(currencycode)
            if not currencyid:
                return Err(ObjectNotFoundError(obj="rates", field=currencycode))
            return Ok(currencyid)
        
        except Exception as e:
            logging.debug(f"Ошибка: {e}")
            return Err(InitialError())

    def get_rate(self, 
                dto: RatesDTO
        ) -> Result[RatesDTO, ObjectNotFoundError | InitialError]:
        def supplement_res(dto: RatesDTO):
            dto.basecurrency = asdict(self.dao_currencies.get_by_id(dto.basecurrencyid))
            dto.targetcurrency = asdict(self.dao_currencies.get_by_id(dto.targetcurrencyid))
            return dto

        try:
            dto.basecurrencyid = self.dao_currencies.get_id_by_code(dto.basecurrencycode)
            dto.targetcurrencyid = self.dao_currencies.get_id_by_code(dto.targetcurrencycode)
            if not dto.basecurrencyid:
                return Err(ObjectNotFoundError(obj="rates", field=dto.basecurrencyid))
            elif not dto.targetcurrencyid:
                return Err(ObjectNotFoundError(obj="rates", field=dto.targetcurrencyid))
            
            # Cуществует валютная пара AB - берём её курс
            rate = self.dao.get_by_ids(
                basecurrencyid=dto.basecurrencyid, targetcurrencyid=dto.targetcurrencyid)
            if rate:
                return Ok(supplement_res(rate))

            # Cуществует валютная пара BA - берем её курс, и считаем обратный, чтобы получить AB
            rate = self.dao.get_by_ids(
                basecurrencyid=dto.targetcurrencyid, targetcurrencyid=dto.basecurrencyid)
            if rate:
                rate.rate = 1 / rate.rate
                return Ok(supplement_res(rate))
            
            # Cуществуют валютные пары USD-A и USD-B - вычисляем из этих курсов курс AB
            usd_id = self.dao_currencies.get_id_by_code(code="USD")
            rate1 = self.dao.get_by_ids(
                basecurrencyid=usd_id, targetcurrencyid=dto.basecurrencyid)
            rate2 = self.dao.get_by_ids(
                basecurrencyid=usd_id, targetcurrencyid=dto.targetcurrencyid)
            if rate1 and rate2:
                dto.rate = rate2.rate / rate1.rate
                return Ok(supplement_res(dto))

            
            return Err(ObjectNotFoundError(obj="dto", field=f"({dto.basecurrencycode}, {dto.targetcurrencycode})"))
        
        except Exception as e:
            logging.debug(f"Ошибка: {e}")
            return Err(InitialError())

    def get_rates(self) -> Result[list[RatesDTO], ObjectNotFoundError | InitialError]:
        try:
            rates = self.dao.get_all()
            if not rates:
                return Err(ObjectNotFoundError(obj="rates"))
            for i in range(len(rates)):
                rates[i].basecurrency = asdict(self.dao_currencies.get_by_id(rates[i].basecurrencyid))
                rates[i].targetcurrency = asdict(self.dao_currencies.get_by_id(rates[i].targetcurrencyid))
            return Ok(rates)
        
        except Exception as e:
            logging.debug(f"Ошибка: {e}")
            return Err(InitialError())
        
            
    def post_rate(self, dto: RatesDTO) -> Result[RatesDTO, InitialError | ObjectAlreadyExists| ObjectNotFoundError]:
        try:
            dto.basecurrencyid = self.dao_currencies.get_id_by_code(dto.basecurrencycode)
            dto.targetcurrencyid = self.dao_currencies.get_id_by_code(dto.targetcurrencycode)
            if not dto.basecurrencyid:
                return Err(ObjectNotFoundError(obj="rates", field=dto.basecurrencyid))
            elif not dto.targetcurrencyid:
                return Err(ObjectNotFoundError(obj="rates", field=dto.targetcurrencyid))
            rate = self.dao.get_by_ids(
                basecurrencyid=dto.basecurrencyid, targetcurrencyid=dto.targetcurrencyid
            )
            if rate:
                return Err(ObjectAlreadyExists(
                    obj="rates", field=f"({dto.basecurrencyid}, {dto.targetcurrencyid})"))


            rate_id = self.dao.post(dto)
            if not rate_id:
                logging.debug(f"Ошибка сервера")
                return Err(InitialError())
            dto.id = rate_id
            bc = self.dao_currencies.get_by_code(dto.basecurrencycode)
            tc = self.dao_currencies.get_by_code(dto.targetcurrencycode)
            if not bc or not tc:
                return Err(ObjectNotFoundError(
                    obj="rates", field=f"({dto.basecurrencycode}, {dto.targetcurrencycode})"))
            dto.basecurrency = asdict(bc)
            dto.targetcurrency= asdict(tc)
            return Ok(dto)
        
        except Exception as e:
            logging.debug(f"Ошибка: {e}")
            return Err(InitialError())
        
    def update_rate(self, dto: RatesDTO) -> Result[None, InitialError]:
        try:
            self.dao.update_rate(dto=dto)
            return Ok(None)
        except Exception as e:
            logging.debug(f"Ошибка: {e}")
            return Err(InitialError())