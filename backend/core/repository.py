from abc import ABC
from contextlib import asynccontextmanager

from asyncpg import Connection
from fastapi import Depends

from backend.core import db


class DBUtils:
    @staticmethod
    def is_updated(result: str) -> bool:
        return result != 'UPDATE 0'


class BaseRepository(ABC):
    context_connection = asynccontextmanager(db.get_connection)

    def __init__(self, connection: Connection = Depends(db.get_connection)):
        self.connection = connection
        self._utils = DBUtils()
