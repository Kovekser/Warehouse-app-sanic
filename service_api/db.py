from aiopg.sa import create_engine

from service_api.constants import DB_CONFIG


async def select(statement):
    async with create_engine(**DB_CONFIG) as engine:
        async with engine.acquire() as conn:
            result = [dict(r) async for r in conn.execute(statement)]
            return result[0] if len(result) == 1 else result


async def insert(statement):
    async with create_engine(**DB_CONFIG) as engine:
        async with engine.acquire() as conn:
            await conn.execute(statement)
