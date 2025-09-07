import sqlite3


class DaoCurrencies():
    def __init__(self):
        pass

    def create_table():
        with sqlite3.connect('bd.sql') as conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE currency(
                id INT AUTO_INCREMENT PRIMARY KEY, 
                code VARCHAR(30),
                fullname VARCHAR(30),
                sing VARCHAR(5)             
                );
                """)