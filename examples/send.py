import os
from blockstack.client import BlockstackClient

token = os.environ.get('BK_TOKEN')
client = BlockstackClient(base_uri=('%s/api' % os.environ['BK_INSTANCE']), token=token)
alice = client.wallets.get('Blue')
bob = client.wallets.get('Red')
alice_oracle = client.oracles.get('Blue')
bob_oracle = client.oracles.get('Red')

alice_txs = alice.transactions
bob_txs = bob.transactions

send = alice_txs.create(asset='TRY', address=bob.assetAddress, amount=1)
print(send)
