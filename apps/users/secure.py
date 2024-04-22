from datetime import datetime, timedelta
from typing import Self

from jose import jwt, JWTError

import settings
from apps.users.handlers.schemas import TokenView


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
