from http.server import BaseHTTPRequestHandler
import json
import logging
from urllib.parse import parse_qs, urlparse

from src.controller.controller_currencies import CurrenciesController
from src.controller.controller_exchange import ExchangeController
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

# Принимаем, обрабатываем запрос, отдаем контроллеру
class Server(BaseHTTPRequestHandler):
    def __init__(self, controllers:dict, *args, **kwargs):
        self.controllers = controllers
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        return

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,PATCH,OPTIONS')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

    def do_GET(self):
        logging.debug(f"GET {"/".join(map(str, self.client_address))}{self.path}")
        parsed_url = urlparse(self.path)
        path = parsed_url.path.split("/")
        query = parse_qs(parsed_url.query)
        if path[1] in self.controllers:
            handle_class = self.controllers[path[1]]
            if isinstance(handle_class, (RatesController, CurrenciesController)):
                # В данном случае возвращаем массив
                response = handle_class.do_GET(path)
            # Можно сократить до else
            elif isinstance(handle_class, (RateController, CurrencyController, ExchangeController)):
                # В данном json
                response = handle_class.do_GET(path, query)
        else:
            message = (
        f"К сожалению, сервер не обрабатывает запросы по данному адресу"
            )
            response = Responses.initial_err(message)
        
        if response["status_code"] == 200:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            self.wfile.write(json.dumps(response["data"]).encode("utf-8"))
        else:
            self.send_error_response(response)


    def do_POST(self):
        logging.debug(f"POST {"/".join(map(str, self.client_address))}{self.path}")
        parsed_url = urlparse(self.path)
        path = parsed_url.path.split("/")
        content_length = int(self.headers.get('Content-Length', 0))
        data = parse_qs(self.rfile.read(content_length).decode('utf-8'))
        if path[1] in self.controllers:
            handle_class = self.controllers[path[1]]
            # Можно потом убрать
            if isinstance(handle_class, (RatesController, CurrenciesController)):
                response = handle_class.do_POST(path, data)
        else:
            message = (
        f"К сожалению, сервер не обрабатывает запросы по данному адресу"
            )
            response = Responses.initial_err(message)
        
        if response["status_code"] == 200:
            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            self.wfile.write(json.dumps(response["data"]).encode("utf-8"))
        else:
            self.send_error_response(response)


    def do_PATCH(self):
        logging.debug(f"PATCH {self.client_address}{self.path}")
        parsed_url = urlparse(self.path)
        path = parsed_url.path.split("/")
        content_length = int(self.headers.get('Content-Length', 0))
        data = parse_qs(self.rfile.read(content_length).decode('utf-8'))
        if path[1] in self.controllers:
            handle_class = self.controllers[path[1]]
            # Можно потом убрать
            if isinstance(handle_class, (RateController)):
                response = handle_class.do_PATCH(path, data)
        else:
            message = (
        f"К сожалению, сервер не обрабатывает запросы по данному адресу"
            )
            response = Responses.initial_err(message)
        
        if response["status_code"] == 200:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            self.wfile.write(json.dumps(response["data"]).encode("utf-8"))
        else:
            self.send_error_response(response)
        


    def send_error_response(self, response: dict):
        self.send_response(response["status_code"])
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response = {"code": str(response["status_code"]), 
                    "status": "Ошибка", 
                    "message": response["message"]}
        self.wfile.write(json.dumps(response).encode("utf-8"))