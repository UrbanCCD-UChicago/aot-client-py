import codecs
import json
import os


def load_fixture(name) -> dict:
  name = os.path.join('tests', 'fixtures', name)
  with codecs.open(name, encoding='utf8') as fh:
    return json.load(fh)