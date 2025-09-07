import sqlite3

from src.dao.dao_currencies import DaoCurrencies
from src.dao.dao_rates import DaoRates


class DaoBD():
    
    def create_tables():
        DaoRates.create_table()
        DaoCurrencies.create_table()
    
    def delete_all_tables():
        with sqlite3.connect('bd.sql') as conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master")

            tables = cur.fetchall()
            for table in tables:
                cur.execute(f"DROP TABLE IF EXISTS {table[0]}")
            
            conn.commit()