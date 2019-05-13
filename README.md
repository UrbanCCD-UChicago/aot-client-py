# Array of Things Client

This library serves as the official Python client to the [Array of Things API](https://api.arrayofthings.org/).

## System Requirements

This library will only run on Python 3.6 or better.

We __will not__ support Python 2 or earlier versions of Python 3.

## Using the Library

The AoT Client is available on PyPI:

```bash
$ pip install aot-client
```

You can then use it pull down lists of metadata and observations
as well as detailed information about metadata.

```python
from aot_client import AotClient

client = AotClient()
projects = client.list_projects()
for page in projects:
  for proj in page.data:
    print(f'{proj["name"]} is available at /api/projects/{proj["slug"]}')
```

## Development and Contributing

To run the tests locally:

```bash
$ pipenv install --dev
$ pipenv run python -m pytest
```

To build a release and push it to PyPI:

```bash
$ pipenv run python setup.py sdist bdist_wheel
$ pipenv run twine upload dist/*
```
