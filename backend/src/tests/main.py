import logging
import sys
import os
from pathlib import Path
# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
from server import Server
from http.server import HTTPServer

from src.roters.roter_test import controllers


load_dotenv()

host, port = os.getenv('SERVER_HOST_TEST'), int(os.getenv('SERVER_PORT_TEST'))
server =  HTTPServer((host, port), lambda *args, **kwargs: Server(controllers, *args, **kwargs))

if __name__ == "__main__":
    try:
        logging.info(f"Сервер запущен. Адрес сервера http://{host}:{port}/")
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info('Сервер остановлен')

    finally:
        server.server_close()
