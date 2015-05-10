from ..resources.base import ListResource, InstanceResource

__author__ = 'devrandom'


class Wallet(InstanceResource):
    pass


class Wallets(ListResource):
    instance = Wallet
    name = 'wallets'
    instance_suffix = 'info'

    def __init__(self, *args, **kwargs):
        super(Wallets, self).__init__(*args, **kwargs)

