import os

from dotenv import load_dotenv
from src.controller.controller_currencies import CurrenciesController
from src.controller.controller_exchange import ExchangeController
from src.controller.controller_rate import RateController
from src.controller.controller_rates import RatesController
from src.controller.controllet_currency import CurrencyController
from src.dao.dao_currencies import DaoCurrencies
from src.dao.dao_rates import DaoRates
from src.service.service_currencies import CurrenciesService
from src.service.service_rates import RatesService

load_dotenv()

database = os.getenv('DATABASE')
controllers = {
    "exchange" : ExchangeController(
        service=RatesService(DaoRates(database=database), DaoCurrencies(database=database))
    ), 
    "exchangeRate": RateController(
        service=RatesService(DaoRates(database=database), DaoCurrencies(database=database))
    ),
    "exchangeRates": RatesController(
        service=RatesService(DaoRates(database=database), DaoCurrencies(database=database))
    ),
    "currency": CurrencyController(
        service=CurrenciesService(DaoCurrencies(database=database))
    ),
    "currencies": CurrenciesController(
        service=CurrenciesService(DaoCurrencies(database=database))
    ),
}