# Yes, it's messy; I know
# Full steam ahead; we'll clean it up when we redesign everything

import os
import json
import random

from flask import (
    Flask, jsonify, request, render_template, session, redirect, url_for, g
)
from flask_cors import CORS
from flask_talisman import Talisman

from config import *
from urllib.parse import unquote_plus
from database.database import Database

from blueprints import dashboard
from blueprints import outside
from blueprints import widgets

app = Flask(__name__)
app.secret_key = FLASK_SESSION_SECRET_KEY
Talisman(
    app,
    content_security_policy={
        'default-src': [
            'https://js.stripe.com',
            'https://polyfill.io',
            'https://i.imgur.com',
            DOMAIN,
            '\'unsafe-inline\'',
            'fonts.gstatic.com',
            'fonts.googleapis.com'
        ]
    },
    force_https=False  # We don't want to serve HTTP in general
)
CORS(app)

@app.before_request
def before_request():
    """Per-request setup.

    TODO: Move database creation outside (before_first_request might be good)

    - Loads user from session
    """
    # Database
    if getattr(g, "db", None) is None:
        g.db = Database(MYSQL_CONFIG)
    
    g.user = None
    g.db.users.session_open()
    g.account = None
    g.db.accounts.session_open()


@app.teardown_request
def teardown_request(err):
    """Per-request teardown.
    This runs regardless of errors, unlike after_request.

    - Clears user
    """
    # Clear the current user (this should be done in before_request too for security reasons)
    g.user = None

app.register_blueprint(dashboard.bp)
app.register_blueprint(outside.bp)
app.register_blueprint(widgets.bp)

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        debug=True,
        port=443,
        ssl_context=(
            '/etc/letsencrypt/live/ledgerspacedev.com/fullchain.pem',
            '/etc/letsencrypt/live/ledgerspacedev.com/privkey.pem'
        )
    )
