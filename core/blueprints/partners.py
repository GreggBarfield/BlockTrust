from flask import (
    Blueprint, g, request
)
from ..renderers.partner import partner_render
from ..utilities import crut, csrf

bp = Blueprint('partner_bp', __name__, url_prefix="/partner")


@bp.route('/dashboard', methods=['GET'])
@crut.require_partner
def serve_dashboard():
    return partner_render("main.html")
