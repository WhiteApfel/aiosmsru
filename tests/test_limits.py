import pytest
from pytest_httpx import HTTPXMock

from smsru import AioSMSru, SMSru


@pytest.mark.asyncio
async def test_aio_limits(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://sms.ru/my/limit?api_id=apfel&json=1",
        json={"status": "OK", "status_code": 100, "total_limit": 100, "used_today": 7},
    )
    client = AioSMSru("apfel")
    response = await client.limit()
    assert response.status_code == 100
    assert response.total_limit == 100
    assert response.used_today == 7


def test_limits(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://sms.ru/my/limit?api_id=apfel&json=1",
        json={"status": "OK", "status_code": 100, "total_limit": 100, "used_today": 7},
    )
    client = SMSru("apfel")
    response = client.limit()
    assert response.status_code == 100
    assert response.total_limit == 100
    assert response.used_today == 7


@pytest.mark.asyncio
async def test_aio_free_limits(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://sms.ru/my/free?api_id=apfel&json=1",
        json={"status": "OK", "status_code": 100, "total_free": 100, "used_today": 7},
    )
    client = AioSMSru("apfel")
    response = await client.free_limit()
    assert response.status_code == 100
    assert response.total_free == 100
    assert response.used_today == 7


def test_free_limits(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://sms.ru/my/free?api_id=apfel&json=1",
        json={"status": "OK", "status_code": 100, "total_free": 100, "used_today": 7},
    )
    client = SMSru("apfel")
    response = client.free_limit()
    assert response.status_code == 100
    assert response.total_free == 100
    assert response.used_today == 7
