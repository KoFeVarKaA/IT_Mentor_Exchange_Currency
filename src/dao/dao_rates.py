import sqlite3

from dto.dto_rates import RatesCreateDTO
from schema.rates import RatesCreateSchema


class DaoRates():
    def __init__(self):
        pass

    def create_table():
        with sqlite3.connect('bd.sql') as conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE rates(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                basecurrenceid VARCHAR(30),
                targetcurrenceid VARCHAR(30),
                rate DECIMAL(6)               
                );
                """)
            
    def post(dto: RatesCreateDTO) -> int:
        with sqlite3.connect('bd.sql') as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(f"""
                INSERT INTO rates (basecurrenceid, targetcurrenceid, rate) 
                VALUES (?, ?, ?);
                """, (dto.basecurrenceid, dto.targetcurrenceid, dto.rate))
                id = cur.lastrowid
        return id

    def get(id: int) -> list[RatesCreateSchema]:
        with sqlite3.connect('bd.sql') as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(f"""
                SELECT * FROM rates WHERE id = ?
                """,
                (id))
                result = cur.fetchall()
        return result
    
    def update(id: int, dto: RatesCreateDTO):
        with sqlite3.connect('bd.sql') as conn:
            with conn:
                cur = conn.cursor()
                cur.execute("""
                UPDATE rates
                SET basecurrenceid = ?,
                    targetcurrenceid = ?,
                    rate = ?
                WHERE id = ?;
                """,
                (dto.basecurrenceid, dto.targetcurrenceid, dto.rate, dto.id))
    
    def delete(id: int):
        with sqlite3.connect('bd.sql') as conn:
            with conn:
                cur = conn.cursor()
                cur.execute("""
                    DELETE FROM rates
                    WHERE id = ?;
                """,
                (id))