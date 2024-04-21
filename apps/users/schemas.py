from datetime import datetime

from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str


class UserAuth(BaseUser):
    password: str


class TokenView(BaseModel):
    access_token: str
    expire_utc: datetime
    type_token: str = 'Bearer'
