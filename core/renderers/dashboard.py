from os.path import join
from flask import (
    render_template, g
)
from core.config import DOMAIN

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
    dashboard_standard_args = {
        "dashboard_standard_user_first": g.user.first_name(),
        "dashboard_standard_user_last": g.user.last_name(),
        "dashboard_standard_user_username": g.user.username(),
        "dashboard_standard_account": g.account,
        "dashboard_standard_is_admin": g.is_admin,
        "dashboard_is_employee_impersonating": g.is_employee_impersonating,
        "enable_google_analytics": True if DOMAIN == "blocktrustnetwork.com" else False
    }
    for key in args:
        if key in dashboard_standard_args:
            raise ValueError(key + " cannot be in args since it is already in dashboard_standard_args")
    return render_template(join("dashboard", file), **dashboard_standard_args, **args)

