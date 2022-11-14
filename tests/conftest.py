from core.database.database import Database
import pytest


def pytest_addoption(parser):
    parser.addoption("--DB", action="store", default="DB_server Username Password DB")


@pytest.fixture(scope='session')
def db_connection(request):
    db_string = request.config.getoption("--DB")
    db_config = db_string.split('|')
    db = Database({"host": db_config[0], "user": db_config[1],
                   "passwd": db_config[2], "database": db_config[3]})
    yield db
    db.close()
