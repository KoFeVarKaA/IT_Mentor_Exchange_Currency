import sqlite3

from src.dto.dto_rates import RatesDTO, RatesDTO


class DaoRates():
    def __init__(self):
        pass

    @staticmethod
    def create_table():
        with sqlite3.connect('bd.sql') as conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE rates(
                id INETGER PRIMARY KEY AUTOINCREMENT,
                basecurrenceid INETGER,
                targetcurrenceid INETGER,
                rate DECIMAL(6)               
                );
                """)
            
    @staticmethod     
    def delete_table():
        with sqlite3.connect('bd.sql') as conn:
            cur = conn.cursor()
            cur.execute("""DROP TABLE rates;""")
            
    def post(dto: RatesDTO) -> int:
        with sqlite3.connect('bd.sql') as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(f"""
                INSERT INTO rates (basecurrenceid, targetcurrenceid, rate) 
                VALUES (?, ?, ?);
                """, (dto.basecurrenceid, dto.targetcurrenceid, dto.rate))
                id = cur.lastrowid
        return id

    def get(id: int) -> RatesDTO:
        with sqlite3.connect('bd.sql') as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(f"""
                SELECT * FROM rates WHERE id = ?
                """,
                (id))
                result = cur.fetchall()
        if not result:
            return None
        return RatesDTO(
            id=result[0][0],
            basecurrenceid=result[0][1],
            targetcurrenceid=result[0][2],
            sing=result[0][3]
        )
    
    def get_all() -> list[RatesDTO]:
        with sqlite3.connect('bd.sql') as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(f"""
                SELECT * FROM rates
                """)
                rows = cur.fetchall()
        if not rows:
            return None
        return [RatesDTO(
            id=row[0],
            basecurrenceid=row[1],
            targetcurrenceid=row[2],
            sing=row[3]
        ) for row in rows]
    
    def update(id: int, dto: RatesDTO):
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