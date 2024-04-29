from datetime import datetime

import httpx
import pytest
from asyncpg import Connection


@pytest.mark.parametrize(
    ('status', 'params'),
    (
        (201, {'name': 'test_create_device'}),
        (422, {}),
    ),
)
async def test_create_device(
    test_client_user: httpx.AsyncClient,
    status: int,
    params: dict[str, str],
) -> None:
    response = await test_client_user.post(url='/api/v1/devices', json=params)
    json_response = response.json()
    assert status == response.status_code, json_response
    assert json_response.get('name') == params.get('name')


@pytest.mark.parametrize(
    ('status', 'device_id'),
    (
        (200, '65799ccd-bbc4-4026-a560-af152880280a'),
        (404, '3422b448-2460-4fd2-9183-8000de6f8343'),
    ),
)
async def test_get_device(
    test_client_user: httpx.AsyncClient,
    status: int,
    device_id: str,
) -> None:
    response = await test_client_user.get(url=f'/api/v1/devices/{device_id}')
    json_response = response.json()
    assert status == response.status_code, json_response


class TestDeviceEvent:
    async def test_event_test(
        self,
        test_client_user: httpx.AsyncClient,
    ) -> None:
        response = await test_client_user.post(
            url='/api/v1/devices/65799ccd-bbc4-4026-a560-af152880280a/event', json={'type': 'test', 'data': {'test': 1}}
        )
        assert 201 == response.status_code

    async def test_keep_alive(
        self,
        test_client_user: httpx.AsyncClient,
        test_db: Connection,
    ) -> None:
        sql = "select last_activity from devices where id = '65799ccd-bbc4-4026-a560-af152880280a'"
        last_activity = await test_db.fetchval(sql)
        assert last_activity is None, last_activity

        response = await test_client_user.post(
            url='/api/v1/devices/65799ccd-bbc4-4026-a560-af152880280a/event', json={'type': 'keep_alive'}
        )
        assert 201 == response.status_code

        sql = "select last_activity from devices where id = '65799ccd-bbc4-4026-a560-af152880280a'"
        new_last_activity = await test_db.fetchval(sql)
        assert isinstance(new_last_activity, datetime), new_last_activity

    @pytest.mark.parametrize(
        ('params', 'loc'),
        (
            ({'type': 'test'}, ['body', 'data']),
            ({'type': 'keep_alive', 'data': {'test': 1}}, ['body', 'data']),
            ({'type': 'unknown'}, ['body', 'type']),
        ),
    )
    async def test_bad_body(
        self,
        test_client_user: httpx.AsyncClient,
        params: dict[str, dict[str, str]],
        loc: list[str],
    ) -> None:
        response = await test_client_user.post(
            url='/api/v1/devices/65799ccd-bbc4-4026-a560-af152880280a/event', json=params
        )
        json_response = response.json()
        assert 422 == response.status_code, str(json_response)
        assert json_response['detail'][0].get('loc') == loc, str(json_response)
