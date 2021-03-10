from os.path import join
from flask import (
    Flask, jsonify, request, render_template, redirect, url_for, g
)


def render_email(file, args={}):
    """Renders a template from templates/email.

    Params:
        file: file should be a path relative to templates/emails.
        args: context variables for jinja2

    Returns:
        A Response object
    """
    return render_template(join("email", file), **args)
