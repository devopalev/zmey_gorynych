from dataclasses import dataclass
from enum import StrEnum


class RoleUser(StrEnum):
    USER = 'user'
    ADMIN = 'admin'

    def __str__(self) -> str:
        return self.value

    @classmethod
    def is_admin(cls, user: 'User') -> bool:
        return cls.ADMIN in user.roles


@dataclass
class User:
    id: int
    username: str
    password_hashed: str
    roles: list[RoleUser]
    revoked: bool
