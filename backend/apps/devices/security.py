from fastapi import HTTPException
from typing import Optional
from uuid import UUID

from fastapi import Depends
from fastapi.security import APIKeyHeader

from backend.apps.devices.domain.devices import TokenView
from backend.apps.devices.repository.repo import DeviceRepo
from backend.apps.users.exceptions import AccessError
from backend.apps.users.security import jwt_provider
from backend.core.security import hasher, TokenJWT

api_key_schema = APIKeyHeader(name=TokenView.key, auto_error=False)


async def api_key_provider(
    device_id: UUID,  # from path endpoint
    token: str = Depends(api_key_schema),
    device_repo: DeviceRepo = Depends(DeviceRepo),
) -> bool:
    if not token:
        return False

    token_original_hash = await device_repo.get_hash_token(uuid=device_id)
    if not token_original_hash:
        raise HTTPException(status_code=404, detail='Device not found')

    if not hasher.verify(token, token_original_hash):
        return False
    return True


async def _device_event_policy(
    api_key: Optional[bool] = Depends(api_key_provider), jwt: Optional[TokenJWT] = Depends(jwt_provider)
) -> None:
    if not api_key and not jwt:
        raise AccessError()


DeviceEventPolicy = Depends(_device_event_policy)
