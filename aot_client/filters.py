from typing import Dict, List, Tuple, Union


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
    self.filters = {}
    if args:
      key, *params = args
      self.filters[key] = [tuple(params)]

  def __iand__(self, other: Union['F', tuple]) -> 'F':
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
    if isinstance(other, tuple):
      self.__iand__(F(*other))
    
    elif isinstance(other, F):
      for key, params in other.filters.items():
        if key in self.filters:
          self.filters[key].extend(params)
        
        else:
          self.filters[key] = params
    
    else:
      raise TypeError('Must be either an instance of F or a tuple')
    
    return self

  def __ior__(self, other: Union['F', tuple]) -> 'F':
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
    if isinstance(other, tuple):
      self.__ior__(F(*other))

    elif isinstance(other, F):
      for key, params in other.filters.items():
        self.filters[key] = params

    else:
      raise TypeError('Must be either an instance of F or a tuple')

    return self

  def to_query_params(self):
    """Returns the filter as a list of tuples.
    """
    params = []

    for key, values in self.filters.items():
      if len(values) > 1:
        key = f'{key}[]'

      for value in values:
        value = ':'.join(str(x) for x in value)
        params.append((key, value))

    return params