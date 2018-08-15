from unittest.mock import sentinel

import pytest

from jsonrpcclient.async_client import AsyncClient
from jsonrpcclient.response import Response


class DummyClient(AsyncClient):
    async def send_message(self, request, **kwargs):
        res = '{"jsonrpc": "2.0", "result": 1, "id": 1}'
        return Response(res, raw=sentinel)


class Test:
    @pytest.mark.asyncio
    async def test_json_encoded(self):
        req = '{"jsonrpc": "2.0", "method": "foo", "id": 1}'
        response = await DummyClient("foo").send(req)
        assert response.data.result == 1

    @pytest.mark.asyncio
    async def test_json_decoded(self, *_):
        req = {"jsonrpc": "2.0", "method": "foo", "id": 1}
        response = await DummyClient("foo").send(req)
        assert response.data.result == 1

    @pytest.mark.asyncio
    async def test(self, *_):
        response = await DummyClient("foo").request("multiply", 3, 5)
        assert response.data.ok == True

    @pytest.mark.asyncio
    async def test(self, *_):
        response = await DummyClient("foo").notify("multiply", 3, 5)
        assert response.data.ok == True

    @pytest.mark.asyncio
    async def test_alternate_usage(self, *_):
        response = await DummyClient("foo").multiply(3, 5)
        assert response.data.ok == True
