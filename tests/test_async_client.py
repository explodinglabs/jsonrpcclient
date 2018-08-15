from unittest.mock import sentinel

import pytest

from jsonrpcclient.async_client import AsyncClient
from jsonrpcclient.request import Request
from jsonrpcclient.response import Response


class DummyClient(AsyncClient):
    async def send_message(self, request, **kwargs):
        res = '{"jsonrpc": "2.0", "result": 1, "id": 1}'
        return Response(res, raw=sentinel)


class Test:
    @pytest.mark.asyncio
    async def test_json_encoded(self):
        request = '{"jsonrpc": "2.0", "method": "foo", "id": 1}'
        response = await DummyClient("foo").send(request)
        assert response.data.result == 1

    @pytest.mark.asyncio
    async def test_json_decoded(self, *_):
        request = {"jsonrpc": "2.0", "method": "foo", "id": 1}
        response = await DummyClient("foo").send(request)
        assert response.data.result == 1

    @pytest.mark.asyncio
    async def test_batch(self, *_):
        requests = [Request("foo"), Request("bar")]
        response = await DummyClient("foo").send(requests)
        assert response.data.result == 1

    @pytest.mark.asyncio
    async def test_alternate_usage(self, *_):
        response = await DummyClient("foo").multiply(3, 5)
        assert response.data.ok == True
