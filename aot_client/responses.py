class Response:
    """
    A basic API request response used for endpoints that return a
    single record -- namely the detail specs.

    .. example::

    >>> from aot_client import AotClient
    >>> client = AotClient()
    >>> chicago = AotClient.get_project_details('chicago')
    >>> chicago.data
    {
      name: 'Chicago',
      slug: 'chicago',
      ...
    }
    """

    def __init__(self, payload: dict):
        """Initializes a new instance of ``Response``.

        :param payload: The response JSON
        """
        self._payload = payload
        self._data = payload['data']

    @property
    def data(self) -> dict:
        return self._data


class PagedResponse:
    """
    An API request response used for endpoints that return a
    list of records. This is used to help page through the data.

    .. example::

    >>> from aot_client import AotClient
    >>> client = AotClient()
    >>> dataset = AotClient.list_observations()
    >>> for page in dataset:
    ...   do_something_with(page.data)
    """

    def __init__(self, payload: dict, client: 'AotClient'):
        """Instantiates a new instance of ``PagedResponse``.

        :param payload: The reponse JSON
        :param client: The instance of ``AotClient`` that made the request
        """
        self._payload = payload
        self._meta = payload['meta'] if 'meta' in payload else None
        self._data = payload['data']
        self._client = client

    def __iter__(self) -> 'PagedResponse':
        while True:
            yield self

            refreshed = self._client._send_request(self.next_link)
            if len(refreshed.data) == 0:  # NOQA
                break
            else:
                self = refreshed

        return  # NOQA

    @property
    def data(self) -> dict:
        return self._data

    @property
    def previous_link(self) -> str:
        return self._meta['links']['previous']

    @property
    def current_link(self) -> str:
        return self._meta['links']['current']

    @property
    def next_link(self) -> str:
        return self._meta['links']['next']
