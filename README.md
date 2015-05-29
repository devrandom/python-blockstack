[![Build Status](https://travis-ci.org/devrandom/python-blockstack.svg?branch=master)](https://travis-ci.org/devrandom/python-blockstack)

Blockstack API (https://blockstack.io/)

## Examples


```python
    from blockstack.client import BlockstackClient
    token = YOUR_API_TOKEN
    client = BlockstackClient(base_uri='https://XXX.blockstack.io/', token=token)
    alice = client.wallets.get('alice')
    bob = client.wallets.get('bob')
    print(alice.__dict__.keys())
    print(alice.currentAddress)
    print(alice.currentHeight)
```

```
    dict_keys(['name', 'allBalances', 'currentAddress', 'auth', 'base_uri', 'id', 'transactions', 'currentHeight', 'parent', 'assetAddress', 'balances', 'timeout', 'netBalances'])
    ms9tDLTTqjQa7daCQHj39jjHdTU8AK4of3
    653
```


```python
    alice_txs = alice.transactions
    bob_txs = bob.transactions
    print([t.id for t in alice_txs.list()])
    partial = alice_txs.propose(atomic=True, asset='TRY', address=bob.assetAddress, amount=10000)
    complete = bob_txs.create(atomic=True, asset='USD', address=alice.assetAddress, amount=100, transaction=partial['transaction'])
    signed1 = client.oracles.get('alice').sign(complete.id, complete.transaction)
    committed = client.oracles.get('bob').broadcast(complete.id, signed1.transaction) # sign and broadcast
```

```
    ['1f5381760c56f89b0a35dd6ae5c4ee6a6fb0941f72a27c6fed786cf0829c31bb', '9d2fe8946d0d1575972f0c3181fbfdf22e5e411e1f96ab0e44302245ca510bac', '26b3af7a30f552e2af83d3052ea33a51664ccc3d7dd589d27d58daffadfab6ae', '820364378b7f75f26f77e640167aa1e5ccba9e46b92b977027f547bc6a116443', 'ab99b8b7531592bd3585f2c6c0293e8fe1f952f69558efe44b1ad569329b7272']
```



```python
    tx = alice_txs.get(committed.id)
    print(tx.id)
    print(tx.changes)
```

```
    41a5b967732826d37768c588336b5e3ab5a0c4814885a0fb5b924f4dcd9324e2
    {'USD': 100, 'TRY': -10000, 'Tokens': -20287}
```
