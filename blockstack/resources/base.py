import json
import logging
import platform
# noinspection PyUnresolvedReferences
from six.moves.urllib.parse import urlencode, urlparse, parse_qs
from requests import Session, Request
from six import iteritems, integer_types, binary_type, string_types
from ..util import UNSET_TIMEOUT, BlockstackRestException, BlockstackException
from ..version import __version__

__author__ = 'devrandom'

logger = logging.getLogger('blockstack')


def transform_params(parameters):
    transformed_parameters = {}

    for key, value in iteritems(parameters):
        if value is not None:
            transformed_parameters[key] = value

    return transformed_parameters


def _make_request(method, url, params=None, data=None, headers=None,
                 auth=None, timeout=None,
                 allow_redirects=False):
    """Sends an HTTP request
    :param str method: The HTTP method to use
    :param str url: The URL to request
    :param dict params: Query parameters to append to the URL
    :param dict data: Parameters to go in the body of the HTTP request
    :param dict headers: HTTP Headers to send with the request
    :param float timeout: Socket/Read timeout for the request
    :return: An http response
    :rtype: A :class:`Response <requests.Response>` object
    See the requests documentation for explanation of all these parameters
    """
    session = Session()

    def encode_atom(atom):
        if isinstance(atom, (integer_types, binary_type)):
            return atom
        elif isinstance(atom, string_types):
            return atom.encode('utf-8')
        else:
            raise ValueError('list elements should be an integer, '
                             'binary, or string')

    if data is not None:
        data = json.dumps(data)

    if params is not None:
        enc_params = urlencode(params, doseq=True)
        if urlparse(url).query:
            url = '%s&%s' % (url, enc_params)
        else:
            url = '%s?%s' % (url, enc_params)

    req = Request(method, url, data=data, headers=headers, auth=auth)

    prepped = session.prepare_request(req)
    resp = session.send(prepped, timeout=timeout)
    return resp


def make_request(method, uri, **kwargs):
    """
    Make a request to a Blockstack instance. Throws an error
    :return: a requests-like HTTP response
    :rtype: :class:`RequestsResponse`
    :raises BlockstackRestException: if the response is a 400
        or 500-level response.
    """
    headers = kwargs.get("headers", {})

    user_agent = "blostack-python/%s (Python %s)" % (
        __version__,
        platform.python_version(),
    )
    headers["User-Agent"] = user_agent
    headers["Accept-Charset"] = "utf-8"

    if method == "POST" and "Content-Type" not in headers:
        headers["Content-Type"] = "application/json"

    kwargs["headers"] = headers

    if "Accept" not in headers:
        headers["Accept"] = "application/json"

    resp = _make_request(method, uri, **kwargs)

    if not resp.ok:
        try:
            error = json.loads(resp.content)
            code = error["code"]
            message = error["message"]
        except:
            code = None
            message = resp.content

        raise BlockstackRestException(status=resp.status_code, method=method,
                                      uri=resp.url, msg=message, code=code)

    return resp


class Resource(object):
    """A REST Resource"""

    name = "Resource"

    def __init__(self, base_uri, auth, timeout=UNSET_TIMEOUT):
        self.base_uri = base_uri
        self.auth = auth
        self.timeout = timeout

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.__dict__ == other.__dict__)

    def __hash__(self):
        return hash(frozenset(self.__dict__))

    def __ne__(self, other):
        return not self.__eq__(other)

    def request(self, method, uri, **kwargs):
        """
        Send an HTTP request to the resource.
        :raises: a :exc:`~blockstack.BlockstackRestException`
        """
        if 'timeout' not in kwargs and self.timeout is not UNSET_TIMEOUT:
            kwargs['timeout'] = self.timeout

        resp = make_request(method, uri, auth=self.auth, **kwargs)

        logger.debug(resp.content)

        if method == "DELETE":
            return resp, {}
        else:
            return resp, resp.json()

    @property
    def uri(self):
        fmt = (self.base_uri, self.name)
        return "%s/%s" % fmt


class InstanceResource(Resource):
    """ The object representation of an instance response from the Blockstack API
    """

    subresources = []
    id_key = "id"
    use_json_extension = True

    def __init__(self, parent, id):
        """
            :param parent: The parent list class for this instance resource.
            For example, the parent for a :class:`~blockstack.resources.Wallet`
            would be a :class:`~blockstack.resources.Wallets` object.
            :type parent: :class:`~blockstack.resources.ListResource`
            :param str id: The unique identifier for this instance
        """
        self.parent = parent
        self.name = id
        super(InstanceResource, self).__init__(
            parent.uri,
            parent.auth,
            parent.timeout
        )

    def load_subresources(self):
        """
        Load all subresources
        """
        for resource in self.subresources:
            list_resource = resource(
                self.uri,
                self.parent.auth,
                self.parent.timeout
            )
            self.__dict__[list_resource.key] = list_resource

    def load(self, entries):
        self.__dict__.update(entries)

    def update_instance(self, **kwargs):
        """ Make a POST request to the API to update an object's properties
        :return: None, this is purely side effecting
        :raises: a :class:`~blockstack.util.BlockstackRestException` on failure
        """
        a = self.parent.update(self.name, **kwargs)
        self.load(a.__dict__)

    def delete_instance(self):
        """ Make a DELETE request to the API to delete the object
        :return: None, this is purely side effecting
        :raises: a :class:`~twilio.rest.RestException` on failure
        """
        return self.parent.delete(self.name)

    def __str__(self):
        return "<%s %s>" % (self.__class__.__name__, self.name[0:5])


class ListResource(Resource):
    name = "Resources"
    instance = InstanceResource
    instance_suffix = None

    def __init__(self, *args, **kwargs):
        super(ListResource, self).__init__(*args, **kwargs)

    @property
    def key(self):
        return self.name.lower()

    def get(self, id):
        """ Get an instance resource by its id
        Usage:
        .. code-block:: python
            message = client.wallets.get("alice")
            print message.body
        :rtype: :class:`~blockstack.resources.InstanceResource`
        """
        return self.get_instance(id)

    def get_instance(self, id):
        """Request the specified instance resource"""
        if self.instance_suffix:
            uri = "%s/%s/%s" % (self.uri, id, self.instance_suffix)
        else:
            uri = "%s/%s" % (self.uri, id)
        resp, item = self.request("GET", uri)
        if self.instance.id_key not in item:
            item[self.instance.id_key] = id
        return self.load_instance(item)

    def get_instances(self, params):
        """
        Query the list resource for a list of InstanceResources.
        Raises a :exc:`~twilio.TwilioRestException` if requesting a page of
        results that does not exist.
        :param dict params: List of URL parameters to be included in request
        """
        resp, page = self.request("GET", self.uri, params=params)

        return [self.load_instance(ir) for ir in page]

    def create_instance(self, body):
        """
        Create an InstanceResource via a POST to the List Resource
        :param dict body: Dictionary of POST data
        """
        resp, instance = self.request("POST", self.uri,
                                      data=transform_params(body))

        if resp.status_code not in (200, 201):
            raise BlockstackRestException(resp.status_code,
                                          self.uri, "Resource not created")

        return self.load_instance(instance)

    def delete_instance(self, sid):
        """
        Delete an InstanceResource via DELETE
        body: string -- HTTP Body for the quest
        """
        uri = "%s/%s" % (self.uri, sid)
        resp, instance = self.request("DELETE", uri)
        return resp.status_code == 204

    def update_instance(self, sid, body):
        """
        Update an InstanceResource via a POST
        sid: string -- String identifier for the list resource
        body: dictionary -- Dict of items to POST
        """
        uri = "%s/%s" % (self.uri, sid)
        resp, entry = self.request("POST", uri, data=transform_params(body))
        return self.load_instance(entry)

    def iter(self, **kwargs):
        """ Return all instance resources using an iterator
        This will fetch a page of resources from the API and yield them in
        turn. When the page is exhausted, this will make a request to the API
        to retrieve the next page. Hence you may notice a pattern - the library
        will loop through 50 objects very quickly, but there will be a delay
        retrieving the 51st as the library must make another request to the API
        for resources.
        Example usage:
        .. code-block:: python
            for message in client.messages:
                print message.sid
        """
        params = transform_params(kwargs)

        while True:
            resp, page = self.request("GET", self.uri, params=params)

            # FIXME
            if self.key not in page:
                raise StopIteration()

            for ir in page[self.key]:
                yield self.load_instance(ir)

            if not page.get('next_page_uri', ''):
                raise StopIteration()

            o = urlparse(page['next_page_uri'])
            params.update(parse_qs(o.query))

    def load_instance(self, data):
        instance = self.instance(self, data[self.instance.id_key])
        instance.load(data)
        instance.load_subresources()
        return instance

    def __str__(self):
        return '<%s (%s)>' % (self.__class__.__name__, self.count())

    def list(self, **kw):
        """Query the list resource for a list of InstanceResources.
        :param int page: The page of results to retrieve (most recent at 0)
        :param int page_size: The number of results to be returned.
        """
        return self.get_instances(kw)
