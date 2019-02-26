from aot_client import AotClient


def has_key(d, key):
    return key in d


def test_data_property():
    client = AotClient()
    res = client.get_project_details('chicago')
    
    assert isinstance(res.data, dict)
    assert has_key(res.data, 'name')
    assert has_key(res.data, 'slug')
    assert has_key(res.data, 'hull')
    assert has_key(res.data, 'archive_url')
