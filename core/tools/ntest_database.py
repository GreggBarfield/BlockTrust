import mysql.connector
from mysql.connector.constants import ClientFlag
from core.config import MYSQL_CONFIG, API_MYSQL_CONFIG

# Run with python -m core.tools.ntest_database


def test_config(config):
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor(buffered=True)
    cur.execute("SHOW STATUS LIKE 'Ssl_cipher'")
    f = cur.fetchone()
    print(f)
    if f[0] != 'Ssl_cipher':
        raise "Bad"
    cur.close()
    cnx.close()


test_config(MYSQL_CONFIG)
test_config(API_MYSQL_CONFIG)
