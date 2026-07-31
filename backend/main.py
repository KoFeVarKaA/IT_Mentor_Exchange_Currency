import logging
import os
from dotenv import load_dotenv
from server import Server
from http.server import HTTPServer

from src.roters.roter import controller_factory


load_dotenv() 

host, port = os.getenv('SERVER_HOST_TEST'), int(os.getenv('SERVER_PORT_TEST')) # type: ignore
server =  HTTPServer((host, port),  # type: ignore
    lambda *args, **kwargs: Server(controller_factory(os.getenv('DATABASE_TEST')), *args, **kwargs)) # type: ignore

if __name__ == "__main__":
    try:
        logging.info(f"Сервер запущен. Адрес сервера http://{host}:{port}/")
        server.serve_forever()

    except KeyboardInterrupt:
        logging.info('Сервер остановлен')

    finally:
        server.server_close()