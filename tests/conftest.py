from core.database.database import Database
import pytest


def pytest_addoption(parser):
    parser.addini('host', help="Database server")
    parser.addini('user', help="Username")
    parser.addini('password', help="Password")
    parser.addini('database', help="Database name")
    parser.addoption("--DB", action="store", default="DB_server Username Password DB")


@pytest.fixture(scope='session')
def db_connection(request):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    db_string = request.config.getoption("--DB")
    print(type(db_string))
    db_string = db_string.split('|')
    print(db_string)
    # if 'name' in metafunc.fixturenames and option_value is not None:
    #     metafunc.parametrize("name", [option_value])
    #     print()
    db = Database({"host": db_string[0], "user": db_string[1],
                   "passwd": db_string[2], "database": db_string[3]})
    yield db
    db.close()
