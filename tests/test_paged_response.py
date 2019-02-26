from aot_client import AotClient, F


def test_data_property():
    client = AotClient()
    res = client.list_observations()

    assert isinstance(res.data, list)
    for record in res.data:
        assert isinstance(record, dict)


def test_previous_link_property():
    client = AotClient()
    res = client.list_observations(filters=F('page', '2'))

    assert isinstance(res.previous_link, str)


def test_current_link_property():
    client = AotClient()
    res = client.list_observations(filters=F('page', '2'))

    assert isinstance(res.current_link, str)


def test_next_link_property():
    client = AotClient()
    res = client.list_observations(filters=F('page', '2'))

    assert isinstance(res.next_link, str)


def test_iter():
    client = AotClient()
    dataset = client.list_observations(filters=F('size', 1))

    i = 0
    for page in dataset:
            i += 1
            if i >= 5:
                break
