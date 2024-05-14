from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from typing import Self, cast, Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

import settings


@dataclass
class TokenJWT:
    user_id: int
    exp: Optional[datetime] = None

    def __post_init__(self) -> None:
        if not self.exp:
            now = datetime.now(tz=timezone.utc)
            self.exp = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    @property
    def access_token(self) -> str:
        return cast(str, jwt.encode(asdict(self), settings.SECRET_KEY, algorithm=settings.ALGORITHM))

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
