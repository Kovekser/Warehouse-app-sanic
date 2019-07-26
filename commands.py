import os

from sanic.server import HttpProtocol
from aiopg.sa import create_engine

from service_api.application import app
from service_api.constants import BASIC_DB_CONFIG, get_port, get_host


def runserver():
    class CGDPHttpProtocol(HttpProtocol):

        def __init__(self, *args, **kwargs):
            if "request_timeout" in kwargs:
                kwargs.pop("request_timeout")
            super().__init__(*args, request_timeout=300, **kwargs)

    app.run(protocol=CGDPHttpProtocol, host='0.0.0.0', port=get_port(app.name))


class InitDB:

    def __init__(self, db_name):
        self.db_name = db_name

    async def create_db(self):
        async with create_engine(**BASIC_DB_CONFIG) as engine:
            async with engine.acquire() as conn:
                conn.autocommit = True
                db_exists = await conn.execute(f"SELECT 1 FROM pg_database WHERE datname = '{self.db_name}'")
                if not db_exists.rowcount:
                    role_exists = await conn.execute("SELECT 1 FROM pg_roles WHERE rolname='admin'")
                    if not role_exists.rowcount:
                        await conn.execute("CREATE ROLE admin WITH LOGIN ENCRYPTED PASSWORD 'admin';")
                    await conn.execute("CREATE DATABASE {} WITH OWNER = admin;".format(self.db_name))

                # Automatic migration
                script_dir = os.path.dirname(__file__)
                LIQUIBASE_COMMAND = """
                                {} {} --driver={} --classpath={} --changeLogFile={} --url={} --username={} --password={} --logLevel=info {}
                            """
                liquibase_command = LIQUIBASE_COMMAND.format(
                    'sudo' if get_host()=='localhost' else '',
                    os.path.join(script_dir, "./migrations/liquibase"),
                    "org.postgresql.Driver",
                    os.path.join(script_dir, "./migrations/jdbcdrivers/postgresql-42.2.5.jar"),
                    os.path.join(script_dir, "./migrations/changelog.xml"),
                    f"jdbc:postgresql://{get_host()}/{self.db_name}",
                    'admin',
                    'admin',
                    "migrate"
                )
                print(liquibase_command)
                os.system(liquibase_command)

    async def remove_test_db(self):
        async with create_engine(**BASIC_DB_CONFIG) as engine:
            async with engine.acquire() as conn:
                conn.autocommit = True
                await conn.execute("DROP DATABASE IF EXISTS {} ;".format(self.db_name))
