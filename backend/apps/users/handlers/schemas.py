from datetime import datetime

from pydantic import BaseModel


class UserAuth(BaseModel):
    username: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    expire_utc: datetime
    type_token: str
