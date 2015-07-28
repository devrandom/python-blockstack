import os
from blockstack.client import BlockstackClient

name = 'T5'
token = os.environ.get('BK_TOKEN')
client = BlockstackClient(base_uri=('%s/api' % os.environ['BK_INSTANCE']), token=token)
blue = client.wallets.get('Blue')
issuer = client.issuer
asset = issuer.assets.create('Blue', 'T5', 1000)
print(asset)
asset = blue.assets.get('T5')
print(asset.amount)
