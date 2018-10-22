from typing import Dict, List, Tuple


class F:
  """
  ``F`` is a funky little wrapper around a dictionary
  that helps compose query param filters. You can start with
  either an empty or single filter and use binary operators
  to augment the filters to your liking.

  .. example::

  >>> from aot_client import F
  >>> from datetime import datetime
  >>> f = F()
    f &= ('name', 'eq', 'vince')
    f.filters 
    {
      'name': ('eq', 'vince')
    }

    f &= ('age', 'gt', 21)
    f.filters
    {
      'name': ('eq', 'vince'),
      'age': ('gt', 21)
    }

    f &= ('name', 'eq', 'bob')
    f.filters
    {
      'name': [
        ('eq', 'vince'),
        ('eq', 'bob')
      ],
      'age': ('gt', 21)
    }

    f.to_query_params()
    [
      ('name[]', 'eq:vince'),
      ('name[]', 'eq:bob'),
      ('age', 'gt:21')
    ]
  """

  def __init__(self, *args):
    """Instantiates a new instance of ``F``
    """
    self.filters: Dict[str, tuple] = {}

    if args:
      key, op, value = args
      self.filters[key] = (op, value)

  def __iand__(self, other) -> 'F':
    """Joins two filters together.

    .. example::

    >>> from aot_client import F
    >>> f = F('name', 'eq', 'vince')
    >>> f &= ('name', 'eq', 'bob')
    >>> f.filters
    {
      'name': [
        ('eq', 'vince'),
        ('eq', 'bob')
      ]
    }
    """
    if isinstance(other, F):
      for key, op_value in other.filters.items():
        if key in self.filters:
          curr_val = self.filters[key]
          if not isinstance(curr_val, list):
            curr_val = [curr_val]

          if isinstance(op_value, list):
            curr_val.extend(op_value)
          else:
            curr_val.append(op_value)
          self.filters[key] = curr_val

        else:
          self.filters[key] = op_value

    elif isinstance(other, tuple):
      key, op, value = other

      if key in self.filters:
        curr_val = self.filters[key]
        if not isinstance(curr_val, list):
          curr_val = [curr_val]
        curr_val.append((op, value))
        self.filters[key] = curr_val

      else:
        self.filters[key] = (op, value)

    else:
      raise TypeError('other is neither F not Tuple')

    return self

  def __ior__(self, other) -> 'F':
    """Adds or replaces a filter value.

    .. example::

    >>> from aot_client import F
    >>> f = F('name', 'eq', 'vince')
    >>> f |= ('name', 'eq', 'bob')
    >>> f.filters
    {
      'name': ('eq', 'bob')
    }
    """
    if isinstance(other, F):
      for key, op_value in other.filters.items():
        self.filters[key] = op_value

    elif isinstance(other, tuple):
      key, op, value = other
      self.filters[key] = (op, value)

    else:
      raise TypeError('other is neither F nor Tuple')

    return self

  def to_query_params(self) -> List[Tuple[str, str]]:
    """Returns the filter as a list of tuples.
    """
    params = []

    for key, op_value in self.filters.items():
      if isinstance(op_value, list):
        key = '{key}[]'.format(key=key)
        for (op, value) in op_value:
          params.append(
            (key, '{op}:{value}'.format(op=op, value=value)))
      else:
        op, value = op_value
        params.append((key, '{op}:{value}'.format(op=op, value=value)))

    return params
