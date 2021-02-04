import os
import json
import random
import sys

sys.path = [
    os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", ".."))
] + sys.path

__name__ = "api.translation_worker.main"

from core.config import *  # noqa
from core.database.database import Database  # noqa


db = Database(MYSQL_CONFIG)

from .logistics import run  # noqa
from .inserts_model import InsertsModel  # noqa


run(
    db,
    InsertsModel(
        json.load(open(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "..",
            "env_cfg.json"
        )))['api_mysql']
    )
)
