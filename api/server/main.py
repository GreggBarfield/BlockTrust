from datetime import timedelta
import os
import sys


sys.path = [
    os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", ".."))
] + sys.path

run_dev_server = False

if __name__ == "__main__":
    run_dev_server = True

__name__ = "api.server.main"


from flask import (
    Flask
)
from flask_jwt_extended import JWTManager

app = Flask(__name__, template_folder=os.path.abspath('core/templates'))
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "super-secret")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
jwt = JWTManager(app)


from . import input_blueprint
from . import internal_blueprint
from . import external_blueprint
from core.common_exceptions import ExportException


app.register_blueprint(input_blueprint.bp)
app.register_blueprint(internal_blueprint.bp)
app.register_blueprint(external_blueprint.bp)


@app.errorhandler(ExportException)
def handle_export_exception(e):
    return {
        "error": str(e)
    }, 400


if run_dev_server:
    app.run(
        host="0.0.0.0",
        debug=True,
        port=80
    )
