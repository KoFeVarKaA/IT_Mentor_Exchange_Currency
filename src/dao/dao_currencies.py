import sqlite3
from typing import Any

from src.dto.dto_currencies import CurrenciesDTO
from src.schema.currencies import CurrenciesDTO


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
            
    def post(dto: CurrenciesDTO) -> int:
        with sqlite3.connect('bd.sql') as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(f"""
                INSERT INTO currencies (code, fullname, sing) 
                VALUES (?, ?, ?);
                """, (dto.code, dto.fullname, dto.sing))
                id = cur.lastrowid
        return id

    def get_by_id(id: str) -> CurrenciesDTO:
        with sqlite3.connect('bd.sql') as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(f"""
                SELECT * FROM currencies WHERE id = ?
                """,
                (id))
                result = cur.fetchall()
        if not result:
            return []
        return CurrenciesDTO(
            id=result[0],
            code=result[1],
            fullname=result[2],
            sing=result[3]
        )
    
    def get_by_code(code: str) -> CurrenciesDTO:
        with sqlite3.connect('bd.sql') as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(f"""
                SELECT * FROM currencies WHERE code = ?
                """,
                (code))
                result = cur.fetchall()
        if not result:
            return []
        return CurrenciesDTO(
            id=result[0],
            code=result[1],
            fullname=result[2],
            sing=result[3]
        )
    
    def get_all() -> list[CurrenciesDTO]:
        with sqlite3.connect('bd.sql') as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(f"""
                SELECT * FROM currencies
                """)
                rows = cur.fetchall()
        if not rows:
            return None
        return [CurrenciesDTO(
            id=row[0],
            code=row[1],
            fullname=row[2],
            sing=row[3]
        ) for row in rows]
    
    def update(id: int, dto: CurrenciesDTO):
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