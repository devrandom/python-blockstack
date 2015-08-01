import os
from blockstack.client import BlockstackClient
import time
from blockstack.util import BlockstackRestException

for i in range(100):
    name = "w%02d" % (i,)
    print(name)
    token = os.environ.get('BK_TOKEN')
    client = BlockstackClient(base_uri=('%s/api' % os.environ['BK_INSTANCE']), token=token)
    try:
        wallet = client.wallets.create(name, 'correct battery ' + name)
        print(wallet.balances)
    except BlockstackRestException as e:
        if e.code != 'duplicate':
            raise e
