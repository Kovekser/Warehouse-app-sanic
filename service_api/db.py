from aiopg.sa import create_engine
from service_api.constants import DB_CONFIG


async def select_statement(statement):
    async with create_engine(**DB_CONFIG) as engine:
        async with engine.acquire() as conn:
            result_proxy = await conn.execute(statement)
            data = [dict(r) for r in result_proxy]
            return data, result_proxy.keys()


async def execute_statement(statement):
    async with create_engine(**DB_CONFIG) as engine:
        async with engine.acquire() as conn:
            await conn.execute(statement)
