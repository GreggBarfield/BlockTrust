import os
import json
import random
import sys

sys.path = [
    os.path.abspath(os.path.join(os.path.abspath(__file__), "..", ".."))
] + sys.path

__name__ = "reports_worker.main"

from core.config import *  # noqa
from core.database.database import Database  # noqa


db = Database(MYSQL_CONFIG)

from .logistics import run  # noqa

run(db)
