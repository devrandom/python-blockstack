from .resources.wallet import Wallets
from .util import UNSET_TIMEOUT

__author__ = 'devrandom'


class BlockstackClient(object):
    def __init__(self, account=None, token=None, base_uri=None, timeout=UNSET_TIMEOUT):
        """
        :param account: TBD
        :param token: TBD
        :param base_uri: base URL - e.g. https://test1.blockstack.io/api .  Omit trailing slash.
        """
        self.base_uri = base_uri
        self.auth = None
        # (account, token)
        self.wallets = Wallets(self.base_uri, self.auth, timeout)
