from ..resources.base import ListResource, InstanceResource

__author__ = 'devrandom'


class OracleTransaction(InstanceResource):
    pass


class OracleTransactions(ListResource):
    instance = OracleTransaction
    name = 'transactions'

    def __init__(self, *args, **kwargs):
        super(OracleTransactions, self).__init__(*args, **kwargs)

    def sign(self, tx_id, transaction, **kwargs):
        kwargs['transaction'] = transaction
        return self.update_instance(tx_id, kwargs)

    def broadcast(self, tx_id, transaction, **kwargs):
        kwargs['broadcast'] = True
        kwargs['transaction'] = transaction
        return self.update_instance(tx_id, kwargs)


class Oracle(InstanceResource):
    subresources = [OracleTransactions]


class Oracles(ListResource):
    instance = Oracle
    name = 'oracles'

    def __init__(self, *args, **kwargs):
        super(Oracles, self).__init__(*args, **kwargs)


