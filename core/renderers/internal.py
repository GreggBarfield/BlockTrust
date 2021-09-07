from os.path import join
from flask import (
    Flask, jsonify, request, render_template, session, redirect, url_for, g
)


def internal_render(file, args={}):
    """Renders a template from templates/internal.

    Params:
        file: file should be a path relative to internal/internal.
        args: context variables for jinja2

    Returns:
        A Response object

    Raises:
        ValueError: On 'args' conflicting with standard internal_standard_args
        ValueError: On the user not being logged in

    """
    if g.user is None:
        raise ValueError("user is not logged in")
    internal_standard_args = {
        "internal_standard_user_first": g.user.first(),
        "internal_standard_user_last": g.user.last(),
        "internal_standard_user_username": g.user.username(),
        "internal_standard_account": g.account,
        "internal_standard_is_admin": g.is_admin
    }
    for key in args:
        if key in internal_standard_args:
            raise ValueError(key + " cannot be in args since it is already in internal_standard_args")
    return render_template(join("internal", file), **internal_standard_args, **args)
