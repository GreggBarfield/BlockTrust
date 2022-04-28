from functools import wraps
from flask import g


class RequireUserFailed(Exception):
    pass


def _require_user():
    if 'user' in g and g.user is not None:
        return
    raise RequireUserFailed()


class RequireAccountFailed(Exception):
    pass


def _require_account():
    if 'account' in g and g.account is not None:
        return
    raise RequireAccountFailed()


class RequirePaidAccountFailed(Exception):
    pass


def _require_paid_account():
    if g.account.generated_paid() == 1:
        return
    raise RequirePaidAccountFailed()


class RequireEmployeeFailed(Exception):
    pass


def _require_employee():
    if 'employee' in g and g.employee is not None:
        return
    raise RequireEmployeeFailed()


class RequireAccountOrEmployeeFailed(Exception):
    pass


def _require_account_or_employee():
    if 'account' in g and g.account is not None:
        if 'user' in g and g.user is not None:
            return
    if 'employee' in g and g.employee is not None:
        return
    raise RequireAccountOrEmployeeFailed()


def require_user(func):
    """Decorator to ensure a user is logged in."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        _require_user()
        return func(*args, **kwargs)

    return wrapper


def require_account(func):
    """Decorator to ensure a user has an account and is logged in."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        _require_user()
        _require_account()
        return func(*args, **kwargs)
    return wrapper


def require_paid_account(func):
    """Decorator to ensure a user has a paid account and is logged in."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        _require_user()
        _require_account()
        _require_paid_account()
        return func(*args, **kwargs)
    return wrapper


def require_employee(func):
    """Decorator to ensure a employee is logged in."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        _require_employee()
        return func(*args, **kwargs)

    return wrapper


def require_account_or_employee(func):
    """Decorator to ensure an employee or a user with an account is logged in."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        _require_account_or_employee()
        return func(*args, **kwargs)

    return wrapper
