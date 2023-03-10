from os.path import join
from flask import (
    render_template, g, url_for
)
from ..config import DOMAIN

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
    if "user" in g:
        if "account" in g and g.account.is_partner():
            dashboard_URL = url_for("partner_bp.serve_dashboard")
        else:
            dashboard_URL = url_for("dashboard_bp.serve_dashboard")
    else:
        dashboard_URL = url_for("employee_bp.serve_dashboard")

    outside_standard_args = {
        "outside_standard_user_username": g.user.username() if "user" in g else "",
        "outside_standard_logged_in": "user" in g or "employee" in g,
        "outside_standard_employee_username": g.employee.username() if "employee" in g else "",
        "enable_google_analytics": True if DOMAIN == "blocktrustnetwork.com" else False,
        "outside_standard_dashboard_URL": dashboard_URL
    }

    for key in args:
        if key in outside_standard_args:
            raise ValueError(key + " cannot be in args since it is already in outside_standard_args")
    return render_template(join("outside", file), **outside_standard_args, **args)
