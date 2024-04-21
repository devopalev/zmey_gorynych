from enum import StrEnum, Enum
from typing import Literal, TypeVar, Self, Any, Union
from uuid import UUID

from pydantic import BaseModel, model_validator


class TestDataEvent(BaseModel):
    test: Any


class EventType(str, Enum):
    TEST = 'test'
    KEEP_ALIVE = 'keep_alive'

    def __str__(self) -> str:
        return self.value

    @property
    def schema(self) -> BaseModel | None:
        match self:
            case self.TEST:
                return TestDataEvent


class Event(BaseModel):
    type: EventType
    data: Union[
        None,
        TestDataEvent,
    ] = None

    @model_validator(mode='after')
    def validate_data(self):
        if self.type.schema and not self.data:
            raise ValueError(f'<data> for type={self.type} required!')
        elif not self.type.schema and self.data:
            raise ValueError(f'<data> for type={self.type} must be null')
        elif self.type.schema and not isinstance(self.data, self.type.schema):
            raise ValueError('<data> does not match the <type>')
        return self
