import tkinter as tk
import time
import threading
from database import create_tables, get_balance, update_balance

# Initialize database
create_tables()

coins_per_second = 1  # mining rate

def mine():
    while True:
        time.sleep(1)
        update_balance(coins_per_second)

def update_gui():
    balance = get_balance()
    coin_label.config(text=f"Balance: {balance:.2f} GeoCoins")
    usd_label.config(text=f"USD Value: ${balance * 0.01:.2f}")  # Example: 1 GeoCoin = $0.01
    root.after(1000, update_gui)

# GUI Setup
root = tk.Tk()
root.title("GeoCoin Miner")

coin_label = tk.Label(root, text="Balance: 0 GeoCoins", font=("Arial", 16))
coin_label.pack(pady=10)

usd_label = tk.Label(root, text="USD Value: $0.00", font=("Arial", 14))
usd_label.pack(pady=10)

# Start mining in background
t = threading.Thread(target=mine, daemon=True)
t.start()

# Update GUI loop
update_gui()
root.mainloop()
