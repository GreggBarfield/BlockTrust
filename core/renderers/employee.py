from os.path import join
from flask import (
    render_template, g
)


def employee_render(file, args={}):
    """Renders a template from templates/employee.

    Params:
        file: file should be a path relative to employee/employee.
        args: context variables for jinja2

    Returns:
        A Response object

    Raises:
        ValueError: On 'args' conflicting with standard employee_standard_args
        ValueError: On the employee not being logged in

    """
    if g.employee is None:
        raise ValueError("Employee is not logged in")
    employee_standard_args = {
        "employee_standard_employee_first": g.employee.first_name(),
        "employee_standard_employee_last": g.employee.last_name()
    }
    for key in args:
        if key in employee_standard_args:
            raise ValueError(key + " cannot be in args since it is already in employee_standard_args")
    return render_template(join("employee", file), **employee_standard_args, **args)
