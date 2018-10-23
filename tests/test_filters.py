from aot_client import F


def test_empty_init():
    f = F()
    assert f.filters == {}


def test_tuple_init():
    f = F('age', 'gt', 21)
    assert f.filters == {
        'age': [('gt', 21)]
    }


def test_iand_with_a_tuple():
    f = F()
    assert f.filters == {}

    f &= ('name', 'eq', 'vince')
    assert f.filters == {
        'name': [('eq', 'vince')]
    }

    f &= ('age', 'gt', 21)
    assert f.filters == {
        'name': [('eq', 'vince')],
        'age': [('gt', 21)]
    }

    f &= ('name', 'eq', 'bob')
    assert f.filters == {
        'name': [
            ('eq', 'vince'),
            ('eq', 'bob')
        ],
        'age': [('gt', 21)]
    }


def test_iand_with_another_filter():
    f = F()
    assert f.filters == {}

    f &= F('name', 'eq', 'vince')
    assert f.filters == {
        'name': [('eq', 'vince')]
    }

    f &= F('age', 'gt', 21)
    assert f.filters == {
        'name': [('eq', 'vince')],
        'age': [('gt', 21)]
    }

    f &= F('name', 'eq', 'bob')
    assert f.filters == {
        'name': [
            ('eq', 'vince'),
            ('eq', 'bob')
        ],
        'age': [('gt', 21)]
    }


def test_ior_with_a_tuple():
    f = F()
    assert f.filters == {}

    f |= ('name', 'eq', 'vince')
    assert f.filters == {
        'name': [('eq', 'vince')]
    }

    f |= ('age', 'gt', 21)
    assert f.filters == {
        'name': [('eq', 'vince')],
        'age': [('gt', 21)]
    }

    f |= ('name', 'eq', 'bob')
    assert f.filters == {
        'name': [('eq', 'bob')],
        'age': [('gt', 21)]
    }


def test_ior_with_another_filter():
    f = F()
    assert f.filters == {}

    f |= F('name', 'eq', 'vince')
    assert f.filters == {
        'name': [('eq', 'vince')]
    }

    f |= F('age', 'gt', 21)
    assert f.filters == {
        'name': [('eq', 'vince')],
        'age': [('gt', 21)]
    }

    f |= F('name', 'eq', 'bob')
    assert f.filters == {
        'name': [('eq', 'bob')],
        'age': [('gt', 21)]
    }


def test_to_query_params():
    f = F('name', 'eq', 'vince')
    assert f.to_query_params() == [
        ('name', 'eq:vince')
    ]

    f &= ('name', 'eq', 'bob')
    assert f.to_query_params() == [
        ('name[]', 'eq:vince'),
        ('name[]', 'eq:bob')
    ]


def test_two_length_filter():
    f = F('include_nodes', True)
    assert f.to_query_params() == [
        ('include_nodes', 'True')
    ]