import sqlite3
from typing import Any

from src.dto.dto_currencies import CurrenciesDTO


class DaoCurrencies():
    def __init__(self, database: str):
        self.database = database

    def create_table(self):
        with sqlite3.connect(self.database) as conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE currencies(
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              code VARCHAR(30),
                              fullname VARCHAR(40),
                              sign VARCHAR(5) 
                            );
                        """)
    
    def delete_table(self):
        with sqlite3.connect(self.database) as conn:
            cur = conn.cursor()
            cur.execute("""DROP TABLE currencies;""")
            
    def post(self, dto: CurrenciesDTO) -> int:
        with sqlite3.connect(self.database) as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(f"""
                INSERT INTO currencies (code, fullname, sign) 
                VALUES (?, ?, ?);
                """, (dto.code, dto.fullname, dto.sign))
                currency_id = cur.lastrowid
        return currency_id

    def get_by_id(self, id: str) -> CurrenciesDTO:
        with sqlite3.connect(self.database) as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(f"""
                SELECT * FROM currencies WHERE id = ?
                """,
                (id,))
                result = cur.fetchall()
        if not result:
            return []
        return CurrenciesDTO(
            id=result[0][0],
            code=result[0][1],
            fullname=result[0][2],
            sign=result[0][3]
        )
    
    def get_id_by_code(self, code: str) -> int:
        with sqlite3.connect(self.database) as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(f"""
                SELECT id FROM currencies WHERE code = ?
                """,
                (code,))
                result = cur.fetchall()
        if not result:
            return []
        return result[0][0]

    def get_by_code(self, code: str) -> CurrenciesDTO:
        with sqlite3.connect(self.database) as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(f"""
                SELECT * FROM currencies WHERE code = ?
                """,
                (code,))
                result = cur.fetchall()
        if not result:
            return []
        return CurrenciesDTO(
            id=result[0][0],
            code=result[0][1],
            fullname=result[0][2],
            sign=result[0][3]
        )
    
    def get_all(self, ) -> list[CurrenciesDTO]:
        with sqlite3.connect(self.database) as conn:
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
            sign=row[3]
        ) for row in rows]
    
    def update(self, id: int, dto: CurrenciesDTO):
        with sqlite3.connect(self.database) as conn:
            with conn:
                cur = conn.cursor()
                cur.execute("""
                UPDATE currencies
                SET code = ?,
                    fullname = ?,
                    sign = ?
                WHERE id = ?;
                """,
                (dto.code, dto.fullname, dto.sign, dto.id))
        
    
    def delete(self, id: int):
        with sqlite3.connect(self.database) as conn:
            with conn:
                cur = conn.cursor()
                cur.execute("""
                    DELETE FROM currencies
                    WHERE id = ?;
                """,
                (id,))