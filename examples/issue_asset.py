from blockstack.client import BlockstackClient
from blockstack.util import BlockstackRestException
import time

name = 'T5'
client = BlockstackClient(base_uri='http://localhost:8080/api')
blue = client.wallets.get('Blue')
issuer = client.issuer
asset = issuer.assets.create('Blue', 'T5', 1000)
print(asset)
asset = blue.assets.get('T5')
print(asset.amount)
