import pytest
from jsonrpcclient.async_client import AsyncClient


class DummyClient(AsyncClient):
    async def send_message(self, request, **kwargs):
        pass


class Test():
    @pytest.mark.asyncio
    async def test_notify(self):
        await DummyClient("foo").notify("foo")
