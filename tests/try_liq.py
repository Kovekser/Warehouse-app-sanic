import subprocess
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os


script_dir = os.path.dirname(__file__)

LIQUIBASE_COMMAND = """java -jar %s \
    --driver=%s \
    --classpath=%s \
    --changeLogFile=%s \
    --url="%s" \
    --username=%s \
    --password=%s \
    --logLevel=info \
"""

db_info = {
        'url': "jdbc:postgresql://localhost/test_db",
        'driver': "org.postgresql.Driver",
        'db_connector': os.path.join(script_dir, "../migrations/jdbcdrivers/postgresql-42.2.5.jar"),
        'command': LIQUIBASE_COMMAND
}

liquibase_command = db_info['command'] % (
    os.path.join(script_dir, "../migrations/liquibase.jar"),
    db_info['driver'],
    db_info['db_connector'],
    os.path.join(script_dir, "../migrations/changelog.xml"),
    db_info['url'],
    'postgres',
    'admin'
)


# command = """./migrations/liquibase.jar --url=jdbc:postgresql://localhost/test_db \
# 	--driver=org.postgresql.Driver \
# 	--classpath=./migrations/jdbcdrivers/postgresql-42.2.5.jar \
# 	--username=postgres \
# 	--password=admin \
# 	--changeLogFile=/migrations/changelog.xml """

con = psycopg2.connect(dbname='postgres',
      user='postgres', host='localhost',
      password='admin')

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = con.cursor()
try:
    cur.execute("DROP DATABASE {}  ;".format('test_db'))
except psycopg2.ProgrammingError:
    pass
finally:
    cur.execute("CREATE DATABASE {}  ;".format('test_db'))
    cur.close()

liquibase_command = liquibase_command + "migrate"
print(liquibase_command)
import os
os.system(liquibase_command)
# output = subprocess.check_output(
#     liquibase_command,
#     stderr=subprocess.STDOUT,
#     shell=True
# )

# print(output)

# cur.execute("DROP DATABASE {}  ;" .format('test_db'))