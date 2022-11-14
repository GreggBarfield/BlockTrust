from core.database.database import Database
import pytest


def pytest_addoption(parser):
    parser.addini('host', help="Database server")
    parser.addini('user', help="Username")
    parser.addini('password', help="Password")
    parser.addini('database', help="Database name")
    parser.addoption("--DB", action="store", default="DB server|Username|Password|DB")


@pytest.fixture(scope='session')
def db_connection(request):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value = request.config.getoption("--DB")
    print(option_value)
    # if 'name' in metafunc.fixturenames and option_value is not None:
    #     metafunc.parametrize("name", [option_value])
    #     print()
    db = Database({"host": request.config.getini("host"), "user": request.config.getini("user"),
                   "passwd": request.config.getini("password"), "database": request.config.getini("database")})
    yield db
    db.close()
