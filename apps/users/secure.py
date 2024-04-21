from datetime import datetime, timedelta
from typing import Self, Iterable

from fastapi import Depends
from jose import jwt, JWTError
from passlib.context import CryptContext

import settings
from apps.users.domain.users import RoleUser
from apps.users.schemas import TokenView


class PasswordHasher:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, password):
        self.hashed_password = self.hash_password(password)

    def __eq__(self, other):
        assert isinstance(other, self.__class__)
        return self.hashed_password == other.hashed_password

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.pwd_context.hash(password)


class TokenJWTFactory:
    _KEY_SUB = 'sub'
    _KEY_EXP = 'exp'

    def __init__(self, sub: str, exp: int | None = None):
        self.sub: str = sub
        self._token: TokenView | None = None

        if exp:
            self.expire: datetime = datetime.fromtimestamp(exp)
        else:
            self.expire: datetime = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    def create_token(self) -> TokenView:
        if self._token:
            return self._token

        to_encode = {
            self._KEY_SUB: self.sub,
            self._KEY_EXP: self.expire,
        }

        token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return TokenView(access_token=token, expire_utc=self.expire)

    @classmethod
    def from_token(cls, token: str) -> Self:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return cls(**payload)
        except JWTError:
            raise ValueError('Bad token')
