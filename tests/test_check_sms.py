import pytest
from pytest_httpx import HTTPXMock

from smsru import AioSMSru, SMSru


@pytest.mark.asyncio
async def test_aio_check_sms(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://sms.ru/sms/status?api_id=apfel&sms_id=000000-000001,000000-000002,000000-000003&json=1",
        json={
            "status": "OK",
            "status_code": 100,
            "sms": {
                "000000-000001": {
                    "status": "OK",
                    "status_code": 103,
                    "cost": 0.50,
                    "status_text": "Сообщение доставлено",
                },
                "000000-000002": {
                    "status": "OK",
                    "status_code": 104,
                    "cost": 0.50,
                    "status_text": "Не может быть доставлено: время жизни истекло",
                },
                "000000-000003": {
                    "status": "ERROR",
                    "status_code": -1,
                    "status_text": "Сообщение не найдено",
                },
            },
            "balance": 4122.56,
        },
    )
    client = AioSMSru("apfel")
    response = await client.check_sms(
        ["000000-000001", "000000-000002", "000000-000003"]
    )
    assert response.status_code == 100
    assert response.status == "OK"
    assert response.sms["000000-000001"].cost == 0.5
    assert response.sms["000000-000003"].status_code == -1
    assert response.sms["000000-000003"].cost is None
    assert response.balance == 4122.56


@pytest.mark.asyncio
async def test_aio_check_one_sms(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://sms.ru/sms/status?api_id=apfel&sms_id=000000-000001&json=1",
        json={
            "status": "OK",
            "status_code": 100,
            "sms": {
                "000000-000001": {
                    "status": "OK",
                    "status_code": 103,
                    "cost": 0.50,
                    "status_text": "Сообщение доставлено",
                }
            },
            "balance": 4122.56,
        },
    )
    client = AioSMSru("apfel")
    response = await client.check_sms("000000-000001")
    assert response.status_code == 100
    assert response.status == "OK"
    assert response.sms["000000-000001"].cost == 0.5
    assert response.balance == 4122.56


def test_check_sms(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://sms.ru/sms/status?api_id=apfel&sms_id=000000-000001,000000-000002,000000-000003&json=1",
        json={
            "status": "OK",
            "status_code": 100,
            "sms": {
                "000000-000001": {
                    "status": "OK",
                    "status_code": 103,
                    "cost": 0.50,
                    "status_text": "Сообщение доставлено",
                },
                "000000-000002": {
                    "status": "OK",
                    "status_code": 104,
                    "cost": 0.50,
                    "status_text": "Не может быть доставлено: время жизни истекло",
                },
                "000000-000003": {
                    "status": "ERROR",
                    "status_code": -1,
                    "status_text": "Сообщение не найдено",
                },
            },
            "balance": 4122.56,
        },
    )
    client = SMSru("apfel")
    response = client.check_sms(["000000-000001", "000000-000002", "000000-000003"])
    assert response.status_code == 100
    assert response.status == "OK"
    assert response.sms["000000-000001"].cost == 0.5
    assert response.sms["000000-000003"].status_code == -1
    assert response.sms["000000-000003"].cost is None
    assert response.balance == 4122.56


def test_check_one_sms(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://sms.ru/sms/status?api_id=apfel&sms_id=000000-000001&json=1",
        json={
            "status": "OK",
            "status_code": 100,
            "sms": {
                "000000-000001": {
                    "status": "OK",
                    "status_code": 103,
                    "cost": 0.50,
                    "status_text": "Сообщение доставлено",
                }
            },
            "balance": 4122.56,
        },
    )
    client = SMSru("apfel")
    response = client.check_sms("000000-000001")
    assert response.status_code == 100
    assert response.status == "OK"
    assert response.sms["000000-000001"].cost == 0.5
    assert response.balance == 4122.56
