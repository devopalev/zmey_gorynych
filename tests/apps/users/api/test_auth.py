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
    response = await test_client_user.post(url='/api/v1/users/token', json=params)
    json_response = response.json()
    assert status == response.status_code, json_response
