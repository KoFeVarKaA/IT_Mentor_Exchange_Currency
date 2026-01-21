from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from urllib.parse import urlparse

from controller.controller_currencies import CurrenciesController
from controller.controller_rate import RateController
from controller.controller_rates import RatesController
from controller.controllet_currency import CurrencyController

controllers = {
    "exchangeRate": RateController,
    "exchangeRates": RatesController,
    "currency": CurrencyController,
    "currencies": CurrenciesController,

}

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).split("/")[1]
        # if path in co

    def do_POST(self):
        pass

    def do_PATCH(self):
        pass