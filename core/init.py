import os
import json
import random
import sys
import traceback

try:
    sys.path = [
        os.path.abspath(os.path.join(os.path.abspath(__file__), "..", ".."))
    ] + sys.path
    print(sys.path)
    # PACKAGE_PARENT = '..'
    # SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    # sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

    # debug_mode = False

    # if __name__ == "__main__":
    #     debug_mode = True

    __name__ = "core.main"

    from flask import (
        Flask, jsonify, request, render_template, session, redirect, url_for, g
    )
    from flask_cors import CORS
    from flask_talisman import Talisman

    from .config import *
    from urllib.parse import unquote_plus
    from .database.database import Database

    from .blueprints import dashboard
    from .blueprints import outside
    from .blueprints import widgets
    from .blueprints import stripe
    from .blueprints import shop

    from .utilities.handlers import attach_handlers
    from .utilities import auth

    def create_app():
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
            g.account = None
            g.is_admin = None
            auth.session_open()


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
        app.register_blueprint(stripe.bp)
        app.register_blueprint(shop.bp)
        return app

    if __name__ == "core.main":
        app = create_app()
        app.run(
                host="0.0.0.0",
                debug=True,
                port=5000
        )

except Exception as e:
    print(e, traceback.format_exc())
