from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect, url_for
)
from ..renderers.internal import internal_render
from ..sectors import sectors_by_id

bp = Blueprint('internal_bp', __name__)


@bp.route("/internal/dashboard", methods=["GET"])
def serve_internal_dashboard():
    return internal_render("/internal/accounts/homepage.html")


@bp.route("/internal/create-new-account", methods=["GET"])
def serve_internal_create_account():
    partners = g.db.accounts.get_partners()
    return internal_render("/internal/accounts/create-new-account.html", {"sectors_by_id": sectors_by_id, "partners": partners})
