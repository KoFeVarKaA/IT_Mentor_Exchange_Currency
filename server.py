from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
from typing import Optional
from urllib.parse import urlparse

from src.controller.controller_currencies import CurrenciesController
from src.controller.controller_rate import RateController
from src.controller.controller_rates import RatesController
from src.controller.controllet_currency import CurrencyController
from src.response import Responses

controllers = {
    "exchangeRate": RateController,
    "exchangeRates": RatesController,
    "currency": CurrencyController,
    "currencies": CurrenciesController,

}
# Принимаем, обрабатываем запрос, отдаем контроллеру
class Server(BaseHTTPRequestHandler):
    def do_GET(self) -> dict | list:
        path = urlparse(self.path).path.split("/")
        if path[1] in controllers:
            handle_class = path[1]
            if isinstance(handle_class(), (RatesController, CurrenciesController)):
                # В данном случае возвращаем массив
                response = controllers[path[1]].do_GET(path)
            else:
                # В данном json
                response = controllers[path[1]].do_GET(path)
        else:
            message = (
        f"К сожалению, сервен не обрабатывает запросы по адресу {self.path}"
            )
            response = Responses.not_found_err(message)
        return response


    def do_POST(self) -> dict:
        path = urlparse(self.path).path.split("/")
        print(path)
        if path[1] in controllers:
            response = controllers[path[1]].do_POST(path)
        else:
            message = (
        f"К сожалению, сервен не обрабатывает запросы по адресу {self.path}"
            )
            response = Responses.not_found_err(message)
        return response


    def do_PATCH(self) -> dict:
        path = urlparse(self.path).path.split("/")
        print(path)
        if path[1] in controllers:
            response = controllers[path[1]].do_PATCH(path)
        else:
            message = (
        f"К сожалению, сервен не обрабатывает запросы по адресу {self.path}"
            )
            response = Responses.not_found_err(message)
        return response