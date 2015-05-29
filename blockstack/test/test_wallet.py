from collections import namedtuple
from blockstack.client import BlockstackClient
from mock import MagicMock
import unittest

__author__ = 'devrandom'


MockResponse = namedtuple('MockResponse', 'status_code')


class WalletTest(unittest.TestCase):
    def setUp(self):
        self.client = BlockstackClient(base_uri='https://test.blockstack.io/api')

    def testWalletUri(self):
        wallets = self.client.wallets
        self.assertEquals('https://test.blockstack.io/api/wallets', wallets.uri)
        wallets.request = MagicMock(return_value=(object(), {'id': 'alice'}))
        wallet = wallets.get('alice')
        wallets.request.assert_called_with('GET', 'https://test.blockstack.io/api/wallets/alice')
        self.assertEqual('alice', wallet.id)

    def testTransactionsUri(self):
        wallets = self.client.wallets
        wallets.request = MagicMock(return_value=(object(), {'id': 'alice'}))
        wallet = wallets.get('alice')
        self.assertEquals('https://test.blockstack.io/api/wallets/alice/transactions', wallet.transactions.uri)
        wallet.transactions.request = MagicMock(return_value=(object(), [{'id': 'abcd'}]))
        txs = wallet.transactions.list()
        wallet.transactions.request.assert_called_with('GET',
                                                       'https://test.blockstack.io/api/wallets/alice/transactions',
                                                       params={})
        self.assertEqual(1, len(txs))
        self.assertEqual('abcd', txs[0].id)

    def testProposeTransaction(self):
        wallets = self.client.wallets
        wallets.request = MagicMock(return_value=(object(), {'id': 'alice'}))
        wallet = wallets.get('alice')
        wallet.transactions.request = MagicMock(return_value=(MockResponse(200), {'transaction': 'ffff'}))
        params = {"asset": "TRY",
                  "address": "a1",
                  "amount": 1000,
                  "atomic": True}
        result = wallet.transactions.propose(**params)
        wallet.transactions.request.assert_called_with('POST',
                                                       'https://test.blockstack.io/api/wallets/alice/transactions',
                                                       data=params)
        self.assertEqual(result['transaction'], 'ffff')

    def testCreateTransaction(self):
        wallets = self.client.wallets
        oracles = self.client.oracles
        wallets.request = MagicMock(return_value=(object(), {'id': 'alice'}))
        oracles.request = MagicMock(return_value=(object(), {'id': 'alice'}))
        wallet = wallets.get('alice')
        wallet.transactions.request = MagicMock(return_value=(MockResponse(200), {'id': 'a1', 'transaction': 'eeee'}))
        other_params = {"asset": "USD",
                        "address": "b1",
                        "transaction": 'ffff',
                        "amount": 100,
                        "atomic": True}
        result = wallet.transactions.create(**other_params)
        wallet.transactions.request.assert_called_with('POST',
                                                       'https://test.blockstack.io/api/wallets/alice/transactions',
                                                       data=other_params)
        self.assertEqual(result.id, 'a1')
        oracle = oracles.get('alice')
        oracle.transactions.request = MagicMock(return_value=(MockResponse(200), {'id': 'a1', 'transaction': 'eeee'}))
        oracle.transactions.sign(result.id, result.transaction)
        oracle.transactions.request.assert_called_with('POST',
                                                       'https://test.blockstack.io/api/oracles/alice/transactions/a1',
                                                       data={'transaction': 'eeee'})

    def testAssets(self):
        wallets = self.client.wallets
        wallets.request = MagicMock(return_value=(object(), {'id': 'alice'}))
        wallet = wallets.get('alice')
        self.assertEquals('https://test.blockstack.io/api/wallets/alice/assets', wallet.assets.uri)
        wallet.assets.request = MagicMock(return_value=(object(), [{'name': 'abcd', 'amount': 100}]))
        assets = wallet.assets.list()
        wallet.assets.request.assert_called_with('GET',
                                                 'https://test.blockstack.io/api/wallets/alice/assets',
                                                 params={})
        self.assertEqual(1, len(assets))
        self.assertEqual('abcd', assets[0].name)

