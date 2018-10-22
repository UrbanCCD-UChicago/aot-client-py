import re

import responses

from aot_client import AotClient
from aot_client.responses import PagedResponse
from utils import load_fixture


page_2_regex = re.compile('.*page=2.*')
page_3_regex = re.compile('.*page=3.*')


@responses.activate
def test_iter():
  responses.add(
    method=responses.GET,
    url=page_2_regex,
    status=200,
    json=load_fixture('obs-2.json')
  )
  responses.add(
    method=responses.GET,
    url=page_3_regex,
    status=200,
    json={'data': []}
  )

  client = AotClient()
  payload = load_fixture('obs.json')

  dataset = PagedResponse(payload, client)
  pages = [page for page in dataset]
  
  assert len(pages) == 2