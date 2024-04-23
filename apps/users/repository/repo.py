from apps.users.domain.users import User
from apps.users.repository.queries import GET_USER

from core.repository import BaseRepository


class UserRepo(BaseRepository):
    async def get(self, username: str) -> User | None:
        res = await self.connection.fetchrow(GET_USER, username)
        return User(**dict(res.items())) if res else None
