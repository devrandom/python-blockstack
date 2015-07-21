from blockstack.util import BlockstackRestException
from ..resources.base import ListResource, InstanceResource, transform_params, Resource

__author__ = 'devrandom'


class IssuerAsset(InstanceResource):
    id_key = 'name'


class IssuerAssets(ListResource):
    instance = IssuerAsset
    name = 'assets'

    def __init__(self, *args, **kwargs):
        super(IssuerAssets, self).__init__(*args, **kwargs)

    def create(self, wallet, name, amount, metadata=None, **kwargs):
        if not metadata:
            metadata = {}
        kwargs['wallet'] = wallet
        kwargs['name'] = name
        kwargs['amount'] = amount
        kwargs['metadata'] = metadata
        return self.create_instance(kwargs)


class Issuer(Resource):
    def __init__(self, uri, auth, timeout, *args, **kwargs):
        super(Issuer, self).__init__(uri + "/issuer", auth, timeout, *args, **kwargs)
        self.assets = IssuerAssets(self.base_uri, self.auth, timeout)

