import tkinter as tk
import time
import threading
import requests

# Config
COIN_NAME = "GeoCoin"
COINS_PER_SECOND = 1
COIN_TO_USD = 0.55  # 1 GeoCoin = $0.55
API_URL = "http://127.0.0.1:5000/transaction"  # Flask API endpoint

# Replace these with your actual addresses later
SENDER_ADDRESS = "your_wallet_address"
RECIPIENT_ADDRESS = "recipient_address"

class GeoCoinMiner:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{COIN_NAME} Miner")

        self.start_time = None
        self.coins = 0
        self.running = False

        # Labels
        self.timer_label = tk.Label(root, text="Time: 0s", font=("Arial", 16))
        self.timer_label.pack(pady=10)

        self.coins_label = tk.Label(root, text=f"{COIN_NAME}: 0", font=("Arial", 16))
        self.coins_label.pack(pady=10)

        self.usd_label = tk.Label(root, text="USD: $0.00", font=("Arial", 16))
        self.usd_label.pack(pady=10)

        # Buttons
        self.start_button = tk.Button(root, text="Start Mining", command=self.start_mining, width=15, font=("Arial", 14))
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop Mining", command=self.stop_mining, width=15, font=("Arial", 14))
        self.stop_button.pack(pady=5)

    def start_mining(self):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            threading.Thread(target=self.mine_loop, daemon=True).start()

    def stop_mining(self):
        self.running = False

    def mine_loop(self):
        while self.running:
            elapsed = int(time.time() - self.start_time)
            self.coins += COINS_PER_SECOND
            usd_value = self.coins * COIN_TO_USD

            # Update GUI
            self.timer_label.config(text=f"Time: {elapsed}s")
            self.coins_label.config(text=f"{COIN_NAME}: {self.coins}")
            self.usd_label.config(text=f"USD: ${usd_value:.2f}")

            # Send mined coins to Flask API automatically
            self.send_to_blockchain(SENDER_ADDRESS, RECIPIENT_ADDRESS, COINS_PER_SECOND)

            time.sleep(1)

    def send_to_blockchain(self, sender, recipient, amount):
        data = {"sender": sender, "recipient": recipient, "amount": amount}
        try:
            response = requests.post(API_URL, json=data)
            if response.status_code != 200:
                print("Failed to send to blockchain:", response.text)
        except Exception as e:
            print("Could not connect to API:", e)

if __name__ == "__main__":
    root = tk.Tk()
    app = GeoCoinMiner(root)
    root.mainloop()
