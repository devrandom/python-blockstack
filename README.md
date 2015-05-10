[![Build Status](https://travis-ci.org/devrandom/python-blockstack.svg?branch=master)](https://travis-ci.org/devrandom/python-blockstack)

https://blockstack.io/ API

Examples
===

```python
    from blockstack.client import BlockstackClient
    client = BlockstackClient(base_uri='http://localhost:8080/api')
    alice = client.wallets.get('alice')
    print(alice.__dict__.keys())
    print(alice.currentAddress)
    print(alice.currentHeight)
```

    dict_keys(['allBalances', 'balances', 'auth', 'id', 'netBalances', 'parent', 'base_uri', 'timeout', 'assetAddress', 'name', 'currentAddress', 'currentHeight'])
    ms9tDLTTqjQa7daCQHj39jjHdTU8AK4of3
    649

