import sqlite3

conn = sqlite3.connect("product_trace.db", check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    batch TEXT,
    temp REAL,
    weight REAL,
    size REAL,
    label TEXT
)''')
conn.commit()

def insert_product(name, batch, temp, weight, size, label):
    c.execute("INSERT INTO products (name, batch, temp, weight, size, label) VALUES (?, ?, ?, ?, ?, ?)",
              (name, batch, temp, weight, size, label))
    conn.commit()

def get_all_products():
    c.execute("SELECT * FROM products")
    return c.fetchall()