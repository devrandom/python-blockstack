from blockstack.client import BlockstackClient
from unittest.mock import MagicMock
import unittest

__author__ = 'devrandom'


class WalletTest(unittest.TestCase):
    def setUp(self):
        self.client = BlockstackClient(base_uri='https://test.blockstack.io/api')

    def testWalletUri(self):
        wallets = self.client.wallets
        self.assertEquals('https://test.blockstack.io/api/wallets', wallets.uri)
        wallets.request = MagicMock(return_value=(object(), {'id': 'alice'}))
        wallet = wallets.get('alice')
        wallets.request.assert_called_with('GET', 'https://test.blockstack.io/api/wallets/alice/info')
        self.assertEqual('alice', wallet.id)