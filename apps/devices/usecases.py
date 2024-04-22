from abc import ABC
from uuid import UUID

from fastapi import Depends

from apps.devices.domain.devices import DeviceView
from apps.devices.repository.repo import DeviceRepo
from core.usecases import BaseUseCase


class BaseUseCaseDevice(BaseUseCase, ABC):
    def __init__(self, device_repo: DeviceRepo = Depends(DeviceRepo)):
        self.device_repo = device_repo


class CreateDevice(BaseUseCaseDevice):
    async def execute(self, user_id: int, device_name: str) -> DeviceView:
        return await self.device_repo.create(user_id=user_id, name=device_name)


class GetDevice(BaseUseCaseDevice):
    async def execute(self, uuid: UUID) -> DeviceView | None:
        return await self.device_repo.get(uuid=uuid)
