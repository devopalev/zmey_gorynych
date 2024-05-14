from typing import Optional

from backend.apps.users.domain.token import RefreshToken
from backend.apps.users.domain.users import User
from backend.apps.users.repository.queries import (
    GET_USER,
    GET_REFRESH_TOKEN,
    UPDATE_TOKEN,
    INSERT_TOKEN,
    DELETE_EXPIRED_TOKENS,
)

from backend.core.repository import BaseRepository


class UserRepo(BaseRepository):
    async def get(self, user_id: Optional[int] = None, username: Optional[str] = None) -> Optional[User]:
        res = await self.connection.fetchrow(GET_USER, user_id, username)
        return User(**dict(res.items())) if res else None

    async def get_refresh_token(self, user_id: int, refresh_token: str) -> Optional[RefreshToken]:
        await self.connection.execute(DELETE_EXPIRED_TOKENS)
        res = await self.connection.fetchrow(GET_REFRESH_TOKEN, user_id, refresh_token)
        return RefreshToken(**dict(res.items())) if res else None

    async def save_refresh_token(
        self, user_id: int, new_refresh_token: str, old_refresh_token: Optional[str] = None
    ) -> None:
        updated = False

        if old_refresh_token:
            res = await self.connection.execute(UPDATE_TOKEN, user_id, old_refresh_token, new_refresh_token)
            updated = self._utils.is_updated(res)

        if not updated:
            await self.connection.execute(INSERT_TOKEN, user_id, new_refresh_token)
