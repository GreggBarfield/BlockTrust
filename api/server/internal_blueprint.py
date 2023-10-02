import json
import os
import gzip


from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect
)

from ..database.inserts_model import InsertsModel
from core.database.tables.matches import Matches
from core.database.database import Database
from core.config import MYSQL_CONFIG, API_MYSQL_CONFIG, INTERNAL_API_SECRET
from core.common_exceptions import ExportException


bp = Blueprint('internal_blueprint', __name__)


@bp.before_request
def before_request():
    """Per-request setup."""
    g.db = Database(MYSQL_CONFIG)


@bp.route('/api/ils-eids/<secret>', methods=["POST", "GET"])
def serve_api_eids(secret):

    if secret != INTERNAL_API_SECRET:
        print(secret)
        raise ExportException("Bad internal API secret")

    eids = Matches(g.db).get_ils_eids()

    return {
        "eids": eids
    }, 200
