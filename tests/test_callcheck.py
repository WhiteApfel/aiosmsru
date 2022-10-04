import pytest
from pytest_httpx import HTTPXMock

from smsru import AioSMSru, SMSru


@pytest.mark.asyncio
async def test_aio_limits(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://sms.ru/code/call?phone=79998887766&ip=-1&api_id=apfel&json=1&partner_id=331687",
        json={
            "status": "OK",
            "status_code": 100,
            "balance": 314.15,
            "cost": 0.9,
            "call_id": "000000-10000000",
            "code": "7878",
        },
    )
    client = AioSMSru("apfel")
    response = await client.callcheck("79998887766")
    assert response.code == "7878"


def test_limits(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://sms.ru/code/call?phone=79998887766&ip=-1&api_id=apfel&json=1&partner_id=331687",
        json={
            "status": "OK",
            "status_code": 100,
            "balance": 314.15,
            "cost": 0.9,
            "call_id": "000000-10000000",
            "code": "7878",
        },
    )
    client = SMSru("apfel")
    response = client.callcheck("79998887766")
    assert response.code == "7878"
