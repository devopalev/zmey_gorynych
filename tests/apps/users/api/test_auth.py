import httpx
import pytest


@pytest.mark.parametrize(
    ('status', 'params'),
    (
        (201, {'username': 'test_user', 'password': 'Xx7536951xX'}),
        (401, {'username': 'bad_username', 'password': 'Xx7536951xX'}),
        (401, {'username': 'test_user', 'password': 'bad_password'}),
        (422, {}),
    ),
)
async def test_create_token(
    test_client_user: httpx.AsyncClient,
    status: int,
    params: dict[str, str],
) -> None:
    response = await test_client_user.post(url='/api/v1/users/token', data=params)
    json_response = response.json()
    assert status == response.status_code, json_response


async def test_refresh_token(
    test_client_user: httpx.AsyncClient,
) -> None:
    auth_data = {'username': 'test_user', 'password': 'Xx7536951xX'}
    response = await test_client_user.post(url='/api/v1/users/token', data=auth_data)
    res_json = response.json()['result']
    headers = {
        res_json['access_header_name']: f"{res_json['type_access_token']} {res_json['access_token']}",
        res_json['refresh_header_name']: res_json['refresh_token'],
    }

    response = await test_client_user.post(url='/api/v1/users/refresh-token', headers=headers)
    assert response.status_code == 201

    response = await test_client_user.post(url='/api/v1/users/refresh-token', headers=headers)
    assert response.status_code == 401
