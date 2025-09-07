import sqlite3


class DaoRates():
    def __init__(self):
        pass

    def create_table():
        with sqlite3.connect('bd.sql') as conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE rates(
                id INT AUTO_INCREMENT PRIMARY KEY,
                basecurrenceid VARCHAR(30),
                targetcurrenceid VARCHAR(30),
                rate DECIMAL(6)               
                );
                """)