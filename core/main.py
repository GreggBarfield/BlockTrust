import os
import json
import random
import sys

sys.path = [
    os.path.abspath(os.path.join(os.path.abspath(__file__), "..", ".."))
] + sys.path

debug_mode = False

if __name__ == "__main__":
    debug_mode = True

__name__ = "core.main"

from flask import (
    Flask, jsonify, request, render_template, session, redirect, url_for, g
)
from flask_cors import CORS
from flask_talisman import Talisman

from .config import *
from urllib.parse import unquote_plus
from .database.database import Database

from .blueprints import dashboard, outside, widgets, stripe, shop, employees

from .utilities.handlers import attach_handlers
from .utilities import auth


app = Flask(__name__)
app.secret_key = FLASK_SESSION_SECRET_KEY
Talisman(
    app,
    content_security_policy=CSP,
    force_https=False  # Handle at nginx in deployment
)
CORS(app)

attach_handlers(app)


@app.before_request
def before_request():
    """Per-request setup.

    TODO: Move database creation outside (before_first_request might be good)

    - Loads user from session
    """
    # Database
    if getattr(g, "db", None) is None:
        g.db = Database(MYSQL_CONFIG)

    if request.method == 'POST':
        g.api = True
    
    g.user = None
    g.employee = None
    g.account = None
    g.is_admin = 0
    g.is_employee_impersonating = 0
    auth.session_open()


@app.teardown_request
def teardown_request(err):
    """Per-request teardown.
    This runs regardless of errors, unlike after_request.

    - Clears user
    """
    # Clear the current user (this should be done in before_request too for security reasons)
    g.user = None
    db = g.pop("db", None)
    if db is not None:
        db.close()

app.register_blueprint(dashboard.bp)
app.register_blueprint(outside.bp)
app.register_blueprint(widgets.bp)
app.register_blueprint(stripe.bp)
app.register_blueprint(shop.bp)
app.register_blueprint(employees.bp)

if debug_mode:
    app.run(
        host="0.0.0.0",
        debug=True,
        port=5000
    )
