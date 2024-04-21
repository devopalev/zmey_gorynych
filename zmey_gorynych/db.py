import asyncpg
from asyncpg import Pool
import settings

pool: Pool | None = None


async def init():
    global pool
    pool = await asyncpg.pool.create_pool(
        dsn=settings.DB_DSN,
        min_size=settings.DB_POOL_MIN_SIZE,
        max_size=settings.DB_POOL_MAX_SIZE
    )


async def shutdown():
    if pool:
        await pool.close()


async def get_connection() -> asyncpg.Connection:
    if pool:
        async with pool.acquire() as con:
            yield con
    else:
        raise ValueError('pool is not initialized')
