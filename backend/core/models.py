import typing
from dataclasses import dataclass

T = typing.TypeVar('T')


@dataclass
class Result(typing.Generic[T]):
    result: T
