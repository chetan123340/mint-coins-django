from main.models import Block, Transaction


def get_blockchain_data():
    blocks = Block.objects.all()
    blockchain_data = []
    for block in blocks:
        block_data = {
            'index': block.index,
            'miner': block.miner.username,
            'prev_hash': block.prev_hash,
            'hash': block.hash,
            'timestamp': block.timestamp.isoformat(),
            'transactions': serialize_transactions(block.transactions.all()),
            'no_of_transactions': block.no_of_transactions,
            'nonce': block.nonce,
            'difficulty': block.difficulty,
            'block_reward': block.block_reward,
            'block_size': block.block_size,
        }
        blockchain_data.append(block_data)
    
    return blockchain_data

def serialize_transactions(transactions):
    # Serialize each transaction
    serialized_transactions = []
    for transaction in transactions:
        transaction_data = {
            'sender': transaction.sender.username,
            'reciever': transaction.reciever.username,
            'amount': transaction.amount,
            'timestamp': transaction.timestamp.isoformat(),
            'signature': transaction.signature,
            'confirmed': transaction.confirmed,
            'hash': transaction.hash,
        }
        serialized_transactions.append(transaction_data)
    
    return serialized_transactions

def serialize_blockchain(blockchain_data):
    return blockchain_data
