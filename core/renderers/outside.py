from os.path import join
from flask import (
    Flask, jsonify, request, render_template, redirect, url_for, g
)


def outside_render(file, args={}):
    """Renders a template from templates/outside.

    Params:
        file: file should be a path relative to templates/outside.
        args: context variables for jinja2

    Returns:
        A Response object

    Raises:
        ValueError: On 'args' conflicting with standard outside_standard_args
    """
    outside_standard_args = {
        "outside_standard_user_username": g.user.username() if g.user is not None else "",
        "outside_standard_user_logged_in": g.user is not None
    }
    for key in args:
        if key in outside_standard_args:
            raise ValueError(key + " cannot be in args since it is already in outside_standard_args")
    return render_template(join("outside", file), **outside_standard_args, **args)
