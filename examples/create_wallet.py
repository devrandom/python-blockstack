import os
from blockstack.client import BlockstackClient
import time

name = 'Aqua'
token = os.environ.get('BK_TOKEN')
client = BlockstackClient(base_uri=('%s/api' % os.environ['BK_INSTANCE']), token=token)
aqua = client.wallets.create(name, 'correct battery ' + name)
print(aqua.balances)
time.sleep(1)
aqua = client.wallets.get(name)
print(aqua.balances)
