from flask import (
    Blueprint
)
from ..utilities import crut, auth


bp = Blueprint('employees_bp', __name__)

@bp.route('/employee/dashboard', methods=['GET'])
@crut.require_employee
def serve_employee_dashboard():    
    return "<h1>Employee is logged in</h1>"

#Employee routes go here.... 