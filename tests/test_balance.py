import pytest
from pytest_httpx import HTTPXMock

from smsru import AioSMSru, SMSru


@pytest.mark.asyncio
async def test_aio_balance(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://sms.ru/my/balance?api_id=apfel&json=1",
        json={"status": "OK", "status_code": 100, "balance": 4762.58},
    )
    client = AioSMSru("apfel")
    response = await client.balance()
    assert response.status_code == 100
    assert response.balance == 4762.58
    assert response.status == "OK"


def test_balance(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://sms.ru/my/balance?api_id=apfel&json=1",
        json={"status": "OK", "status_code": 100, "balance": 4762.58},
    )
    client = SMSru("apfel")
    response = client.balance()
    assert response.status_code == 100
    assert response.balance == 4762.58
    assert response.status == "OK"
