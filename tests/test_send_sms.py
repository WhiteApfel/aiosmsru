import pytest
from pytest_httpx import HTTPXMock

from smsru import AioSMSru, SMSru


@pytest.mark.asyncio
async def test_aio_send_one_sms(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://sms.ru/sms/send?api_id=apfel&to=79991398805&msg=hello+world&json=1",
        json={
            "status": "OK",
            "status_code": 100,
            "sms": {
                "79991398805": {
                    "status": "OK",
                    "status_code": 100,
                    "sms_id": "000000-10000000"
                }
            },
            "balance": 4122.56
        }
    )
    client = AioSMSru("apfel")
    response = await client.send_sms("79991398805", 'hello world')
    assert response.status_code == 100
    assert response.status == "OK"
    assert response.sms['79991398805'].sms_id == "000000-10000000"
    assert response.balance == 4122.56


def test_send_one_sms(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://sms.ru/sms/send?api_id=apfel&to=79991398805&msg=hello+world&json=1",
        json={
            "status": "OK",
            "status_code": 100,
            "sms": {
                "79991398805": {
                    "status": "OK",
                    "status_code": 100,
                    "sms_id": "000000-10000000"
                }
            },
            "balance": 4122.56
        }
    )
    client = SMSru("apfel")
    response = client.send_sms("79991398805", 'hello world')
    assert response.status_code == 100
    assert response.status == "OK"
    assert response.sms['79991398805'].sms_id == "000000-10000000"
    assert response.balance == 4122.56
