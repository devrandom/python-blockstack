from blockstack.client import BlockstackClient

client = BlockstackClient(base_uri='http://localhost:8080/api')
alice = client.wallets.get('Blue')
bob = client.wallets.get('Red')
alice_oracle = client.oracles.get('Blue')
bob_oracle = client.oracles.get('Red')

alice_txs = alice.transactions
bob_txs = bob.transactions

send = alice_txs.create(asset='TRY', address=bob.assetAddress, amount=1)
print(send)
