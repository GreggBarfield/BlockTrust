from os.path import join
from flask import (
    render_template, g
)
from core.config import DOMAIN
from core.sectors import SECTORS_NAME_TO_ID


def dashboard_render(file, args={}):
    """Renders a template from templates/dashboard.

    Params:
        file: file should be a path relative to templates/dashboard.
        args: context variables for jinja2

    Returns:
        A Response object

    Raises:
        ValueError: On 'args' conflicting with standard dashboard_standard_args
        ValueError: On the user not being logged in

    """
    if g.user is None:
        raise ValueError("user is not logged in")
    partner_account = (g.db.accounts.get_accounts(id=g.account.partner_account_id())[0]
                       if g.account.partner_account_id() else None)
    dashboard_standard_args = {
        "dashboard_standard_user_first": g.user.first_name(),
        "dashboard_standard_user_last": g.user.last_name(),
        "dashboard_standard_user_username": g.user.username(),
        "dashboard_standard_account": g.account if "account" in g else None,
        "dashboard_standard_is_admin": g.is_admin if "is_admin" in g else None,
        "dashboard_is_employee": "employee_id" in g,
        "dashboard_is_partner": "impersonated_by_user_id" in g,
        "dashboard_logo": partner_account["partner_private_logo"],
        "dashboard_color": partner_account["partner_color"],
        "enable_google_analytics": True if DOMAIN == "blocktrustnetwork.com" else False,
        "sectors_name_to_id": SECTORS_NAME_TO_ID
    }
    for key in args:
        if key in dashboard_standard_args:
            raise ValueError(key + " cannot be in args since it is already in dashboard_standard_args")
    return render_template(join("dashboard", file), **dashboard_standard_args, **args)
