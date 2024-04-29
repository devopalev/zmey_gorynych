from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class DeviceView:
    id: UUID
    name: str
    revoked: bool
    last_activity: datetime
