import secrets
from abc import ABC
from typing import Optional

from fastapi import Depends

from backend.apps.users.domain.token import TokenView
from backend.apps.users.repository.repo import UserRepo
from backend.core.security import TokenJWT
from backend.core.security import hasher
from backend.core.usecases import BaseUseCase


class BaseUserUseCase(BaseUseCase, ABC):
    def __init__(self, user_repo: UserRepo = Depends(UserRepo)):
        self.user_repo = user_repo

    @staticmethod
    def _create_token(user_id: int) -> TokenView:
        jwt = TokenJWT(user_id=user_id)
        refresh = secrets.token_hex(32)
        return TokenView(
            access_token=jwt.access_token,
            refresh_token=refresh,
            expire_utc=jwt.exp,  # type: ignore[arg-type]
        )


class CreateTokenUseCase(BaseUserUseCase):
    async def execute(self, username: str, password: str) -> Optional[TokenView]:
        user = await self.user_repo.get(username=username)

        if not user or not hasher.verify(password, user.password_hashed) or user.revoked:
            return None

        new_token = self._create_token(user_id=user.id)
        await self.user_repo.save_refresh_token(user_id=user.id, new_refresh_token=new_token.refresh_token)
        return new_token


class RefreshTokenUseCase(BaseUserUseCase):
    async def execute(self, access_token: TokenJWT, refresh_token: str) -> Optional[TokenView]:
        r_token = await self.user_repo.get_refresh_token(user_id=access_token.user_id, refresh_token=refresh_token)

        if not r_token:
            return None

        new_token = self._create_token(user_id=r_token.user_id)
        await self.user_repo.save_refresh_token(
            user_id=r_token.user_id,
            new_refresh_token=new_token.refresh_token,
            old_refresh_token=r_token.refresh_token,
        )
        return new_token
