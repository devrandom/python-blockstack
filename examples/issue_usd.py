import os

from blockstack.client import BlockstackClient
import time

token = os.environ.get('BK_TOKEN')
client = BlockstackClient(base_uri=('%s/api' % os.environ['BK_INSTANCE']), token=token)
issuer = client.wallets.get('issuer')
alice = client.wallets.get('alice')
client.issuer.assets.create('issuer', 'USD', 1000000, metadata={"divisibility": 2})
time.sleep(2)
issuer.transactions.create(asset='USD', address=alice.assetAddress, amount=1)
