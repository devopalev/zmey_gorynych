from asyncpg import Connection
from fastapi import Depends

from apps.users.domain.users import User
from zmey_gorynych.db import get_connection


class UserRepo:
    def __init__(self, connection: Connection = Depends(get_connection)):
        self.connection = connection

    async def get(self, username) -> User | None:

        return User('test', '$2b$12$DyNSDV3kIO6pzWLD00HsJuuEz0Elrskf4uf2KMkiFIlN9w9d0vIkW', ['user'], False)
