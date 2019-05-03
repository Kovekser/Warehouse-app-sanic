from aiopg.sa import create_engine


async def select(statement, db):
    async with create_engine(**db) as engine:
        async with engine.acquire() as conn:
            result = [dict(r) async for r in conn.execute(statement)]
            return result[0] if len(result) == 1 else result


async def execute_statement(statement, db):
    async with create_engine(**db) as engine:
        async with engine.acquire() as conn:
            await conn.execute(statement)
