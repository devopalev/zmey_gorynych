from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Self, cast, Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

import settings
from backend.apps.users.domain.token import TokenView


@dataclass
class TokenJWT:
    sub: str
    exp: Optional[datetime] = None

    def __post_init__(self) -> None:
        if not self.exp:
            now = datetime.now(tz=timezone.utc)
            self.exp = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    @property
    def view(self) -> TokenView:
        to_encode = {
            'sub': self.sub,
            'exp': self.exp,
        }

        token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return TokenView(access_token=token, expire_utc=cast(datetime, self.exp))

    @classmethod
    def from_token(cls, token: str) -> Self:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            payload['exp'] = datetime.fromtimestamp(payload['exp'])
            return cls(**payload)
        except JWTError:
            raise ValueError('Bad token')


class _Hasher:
    context = CryptContext(schemes=['bcrypt'])

    def verify(self, value: str, original_hash: str) -> bool:
        try:
            return cast(bool, self.context.verify(value, original_hash))
        except ValueError:
            return False

    def hash(self, value: str) -> str:
        return cast(str, self.context.hash(value))


hasher = _Hasher()
