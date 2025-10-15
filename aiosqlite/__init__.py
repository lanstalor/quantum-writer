"""Lightweight stand-in for :mod:`aiosqlite` used in test environments.

This shim implements the minimal API that SQLAlchemy expects from the
`aiosqlite` driver so that asynchronous SQLAlchemy sessions can operate
against SQLite without requiring the external dependency (which cannot be
installed in the execution sandbox).  The implementation performs the
database work synchronously inside lightweight ``async`` wrappers, which is
acceptable for the unit-test workloads exercised in this repository.
"""

from __future__ import annotations

import asyncio
import sqlite3
from typing import Any, Iterable, Optional

__all__ = [
    "connect",
    "Connection",
    "Cursor",
    "Error",
    "DatabaseError",
    "IntegrityError",
    "NotSupportedError",
    "OperationalError",
    "ProgrammingError",
    "PARSE_DECLTYPES",
    "PARSE_COLNAMES",
    "sqlite_version",
    "sqlite_version_info",
]

Error = sqlite3.Error
DatabaseError = sqlite3.DatabaseError
IntegrityError = sqlite3.IntegrityError
NotSupportedError = sqlite3.NotSupportedError
OperationalError = sqlite3.OperationalError
ProgrammingError = sqlite3.ProgrammingError

PARSE_DECLTYPES = sqlite3.PARSE_DECLTYPES
PARSE_COLNAMES = sqlite3.PARSE_COLNAMES

sqlite_version = sqlite3.sqlite_version
sqlite_version_info = sqlite3.sqlite_version_info


class _ImmediateQueue:
    """Queue-like helper that immediately executes callables."""

    def put_nowait(self, item: tuple[asyncio.Future, callable]) -> None:
        future, func = item
        try:
            result = func()
        except Exception as exc:  # pragma: no cover - surfaced in tests
            future.set_exception(exc)
        else:
            future.set_result(result)


class Cursor:
    def __init__(self, connection: "Connection"):
        self._connection = connection
        self._cursor = connection._conn.cursor()
        self.description = None
        self.rowcount = -1
        self.lastrowid = None

    async def execute(self, operation: str, parameters: Optional[Iterable[Any]] = None):
        if parameters is None:
            self._cursor.execute(operation)
        else:
            self._cursor.execute(operation, parameters)
        self.description = self._cursor.description
        self.rowcount = self._cursor.rowcount
        self.lastrowid = self._cursor.lastrowid
        return self

    async def executemany(self, operation: str, seq_of_parameters: Iterable[Iterable[Any]]):
        self._cursor.executemany(operation, seq_of_parameters)
        self.description = None
        self.rowcount = self._cursor.rowcount
        self.lastrowid = self._cursor.lastrowid
        return self

    async def fetchall(self):
        return self._cursor.fetchall()

    async def fetchone(self):
        return self._cursor.fetchone()

    async def fetchmany(self, size: Optional[int] = None):
        if size is None:
            size = self._cursor.arraysize
        return self._cursor.fetchmany(size)

    async def close(self):
        self._cursor.close()


class Connection:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
        self._conn.row_factory = sqlite3.Row
        self._lock = asyncio.Lock()
        self._tx = _ImmediateQueue()
        self.isolation_level = conn.isolation_level

    async def cursor(self) -> Cursor:
        return Cursor(self)

    async def execute(self, operation: str, parameters: Optional[Iterable[Any]] = None):
        async with self._lock:
            cursor = await self.cursor()
            await cursor.execute(operation, parameters)
            return cursor

    async def executemany(self, operation: str, seq_of_parameters: Iterable[Iterable[Any]]):
        async with self._lock:
            cursor = await self.cursor()
            await cursor.executemany(operation, seq_of_parameters)
            return cursor

    async def commit(self):
        self._conn.commit()

    async def rollback(self):
        self._conn.rollback()

    async def close(self):
        self._conn.close()

    async def create_function(self, *args, **kwargs):
        self._conn.create_function(*args, **kwargs)

    @property
    def row_factory(self):
        return self._conn.row_factory

    @row_factory.setter
    def row_factory(self, factory):
        self._conn.row_factory = factory


class _ConnectAwaitable:
    def __init__(self, args, kwargs):
        self._args = args
        self._kwargs = kwargs
        self.daemon = True

    def __await__(self):
        async def _connect():
            kwargs = dict(self._kwargs)
            kwargs.setdefault("check_same_thread", False)
            conn = sqlite3.connect(*self._args, **kwargs)
            return Connection(conn)

        return _connect().__await__()


def connect(*args, **kwargs):
    """Return an awaitable object yielding a :class:`Connection`."""

    return _ConnectAwaitable(args, kwargs)
