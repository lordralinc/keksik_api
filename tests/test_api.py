import json

import pytest

from keksik_api import KeksikAPI, KeksikAPIException
from keksik_api.schemas import PaymentsBalanceResponse
from tests.utils import make_session


@pytest.mark.asyncio
async def test_simple_request(aiohttp_client):
    response = dict(
        success=True,
        msg='test message'
    )
    api = KeksikAPI(
        0, '',
        session=await make_session(
            aiohttp_client,
            '/method',
            json.dumps(response)
        )
    )
    assert response == await api.request("method", {})


@pytest.mark.asyncio
async def test_error(aiohttp_client):
    response = dict(
        success=False,
        error=1000,
        msg='test message'
    )
    api = KeksikAPI(
        0, '',
        session=await make_session(
            aiohttp_client,
            '/method',
            json.dumps(response)
        )
    )
    with pytest.raises(KeksikAPIException):
        await api.request('method', {})
    assert response == await api.request("method", {}, raise_errors=False)


@pytest.mark.asyncio
async def test_validation(aiohttp_client):
    response = PaymentsBalanceResponse(
        success=True,
        balance=1000
    )
    api = KeksikAPI(
        0, '',
        session=await make_session(
            aiohttp_client,
            '/balance',
            response.json()
        )
    )
    assert response == await api.payments.balance()
