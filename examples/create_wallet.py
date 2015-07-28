from blockstack.client import BlockstackClient
from blockstack.util import BlockstackRestException
import time

name = 'Aqua'
client = BlockstackClient(base_uri='http://localhost:8080/api')
aqua = client.wallets.create(name, 'correct battery ' + name)
print(aqua.balances)
time.sleep(1)
aqua = client.wallets.get(name)
print(aqua.balances)
