import sqlite3
from typing import Any

from src.dto.dto_currencies import CurrenciesCreateDTO
from src.schema.currencies import CurrenciesCreateSchema


class DaoCurrencies():
    def __init__(self):
        pass

    def create_table():
        with sqlite3.connect('bd.sql') as conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE currencies(
                id INT AUTO_INCREMENT PRIMARY KEY, 
                code VARCHAR(30),
                fullname VARCHAR(30),
                sing VARCHAR(5)             
                );
                """)
            
    def post(dto: CurrenciesCreateDTO) -> int:
        with sqlite3.connect('bd.sql') as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(f"""
                INSERT INTO Currencies (code, fullname, sign) VALUES ({dto.code}, {dto.fullname}, {dto.sing})
                """)
                id = cur.lastrowid
        return id

    def get(id: int) -> list[Any]:
        with sqlite3.connect('bd.sql') as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(f"""
                SELECT * FROM Currencies WHERE id = {id}
                """)
                result = cur.fetchall()
        return result

    def get() -> list[CurrenciesCreateSchema]:
        with sqlite3.connect('bd.sql') as conn:
            with conn:
                cur = conn.cursor()
                cur.execute()
    
    def update(id: int, data: dict):
        with sqlite3.connect('bd.sql') as conn:
            with conn:
                cur = conn.cursor()
                cur.execute()
    
    def delete(id: int):
        with sqlite3.connect('bd.sql') as conn:
            with conn:
                cur = conn.cursor()
                cur.execute()