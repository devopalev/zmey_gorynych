from dataclasses import dataclass
from enum import StrEnum


class RoleUser(StrEnum):
    USER = 'user'
    ADMIN = 'admin'

    def __str__(self) -> str:
        return self.value

    @classmethod
    def is_admin(cls, user: 'User'):
        return cls.ADMIN in user.roles


@dataclass
class User:
    username: str
    hashed_password: str
    roles: list[RoleUser]
    disabled: bool
