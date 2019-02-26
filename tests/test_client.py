import pytest
from requests.exceptions import HTTPError

from aot_client import AotClient
from aot_client.responses import Response, PagedResponse


def test_list_projects():
    client = AotClient()
    res = client.list_projects()
    assert isinstance(res, PagedResponse)


def test_get_project_details():
    client = AotClient()
    res = client.get_project_details('chicago')
    assert isinstance(res, Response)


def test_get_project_doesnt_exist():
    client = AotClient()
    with pytest.raises(HTTPError): 
        res = client.get_project_details('nowhere')


def test_list_nodes():
    client = AotClient()
    res = client.list_nodes()
    assert isinstance(res, PagedResponse)


def test_get_node_details():
    client = AotClient()
    res = client.get_node_details('004')
    assert isinstance(res, Response)


def test_list_sensors():
    client = AotClient()
    res = client.list_sensors()
    assert isinstance(res, PagedResponse)


def test_get_sensor_details():
    client = AotClient()
    res = client.get_sensor_details('chemsense.co.concentration')
    assert isinstance(res, Response)


def test_list_observations():
    client = AotClient()
    res = client.list_observations()
    assert isinstance(res, PagedResponse)
