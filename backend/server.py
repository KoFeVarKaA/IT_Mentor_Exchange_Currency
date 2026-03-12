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
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Type', 'application/json')
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

    def do_GET(self):
        self._process_request("GET")

    def do_POST(self):
        self._process_request("POST")

    def do_PATCH(self):
        self._process_request("PATCH")
        
    def _process_request(self, command: str):
        logging.debug(f"{self.command} {self.client_address}{self.path}")
        parsed_url = urlparse(self.path)
        path = parsed_url.path.split("/")
        query = parse_qs(parsed_url.query)
        content_length = int(self.headers.get('Content-Length', 0))
        data = parse_qs(self.rfile.read(content_length).decode('utf-8'))

        if path[1] not in self.controllers:
            message = "К сожалению, сервер не обрабатывает запросы по данному адресу"
            self._send_response(Responses.initial_err(message))
            return
        
        handle_class = self.controllers[path[1]]
        if  command == "GET":
            response = handle_class.do_GET(path, query)
        elif command == "POST":
            response = handle_class.do_POST(path, data)
        elif command == "PATCH":
            response = handle_class.do_PATCH(path, data)
        self._send_response(response)

    def _send_response(self, response: dict):
        if 200 <= response["status_code"] <= 201:
            logging.info("Запрос успешно выполнен")

            self.send_response(response["status_code"])
            self.send_header("Content-Type", "text/html")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            self.wfile.write(json.dumps(response["data"]).encode("utf-8"))
        else:
            logging.error(f"{response['data']['message']}")
            self._send_error_response(response)

    def _send_error_response(self, response: dict):
        self.send_response(response["status_code"])
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response = {"code": str(response["status_code"]), 
                    "status": "Ошибка", 
                    "message": response["data"]["message"]}
        self.wfile.write(json.dumps(response).encode("utf-8"))