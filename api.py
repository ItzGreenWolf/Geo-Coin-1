from flask import Flask, request, jsonify
from blockchain import Blockchain
from wallets import Wallet
from miner_app import Miner
from database import Database

# Initialize database and blockchain
db = Database("geocoin.db")
blockchain = Blockchain(db)
miner = Miner(blockchain)

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "GeoCoin Node Online 🚀"})

@app.route('/wallet/create', methods=['POST'])
def create_wallet():
    wallet = Wallet()
    wallet.save_to_db(db)
    return jsonify({"address": wallet.address, "private_key": wallet.private_key})

@app.route('/wallet/balance/<address>', methods=['GET'])
def get_balance(address):
    balance = blockchain.get_balance(address)
    return jsonify({"address": address, "balance": balance})

@app.route('/transaction', methods=['POST'])
def create_transaction():
    data = request.get_json()
    sender = data['sender']
    recipient = data['recipient']
    amount = data['amount']

    tx = blockchain.add_transaction(sender, recipient, amount)
    return jsonify(tx)

@app.route('/mine', methods=['POST'])
def mine_block():
    block = miner.mine()
    return jsonify(block)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
