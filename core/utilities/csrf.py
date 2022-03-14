from flask_wtf.csrf import CSRFProtect
from functools import wraps
from flask import request

csrf = CSRFProtect()

def add_csrf(app):
    csrf.init_app(app)
    app.config['WTF_CSRF_ENABLED'] = False


def csrf_protect(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        csrf.protect()
        return func(*args, **kwargs)

    return wrapper
