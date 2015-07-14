from blockstack.client import BlockstackClient
from blockstack.util import BlockstackRestException
import time

client = BlockstackClient(base_uri='http://localhost:8080/api')
alice = client.wallets.get('Blue')
bob = client.wallets.get('Red')
alice_oracle = client.oracles.get('Blue')
bob_oracle = client.oracles.get('Red')
print(alice.currentAddress)
print("current height:", alice.currentHeight)

alice_txs = alice.transactions
bob_txs = bob.transactions
print(len(alice_txs.list()), "transactions in history for Blue")

sent = 0
while sent < 10:
    try:
        partial = alice_txs.propose(atomic=True, asset='TRY', address=bob.assetAddress, amount=1)
        complete = bob_txs.create(atomic=True, asset='USD', address=alice.assetAddress, amount=2, transaction=partial['transaction'])
        signed1 = alice_oracle.transactions.sign(complete.id, complete.transaction)
        committed = bob_oracle.transactions.broadcast(complete.id, signed1.transaction)
        print(committed)
        sent += 1
    except BlockstackRestException as e:
        if e.code == "insufficient":
            # We might have unconfirmed coins, try again.
            # Note - in normal operations we will have coins for a variety of assets, so waiting for unconfirmed coins
            # will be relatively rare.  But in this contrived example, we transact in the same asset repeatedly and we
            # are not optimizing for coin availability.
            time.sleep(0.4)
        else:
            print(e)
            break
