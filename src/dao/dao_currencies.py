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
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              code VARCHAR(30),
                              fullname VARCHAR(40),
                              sing VARCHAR(5) 
                            );
                        """)
            
    def post(dto: CurrenciesCreateDTO) -> int:
        with sqlite3.connect('bd.sql') as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(f"""
                INSERT INTO Currencies (code, fullname, sign) 
                VALUES (?, ?, ?);
                """, (dto.code, dto.fullname, dto.sing))
                id = cur.lastrowid
        return id

    def get(id: int) -> list[CurrenciesCreateSchema]:
        with sqlite3.connect('bd.sql') as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(f"""
                SELECT * FROM Currencies WHERE id = ?
                """,
                (id))
                result = cur.fetchall()
        return result
    
    def update(id: int, dto: CurrenciesCreateDTO):
        with sqlite3.connect('bd.sql') as conn:
            with conn:
                cur = conn.cursor()
                cur.execute("""
                UPDATE currencies
                SET code = ?,
                    fullname = ?,
                    sing = ?
                WHERE id = ?;
                """,
                (dto.code, dto.fullname, dto.sing, dto.id))
    
    def delete(id: int):
        with sqlite3.connect('bd.sql') as conn:
            with conn:
                cur = conn.cursor()
                cur.execute("""
                    DELETE FROM currencies
                    WHERE id = ?;
                """,
                (id))