from dataclasses import dataclass
import datetime


@dataclass
class TokenView:
    access_token: str
    refresh_token: str
    expire_utc: datetime.datetime
    type_access_token: str = 'Bearer'
    access_header_name: str = 'Authorization'
    refresh_header_name: str = 'x-refresh-token'


@dataclass
class RefreshToken:
    user_id: int
    refresh_token: str
