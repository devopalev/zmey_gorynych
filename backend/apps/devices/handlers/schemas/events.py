from enum import Enum
from typing import Any, Union, Self

from pydantic import BaseModel, model_validator, ValidationError
from pydantic_core import InitErrorDetails


class TestDataEvent(BaseModel):
    test: Any


class EventType(str, Enum):
    TEST = 'test'
    KEEP_ALIVE = 'keep_alive'

    def __str__(self) -> str:
        return str(self.value)

    @property
    def schema(self) -> type[BaseModel] | None:
        match self:
            case self.TEST:
                return TestDataEvent
        return None


class Event(BaseModel):
    type: EventType
    data: Union[
        None,
        TestDataEvent,
    ] = None

    @model_validator(mode='after')
    def validate_data(self) -> Self:
        loc = ('data',)
        line_errors = []

        if self.type.schema and not self.data:
            line_errors.append(
                InitErrorDetails(
                    loc=loc,
                    input=None,
                    ctx={'expected': f'data for type={self.type}'},
                    type='missing',
                )
            )
        elif not self.type.schema and self.data:
            line_errors.append(
                InitErrorDetails(
                    loc=loc,
                    input=self.data.model_dump(),
                    ctx={'error': ValueError('<data> was not expected')},
                    type='value_error',
                )
            )
        elif self.type.schema and not isinstance(self.data, self.type.schema):
            line_errors.append(
                InitErrorDetails(
                    loc=loc,
                    input=self.model_dump(),
                    ctx={'error': ValueError('<data> does not match the <type>, see docs by endpoint')},
                    type='value_error',
                )
            )

        if line_errors:
            raise ValidationError.from_exception_data(title='validation_error', line_errors=line_errors)

        return self
