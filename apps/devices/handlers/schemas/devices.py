from pydantic import BaseModel


class DeviceCreateModel(BaseModel):
    name: str


