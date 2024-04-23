from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str


class UserAuth(BaseUser):
    password: str
