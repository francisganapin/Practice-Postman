import sqlite3

conn = sqlite3.connect('sales.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT,
    quantity INTEGER,
    price REAL,
    sale_date TEXT
)
''')
c.executemany('''
INSERT INTO sales (item, quantity, price, sale_date)
VALUES (?, ?, ?, ?)
''', [
    ("apple", 2, 3.00, "2024-06-01"),
    ("orange", 4, 6.00, "2024-06-01"),
    ("banana", 3, 4.50, "2024-06-02"),
])
conn.commit()
conn.close()