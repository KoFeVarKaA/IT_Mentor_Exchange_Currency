from http.server import HTTPServer
import logging
import os

from dotenv import load_dotenv
from server import Server

load_dotenv()

host, port = os.getenv('SERVER_HOST'), int(os.getenv('SERVER_PORT'))
server =  HTTPServer((host, port), Server)

if __name__ == "__main__":
    try:
        logging.info(f"Сервер запущен. Адрес сервера {host}:{port}")
        server.serve_forever()

    except KeyboardInterrupt:
        logging.info('Сервер остановлен')

    finally:
        server.server_close()