from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
from typing import Optional
from urllib.parse import urlparse

from src.service.service_currencies import CurrenciesService
from src.controller.controller_currencies import CurrenciesController
from src.controller.controller_rate import RateController
from src.controller.controller_rates import RatesController
from src.controller.controllet_currency import CurrencyController
from src.response import Responses

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

controllers = {
    "exchangeRate": RateController,
    "exchangeRates": RatesController,
    "currency": CurrencyController,
    "currencies": CurrenciesController(service=CurrenciesService()),

}
# Принимаем, обрабатываем запрос, отдаем контроллеру
class Server(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,PATCH,OPTIONS')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

    def do_GET(self):
        logging.debug(f"{self.path}")
        path = urlparse(self.path).path.split("/")
        if path[1] in controllers:
            handle_class = controllers[path[1]]
            if isinstance(handle_class, (RatesController, CurrenciesController)):
                # В данном случае возвращаем массив
                response = handle_class.do_GET(path)
            else:
                # В данном json
                response = handle_class.do_GET(path)
        else:
            message = (
        f"К сожалению, сервер не обрабатывает запросы по адресу {self.path}"
            )
            response = Responses.not_found_err(message)
        
        if response["status_code"] == 200:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            self.send_error_response(response)


    def do_POST(self):
        path = urlparse(self.path).path.split("/")
        print(path)
        if path[1] in controllers:
            response = controllers[path[1]].do_POST(path)
        else:
            message = (
        f"К сожалению, сервен не обрабатывает запросы по адресу {self.path}"
            )
            response = Responses.not_found_err(message)


    def do_PATCH(self):
        path = urlparse(self.path).path.split("/")
        print(path)
        if path[1] in controllers:
            response = controllers[path[1]].do_PATCH(path)
        else:
            message = (
        f"К сожалению, сервен не обрабатывает запросы по адресу {self.path}"
            )
            response = Responses.not_found_err(message)
        


    def send_error_response(self, response: dict):
        self.send_response(response["status_code"])
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response = {"code": str(response["status_code"]), 
                    "status": "Ошибка", 
                    "message": response["message"]}
        self.wfile.write(json.dumps(response).encode("utf-8"))