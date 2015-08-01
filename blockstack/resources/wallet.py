from blockstack.util import BlockstackRestException
from ..resources.base import ListResource, InstanceResource, transform_params

__author__ = 'devrandom'


class Transaction(InstanceResource):
    pass


class Transactions(ListResource):
    instance = Transaction
    name = 'transactions'

    def __init__(self, *args, **kwargs):
        super(Transactions, self).__init__(*args, **kwargs)

    def propose(self, atomic=False, **kwargs):
        kwargs['atomic'] = atomic
        resp, result = self.request("POST", self.uri,
                                    data=transform_params(kwargs))

        if resp.status_code not in (200, 201):
            raise BlockstackRestException(resp.status_code,
                                          self.uri, "Resource not proposed")
        return result

    def create(self, atomic=False, transaction=None, **kwargs):
        kwargs['atomic'] = atomic
        kwargs['transaction'] = transaction
        return self.create_instance(kwargs)


class Asset(InstanceResource):
    id_key = 'name'


class Assets(ListResource):
    instance = Asset
    name = 'assets'

    def __init__(self, *args, **kwargs):
        super(Assets, self).__init__(*args, **kwargs)


class Wallet(InstanceResource):
    subresources = [Transactions, Assets]


class Wallets(ListResource):
    instance = Wallet
    name = 'wallets'

    def listnames(self):
        resp, names = self.request("GET", self.uri)
        return names

    def create(self, name, mnemonic_phrase, **kwargs):
        kwargs['name'] = name
        kwargs['mnemonic'] = mnemonic_phrase
        return self.create_instance(kwargs)

    def __init__(self, *args, **kwargs):
        super(Wallets, self).__init__(*args, **kwargs)


