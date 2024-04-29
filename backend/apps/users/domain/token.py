from dataclasses import dataclass
from datetime import datetime


@dataclass
class TokenView:
    access_token: str
    expire_utc: datetime
    type_token: str = 'Bearer'
