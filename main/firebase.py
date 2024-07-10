from firebase_admin import db
from main.api import get_blockchain_data, serialize_blockchain

def sync_blockchain_to_firebase():
    firebase_ref = db.reference('/blockchain')  
    blockchain_data = get_blockchain_data()
    serialized_data = serialize_blockchain(blockchain_data)
    firebase_ref.set(serialized_data)
    return serialized_data