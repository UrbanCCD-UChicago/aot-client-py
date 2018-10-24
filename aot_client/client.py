from typing import Union

import requests

from aot_client.filters import F
from aot_client.responses import Response, PagedResponse


class AotClient:
  """
  The ``AotClient`` is the tool used to access data from the
  Array of Things API. It provides abstracted methods to
  either list data or get detailed information about metadata
  entities.

  The responses of the various methods are either a basic
  ``Response`` (in the case of a detail request) or a 
  ``PagedResponse`` (in the case of a list request). The main
  difference between the two is that the paged responses
  provide an iteration abstraction.

  .. example::

  >>> from aot_client import AotClient
  >>> client = AotClient()
  >>> 
  >>> chicago = AotClient.get_project_details('chicago')
  >>> chicago.data
  {
    name: 'Chicago',
    slug: 'chicago', ...
  }
  >>> 
  >>> dataset = AotClient.list_observations()
  >>> for page in dataset:
  ...   do_something_with(page.data)
  """

  def __init__(self, hostname: str='https://api.arrayofthings.org/api'):
    """Instantiates a new instance of ``AotClient``

    :param hostame: The full URL path to the API
    """
    self._hostname = hostname

  def __str__(self) -> str:
    return self._hostname

  def __repr__(self) -> str:
    return f'<AotClient {self}>'

  def list_projects(self, filters: F=None) -> PagedResponse:
    """Returns a ``PagedResponse`` object with a list of *project*
    metadata records. Projects are the highest level in the hierarchy
    of system. 
    
    See the `API documentation`_ for details on the system design.

    .. _API documentation: https://api.arrayofthings.org/docs

    :param filters: Query parameters applied to the request
    """
    return self._send_request(f'{self._hostname}/projects', filters=filters)

  def get_project_details(self, slug) -> Response:
    return self._send_request(f'/projects/{slug}', paged=False)

  def list_nodes(self, filters: F=None) -> PagedResponse:
    """Returns a ``PagedResponse`` object with a list of *node*
    metadata records. Nodes are the physical instruments deployed
    with sensors to record observations. 
    
    See the `API documentation`_ for details on the system design.

    .. _API documentation: https://api.arrayofthings.org/docs

    :param filters: Query parameters applied to the request
    """
    return self._send_request(f'{self._hostname}/nodes', filters=filters)

  def get_node_details(self, vsn) -> Response:
    return self._send_request(f'/nodes/{vsn}', paged=False)
    
  def list_sensors(self, filters: F=None) -> PagedResponse:
    """Returns a ``PagedResponse`` object with a list of *sensor*
    metadata records. Sensors are the components onboard nodes. They
    are the things that record observations.
    
    See the `API documentation`_ for details on the system design.

    .. _API documentation: https://api.arrayofthings.org/docs

    :param filters: Query parameters applied to the request
    """
    return self._send_request(f'{self._hostname}/sensors', filters=filters)

  def get_sensor_details(self, path) -> Response:
    return self._send_request(f'/sensors/{path}', paged=False)

  def list_observations(self, filters: F=None) -> PagedResponse:
    """Returns a ``PagedResponse`` object with a list of *observations*.
    Observations are the data collected by the sensors.
    
    See the `API documentation`_ for details on the system design.

    .. _API documentation: https://api.arrayofthings.org/docs

    :param filters: Query parameters applied to the request
    """
    return self._send_request(f'{self._hostname}/observations', filters=filters)

  def list_raw_observations(self, filters: F=None) -> PagedResponse:
    """Returns a ``PagedResponse`` object with a list of 
    *raw observations*. Raw observations are similar to regular
    observations, however they contain the untested machine value
    for the observation data point and *maybe* the cleaned/translated
    value.
    
    See the `API documentation`_ for details on the system design.

    .. _API documentation: https://api.arrayofthings.org/docs

    :param filters: Query parameters applied to the request
    """
    return self._send_request(f'{self._hostname}/raw-observations',  filters=filters)

  def _send_request(self, endpoint: str, paged: bool=True, filters: F=None) -> Union[Response, PagedResponse]:
    if filters:
      params = filters.to_query_params()
    else:
      params = []

    response = requests.get(endpoint, params)

    if paged:
      return PagedResponse(payload=response.json(), client=self)
    else:  
      return Response(payload=response.json())