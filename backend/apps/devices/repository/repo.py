from typing import Optional, cast
from uuid import UUID

from backend.apps.devices.domain.devices import DeviceView
from backend.apps.devices.repository.queries import (
    CREATE_DEVICE,
    GET_DEVICE,
    GET_DEVICES,
    ACTIVITY_DEVICE,
    SAVE_TOKEN,
    GET_DEVICE_TOKEN,
)
from backend.core.repository import BaseRepository


class DeviceRepo(BaseRepository):
    async def create(self, user_id: int, name: str) -> DeviceView:
        res = await self.connection.fetchrow(CREATE_DEVICE, user_id, name)
        return DeviceView(**dict(res.items()))

    async def get(self, user_id: int, uuid: Optional[UUID] = None) -> list[DeviceView]:
        if uuid:
            res = await self.connection.fetch(GET_DEVICE, user_id, uuid)
        else:
            res = await self.connection.fetch(GET_DEVICES, user_id)
        return [DeviceView(**dict(r.items())) for r in res]

    async def save_hash_token(self, token_hash: str, uuid: UUID) -> bool:
        res = await self.connection.execute(SAVE_TOKEN, token_hash, uuid)
        return bool(int(res[-1]))

    async def get_hash_token(self, uuid: UUID) -> Optional[str]:
        return cast(Optional[str], await self.connection.fetchval(GET_DEVICE_TOKEN, uuid))

    @classmethod
    async def update_activity(cls, uuid: UUID) -> None:
        async with cls.context_connection() as conn:
            await conn.execute(ACTIVITY_DEVICE, uuid)
