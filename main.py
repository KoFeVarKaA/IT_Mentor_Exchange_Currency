from http.server import HTTPServer
import logging
import os

from dotenv import load_dotenv
from dao.dao_rates import DaoRates
from server import Server

from src.dao.dao_currencies import DaoCurrencies

# dao = DaoCurrencies()
# dao.delete_table()
# dao.create_table()
dao = DaoRates()
dao.delete_table()
dao.create_table()


load_dotenv()

host, port = os.getenv('SERVER_HOST'), int(os.getenv('SERVER_PORT'))
server =  HTTPServer((host, port), Server)

if __name__ == "__main__":
    try:
        logging.info(f"Сервер запущен. Адрес сервера http://{host}:{port}/")
        server.serve_forever()

    except KeyboardInterrupt:
        logging.info('Сервер остановлен')

    finally:
        server.server_close()