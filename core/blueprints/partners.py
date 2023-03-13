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


@bp.route('/edit-user', methods=['GET'])
@crut.require_partner
@csrf.csrf_protect
def serve_edit_user():
    user = g.db.users.get_by_username(g.user.username())
    return partner_render("/partner/edit-user.html", {
        "user": user, "is_website_admin": False
    })
