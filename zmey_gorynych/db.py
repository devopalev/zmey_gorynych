import asyncpg

import settings


# TODO: del
async def init_db(app):
     app['pool'] = await asyncpg.create_pool(database='postgres',
                                             user='postgres')
     yield
     app['pool'].close()


pool = asyncpg.pool.create_pool(
    dsn=settings.DB_DSN,
    min_size=settings.DB_POOL_MIN_SIZE,
    max_size=settings.DB_POOL_MAX_SIZE
)


async def get_connection() -> asyncpg.Connection:
    async with pool.acquire() as con:
        yield con
