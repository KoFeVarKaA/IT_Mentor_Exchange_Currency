import sqlite3

from src.dto.dto_rates import RatesDTO


class DaoRates():
    def __init__(self, database: str):
        self.database = database

    def create_table(self):
        with sqlite3.connect(self.database) as conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE rates(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                basecurrencyid INTEGER,
                targetcurrencyid INTEGER,
                rate REAL               
                );
                """)
                 
    def delete_table(self):
        with sqlite3.connect(self.database) as conn:
            cur = conn.cursor()
            cur.execute("""DROP TABLE rates;""")
            
    def post(self, dto: RatesDTO) -> int:
        with sqlite3.connect(self.database) as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(f"""
                INSERT INTO rates (basecurrencyid, targetcurrencyid, rate) 
                VALUES (?, ?, ?);
                """, (dto.basecurrencyid, dto.targetcurrencyid, dto.rate))
                id = cur.lastrowid
        return id

    def get_by_id(self, id: str) -> RatesDTO:
        with sqlite3.connect(self.database) as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(f"""
                SELECT * FROM rates WHERE id = ?
                """,
                (id,))
                result = cur.fetchall()
        if not result:
            return None
        return RatesDTO(
            id=result[0][0],
            basecurrencyid=result[0][1],
            targetcurrencyid=result[0][2],
            rate=result[0][3]
        )
    
    def get_by_ids(
            self, basecurrencyid:str, targetcurrencyid:str
        ) ->RatesDTO:
        with sqlite3.connect(self.database) as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(f"""
                SELECT * FROM rates 
                WHERE basecurrencyid = ? AND targetcurrencyid = ?
                """,
                (basecurrencyid, targetcurrencyid))
                result = cur.fetchall()
        if not result:
            return None
        return RatesDTO(
            id=result[0][0],
            basecurrencyid=result[0][1],
            targetcurrencyid=result[0][2],
            rate=result[0][3]
        )
    
    def get_all(self) -> list[RatesDTO]:
        with sqlite3.connect(self.database) as conn:
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
            basecurrencyid=row[1],
            targetcurrencyid=row[2],
            rate=row[3]
        ) for row in rows]
    
    def update(self, id: int, dto: RatesDTO):
        with sqlite3.connect(self.database) as conn:
            with conn:
                cur = conn.cursor()
                cur.execute("""
                UPDATE rates
                SET basecurrencyid = ?,
                    targetcurrencyid = ?,
                    rate = ?
                WHERE id = ?;
                """,
                (dto.basecurrencyid, dto.targetcurrencyid, dto.rate, dto.id))

    def update_rate(self, dto: RatesDTO):
        with sqlite3.connect(self.database) as conn:
            with conn:
                cur = conn.cursor()
                cur.execute("""
                UPDATE rates
                SET rate = ?
                WHERE id = ?;
                """,
                (dto.rate, dto.id))
    
    def delete(self, id: int):
        with sqlite3.connect(self.database) as conn:
            with conn:
                cur = conn.cursor()
                cur.execute("""
                    DELETE FROM rates
                    WHERE id = ?;
                """,
                (id,))