import sqlite3

DB_NAME = "geocoin.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Table for balances
    c.execute('''CREATE TABLE IF NOT EXISTS balances (
                    id INTEGER PRIMARY KEY,
                    coins REAL
                )''')
    
    # Table for transactions
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    amount REAL,
                    type TEXT
                )''')
    
    # Start balance if not exists
    c.execute("SELECT * FROM balances WHERE id=1")
    if not c.fetchone():
        c.execute("INSERT INTO balances (id, coins) VALUES (1, 0)")
    
    conn.commit()
    conn.close()

def get_balance():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT coins FROM balances WHERE id=1")
    balance = c.fetchone()[0]
    conn.close()
    return balance

def update_balance(amount):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE balances SET coins = coins + ? WHERE id=1", (amount,))
    c.execute("INSERT INTO transactions (amount, type) VALUES (?, 'mined')", (amount,))
    conn.commit()
    conn.close()
