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


class RequireSubscriberFailed(Exception):
    pass


def _require_subscriber():
    if g.account.stripe_customer_id() != "" and g.account.stripe_customer_id() is not None and g.account.generated_paid() == 1:
        return
    raise RequireSubscriberFailed()


class RequireEmployeeFailed(Exception):
    pass


def _require_employee():
    if 'employee' in g and g.employee is not None:
        return
    raise RequireEmployeeFailed()


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


def require_employee(func):
    """Decorator to ensure a employee is logged in."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        _require_employee()
        return func(*args, **kwargs)

    return wrapper


def require_subscriber(func):
    """Decorator to ensure that a subscriber is accesing the page."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        _require_user()
        _require_account()
        _require_subscriber()
        return func(*args, **kwargs)
    return wrapper
