import sqlite3

DATABASE = 'phones.db'


def get_db_connections():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connections()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS phones(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL )

        """)
    conn.commit()
    conn.close()

def create_table_category():
    conn = get_db_connections()