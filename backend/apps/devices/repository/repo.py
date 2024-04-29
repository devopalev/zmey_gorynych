from uuid import UUID

from backend.apps.devices.domain.devices import DeviceView
from backend.apps.devices.repository.queries import CREATE_DEVICE, GET_DEVICE, ACTIVITY_DEVICE
from backend.core.repository import BaseRepository


class DeviceRepo(BaseRepository):
    async def create(self, user_id: int, name: str) -> DeviceView:
        res = await self.connection.fetchrow(CREATE_DEVICE, user_id, name)
        return DeviceView(**dict(res.items()))

    async def get(self, uuid: UUID) -> DeviceView | None:
        res = await self.connection.fetchrow(GET_DEVICE, uuid)
        return DeviceView(**dict(res.items())) if res else None

    @classmethod
    async def update_activity(cls, uuid: UUID) -> None:
        async with cls.context_connection() as conn:
            await conn.execute(ACTIVITY_DEVICE, uuid)
