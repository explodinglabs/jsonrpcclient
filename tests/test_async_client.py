import pytest

from jsonrpcclient.async_client import AsyncClient
from jsonrpcclient.response import Response


class DummyClient(AsyncClient):
    async def send_message(self, request, **kwargs):
        return Response(None)


class Test():
    @pytest.mark.asyncio
    async def test_notify(self):
        await DummyClient("foo").notify("foo")
