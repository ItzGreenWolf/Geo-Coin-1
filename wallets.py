from ecdsa import SigningKey, SECP256k1
import json

class Wallet:
    def __init__(self):
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()

    def get_address(self):
        return self.public_key.to_string().hex()

    def sign_transaction(self, transaction_data):
        tx_json = json.dumps(transaction_data, sort_keys=True).encode()
        return self.private_key.sign(tx_json).hex()
