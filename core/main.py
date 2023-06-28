import os
import sys

sys.path = [
    os.path.abspath(os.path.join(os.path.abspath(__file__), "..", ".."))
] + sys.path

debug_mode = False

if __name__ == "__main__":
    debug_mode = True

__name__ = "core.main"

from flask import (
    Flask, request, g
)
from flask_cors import CORS
from flask_talisman import Talisman
from flask_qrcode import QRcode

from .config import *
from .database.database import Database

from .blueprints import dashboard, outside, widgets, stripe, shop, employees, partners

from .utilities.handlers import attach_handlers
from .utilities import auth, csrf

app = Flask(__name__)
app.secret_key = FLASK_SESSION_SECRET_KEY
Talisman(
    app,
    content_security_policy=CSP,
    force_https=False  # Handle at nginx in deployment
)
CORS(app)
qrcode = QRcode(app)

attach_handlers(app)
csrf.add_csrf(app)

@app.before_request
def before_request():
    """Per-request setup.

    TODO: Move database creation outside (before_first_request might be good)

    - Loads user from session
    """
    # Database
    if getattr(g, "db", None) is None:
        g.db = Database(MYSQL_CONFIG)

    auth.load_app_context_from_session()


@app.teardown_request
def teardown_request(err):
    """Per-request teardown.
    This runs regardless of errors, unlike after_request.

    - Clears user
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()


app.register_blueprint(dashboard.bp)
app.register_blueprint(outside.bp)
app.register_blueprint(widgets.bp)
app.register_blueprint(stripe.bp)
app.register_blueprint(shop.bp)
app.register_blueprint(employees.bp)
app.register_blueprint(partners.bp)

if debug_mode:
    app.run(
        host="0.0.0.0",
        debug=True,
        port=5000
    )
