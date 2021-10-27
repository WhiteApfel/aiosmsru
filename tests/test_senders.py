import pytest
from pytest_httpx import HTTPXMock

from smsru import AioSMSru, SMSru


@pytest.mark.asyncio
async def test_aio_senders(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://sms.ru/my/senders?api_id=apfel&json=1&partner_id=331687",
        json={
            "status": "OK",
            "status_code": 100,
            "senders": ["pfelservice", "pfelstore"],
        },
    )
    client = AioSMSru("apfel")
    response = await client.senders()
    assert response.status_code == 100
    assert "pfelservice" in response.senders
    assert "pfelstore" in response.senders
    assert response.status == "OK"


def test_senders(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://sms.ru/my/senders?api_id=apfel&json=1&partner_id=331687",
        json={
            "status": "OK",
            "status_code": 100,
            "senders": ["pfelservice", "pfelstore"],
        },
    )
    client = SMSru("apfel")
    response = client.senders()
    assert response.status_code == 100
    assert "pfelservice" in response.senders
    assert "pfelstore" in response.senders
    assert response.status == "OK"
