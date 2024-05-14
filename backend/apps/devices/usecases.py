from abc import ABC
from typing import Optional
from uuid import UUID

from fastapi import Depends
import secrets

from backend.apps.devices.domain.devices import DeviceView, TokenView
from backend.apps.devices.repository.repo import DeviceRepo
from backend.apps.users.domain.users import User
from backend.core.security import hasher
from backend.core.usecases import BaseUseCase


class BaseUseCaseDevice(BaseUseCase, ABC):
    def __init__(self, device_repo: DeviceRepo = Depends(DeviceRepo)):
        self.device_repo = device_repo


class CreateDevice(BaseUseCaseDevice):
    async def execute(self, user_id: int, device_name: str) -> DeviceView:
        return await self.device_repo.create(user_id=user_id, name=device_name)


class GetDevice(BaseUseCaseDevice):
    async def execute(self, user: User, uuid: UUID) -> Optional[DeviceView]:
        devices = await self.device_repo.get(user_id=user.id, uuid=uuid)
        try:  # Если except не ожидается часто, то это быстрее if
            return devices.pop()
        except IndexError:
            return None


class GetDevices(BaseUseCaseDevice):
    async def execute(self, user: User) -> list[DeviceView]:
        return await self.device_repo.get(user_id=user.id)


class CreateAccessToken(BaseUseCaseDevice):
    async def execute(self, uuid: UUID) -> Optional[TokenView]:
        new_token = secrets.token_hex(16)
        new_hash = hasher.hash(new_token)

        updated = await self.device_repo.save_hash_token(uuid=uuid, token_hash=new_hash)
        return TokenView(value=new_token) if updated else None
