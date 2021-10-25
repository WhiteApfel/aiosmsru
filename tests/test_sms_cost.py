import pytest
from pytest_httpx import HTTPXMock

from smsru import AioSMSru, SMSru


@pytest.mark.asyncio
async def test_aio_one_sms_cost(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://sms.ru/sms/cost?api_id=apfel&to=79991398805&msg=hello+world&json=1",
        json={
            "status": "OK",
            "status_code": 100,
            "sms": {
                "79991398805": {
                    "status": "OK",
                    "status_code": 100,
                    "cost": 0.50,
                    "sms": 2,
                }
            },
            "total_cost": 1.00,
            "total_sms": 2,
        },
    )
    client = AioSMSru("apfel")
    response = await client.sms_cost("79991398805", "hello world")
    assert response.status_code == 100
    assert response.status == "OK"
    assert response.sms["79991398805"].sms == 2
    assert response.sms["79991398805"].cost == 0.5
    assert response.total_cost == 1.0
    assert response.total_sms == 2


def test_one_sms_cost(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://sms.ru/sms/cost?api_id=apfel&to=79991398805&msg=hello+world&json=1",
        json={
            "status": "OK",
            "status_code": 100,
            "sms": {
                "79991398805": {
                    "status": "OK",
                    "status_code": 100,
                    "cost": 0.50,
                    "sms": 2,
                }
            },
            "total_cost": 1.00,
            "total_sms": 2,
        },
    )
    client = SMSru("apfel")
    response = client.sms_cost("79991398805", "hello world")
    assert response.status_code == 100
    assert response.status == "OK"
    assert response.sms["79991398805"].sms == 2
    assert response.sms["79991398805"].cost == 0.5
    assert response.total_cost == 1.0
    assert response.total_sms == 2


@pytest.mark.asyncio
async def test_aio_any_sms_one_text_cost(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://sms.ru/sms/cost?api_id=apfel&to=79991398805,79956896018&msg=hello+world&json=1",
        json={
            "status": "OK",
            "status_code": 100,
            "sms": {
                "79991398805": {
                    "status": "OK",
                    "status_code": 100,
                    "cost": 0.50,
                    "sms": 2,
                },
                "79956896018": {
                    "status": "ERROR",
                    "status_code": 207,
                    "status_text": "Джигурда",
                },
            },
            "total_cost": 1.00,
            "total_sms": 2,
        },
    )
    client = AioSMSru("apfel")
    response = await client.sms_cost(["79991398805", "79956896018"], "hello world")
    assert response.status_code == 100
    assert response.status == "OK"
    assert response.sms["79991398805"].cost == 0.5
    assert response.sms["79956896018"].status_code == 207
    assert response.sms["79956896018"].sms is None
    assert response.total_cost == 1.0


def test_aio_send_any_sms(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://sms.ru/sms/cost?api_id=apfel&to[79991398805]=hello+world&to[79956896018]=hello+world&json=1",
        json={
            "status": "OK",
            "status_code": 100,
            "sms": {
                "79991398805": {
                    "status": "OK",
                    "status_code": 100,
                    "cost": 0.50,
                    "sms": 2,
                },
                "79956896018": {
                    "status": "ERROR",
                    "status_code": 207,
                    "status_text": "Юра, мы всё просрали",
                },
            },
            "total_cost": 1.00,
            "total_sms": 2,
        },
    )
    client = SMSru("apfel")
    response = client.sms_cost(
        ["79991398805", "79956896018"], ["hello world", "hello world"]
    )
    assert response.status_code == 100
    assert response.status == "OK"
    assert response.sms["79991398805"].sms == 2
    assert response.sms["79956896018"].status_code == 207
