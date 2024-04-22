from abc import ABC
from contextlib import asynccontextmanager

from asyncpg import Connection
from fastapi import Depends

from core import db


class BaseRepository(ABC):
    context_connection = asynccontextmanager(db.get_connection)

    def __init__(self, connection: Connection = Depends(db.get_connection)):
        self.connection = connection
