from os.path import join
from flask import (
    render_template, g, url_for
)
from core.config import DOMAIN
from core.sectors import SECTORS_NAME_TO_ID


def partner_render(file, args={}):
    """Renders a template from templates.

    Params:
        file: file should be a path relative to templates.
        args: context variables for jinja2

    Returns:
        A Response object

    Raises:
        ValueError: On 'args' conflicting with standard dashboard_standard_args
        ValueError: On the user not being logged in

    """
    if g.user is None:
        raise ValueError("user is not logged in")
    partner_args = {
        "partner_user_first": g.user.first_name(),
        "partner_user_last": g.user.last_name(),
        "partner_user_username": g.user.username(),
        "partner": g.account,
        "partner_is_admin": g.is_admin,
        "partner_is_employee": "employee_id" in g,
        "partner_logout": url_for("outside_bp.serve_logout"),
        "partner_edit_user": url_for("partner_bp.serve_edit_user")
    }
    for key in args:
        if key in partner_args:
            raise ValueError(key + " cannot be in args since it is already in dashboard_standard_args")
    return render_template(join("partner", file), **partner_args, **args)
