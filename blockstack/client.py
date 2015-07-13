import requests
from blockstack.resources.oracle import Oracles
from .resources.wallet import Wallets
from .util import UNSET_TIMEOUT

__author__ = 'devrandom'


class MyAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['X-Blockstack-Auth'] = self.token
        return r

class BlockstackClient(object):
    def __init__(self, account=None, token=None, base_uri=None, timeout=UNSET_TIMEOUT):
        """
        :param account: TBD
        :param token: API token
        :param base_uri: base URL - e.g. https://test1.blockstack.io/api .  Omit trailing slash.
        """
        self.base_uri = base_uri
        self.auth = None
        if token:
            self.auth = MyAuth(token)
        self.wallets = Wallets(self.base_uri, self.auth, timeout)
        self.oracles = Oracles(self.base_uri, self.auth, timeout)
