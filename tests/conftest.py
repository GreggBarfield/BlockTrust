from core.database.database import Database
import pytest


def pytest_addoption(parser):
    parser.addini('host', help="Database server")
    parser.addini('user', help="Username")
    parser.addini('password', help="Password")
    parser.addini('database', help="Database name")


@pytest.fixture(scope='session')
def db_connection(request):
    db = Database({"host": request.config.getini("host"), "user": request.config.getini("user"),
                   "passwd": request.config.getini("password"), "database": request.config.getini("database")})
    yield db
    db.close()
