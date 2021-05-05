import pytest
from unittest import TestCase
from unittest.mock import Mock, patch, call
from core.database.objects.match import MatchFactory
from ....exceptions import ExecutionException

from ..AnimalsCSV import AnimalsCSVType


class TestAnimalsCSV(TestCase):

    def test_block_key(self):
        mdb = Mock()
        minserts = Mock()

        d = {}

        handler = AnimalsCSVType(mdb, minserts, d)

        self.assertIs(handler.block_key(), None)

    def test_handle_1(self):
        mdb = Mock()
        f = MatchFactory(mdb)
        mdb.matches.factory = f
        minserts = Mock()

        d = {
            "account": 62,
            "fields": {
                "sex": "",
                "hide": "",
                "farmid": "",
                "appdate": "09/20/2017 21:07:28",
                "file_id": "HEALTHTRACKANIMAL_2020618152340",
                "sponsor": "MFA",
                "st_time": "06/18/2020 20:23:03",
                "zipcode": "63552-0340",
                "end_time": "12/31/9999 23:59:59",
                "patronid": "543493",
                "sequence": "5418",
                "visualid": "05356",
                "weandate": "09/11/2017 10:00:00",
                "creepfeed": "Full Throttle",
                "file_date": "06/18/20",
                "applicatio": "12400",
                "birthweigh": "0",
                "block_acct": "100022",
                "calfbirthd": "01/01/01 12:00:00 AM",
                "calfdescri": "",
                "dtimestamp": "08/27/2020 22:37:42",
                "electronic": "982000422205356",
                "estimateds": "0",
                "first14da1": "Self Fed",
                "first14day": "",
                "firstbirth": "01/26/2017 12:00:00",
                "isvetproce": "True",
                "marketingd": "01/01/0001 00:00:00",
                "marketingm": "",
                "numberofca": "0",
                "salelocati": "",
                "second31d1": "Self Fed",
                "second31da": "Cadence and Corn",
                "weaningstr": "Ranch of Origin",
                "weanweight": ""
            }
        }

        company = Mock()

        mdb.account_links.get_by_uid.side_effect = [[company]]

        handler = AnimalsCSVType(mdb, minserts, d)
        handler.handle()

        self.assertListEqual(
            handler.emitted_matches,
            [
                f.create_visual_id(
                    eid=982000422205356,
                    account_id=62,
                    account_link_id=company.id.return_value,
                    visual_id="05356"
                ),
                f.create_weaned(
                    eid=982000422205356,
                    account_id=62,
                    time=1505124000.0,
                    account_link_id=company.id.return_value,
                    data={
                        "at": "Ranch of Origin",
                        "creep_feed": "Full Throttle",
                        "first_14_method": "Self Fed",
                        "second_31_feed": "Cadence and Corn",
                        "second_31_method": "Self Fed"
                    }
                ),
                f.create_born(
                    eid=982000422205356,
                    account_id=62,
                    time=1485432000.0,
                    account_link_id=company.id.return_value,
                ),
            ]
        )

        self.assertListEqual(
            handler.emitted_blocks,
            []
        )
