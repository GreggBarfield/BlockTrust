import pytest
from unittest import TestCase
from unittest.mock import Mock, patch, call
from core.database.objects.match import MatchFactory
from ....exceptions import ExecutionException

from ..MatchTableCSV import MatchTableCSVType


class TestMatchTableCSV(TestCase):

    def test_block_key(self):
        mdb = Mock()
        minserts = Mock()

        d = {}

        handler = MatchTableCSVType(mdb, minserts, d)

        self.assertIs(handler.block_key(), None)

    def test_handle_1(self):
        mdb = Mock()
        f = MatchFactory(mdb)
        mdb.matches.factory = f
        minserts = Mock()

        d = {
            "account": 62,
            "fields": {
                "eid": "982000418411463",
                "au_lat": "",
                "cc_lat": "38.9776",
                "fd_lat": "38.39129",
                "pk_lat": "37.98909",
                "au_acct": "0",
                "au_date": "  -   -",
                "au_long": "",
                "au_name": "",
                "cc_acct": "1029",
                "cc_date": "2/19/2018",
                "cc_long": "-93.5812",
                "cc_name": "Ranch 1029",
                "fd_acct": "10",
                "fd_date": "3/12/2019",
                "fd_long": "-98.17608",
                "fd_name": "Knight Feedlot",
                "pk_acct": "10",
                "pk_date": "3/13/2019",
                "pk_long": "-100.98816",
                "pk_name": "Tyson Meats",
                "au_cityst": "",
                "fd_cityst": "Lyons, KS",
                "pk_cityst": "Holcomb, KS"
            }
        }

        companycc = Mock()
        companyfd = Mock()
        companypk = Mock()
        companyau = Mock()

        mdb.account_links.get_by_company.side_effect = [
            [companycc], [companyfd], [companypk], [companyau]
        ]

        handler = MatchTableCSVType(mdb, minserts, d)
        handler.handle()

        print('\n'.join([str(m) for m in handler.emitted_matches]))

        self.assertListEqual(
            handler.emitted_matches,
            [
                f.create_sighting(
                    eid=982000418411463,
                    account_id=62,
                    account_link_id=companycc.id.return_value,
                    lat="38.9776",
                    lon="-93.5812",
                    time=1518998400.0
                ),
                f.create_sighting(
                    eid=982000418411463,
                    account_id=62,
                    account_link_id=companyfd.id.return_value,
                    lat="38.39129",
                    lon="-98.17608",
                    time=1552348800.0
                ),
                f.create_sighting(
                    eid=982000418411463,
                    account_id=62,
                    account_link_id=companypk.id.return_value,
                    lat="37.98909",
                    lon="-100.98816",
                    time=1552435200.0
                ),
            ]
        )

        self.assertListEqual(
            mdb.account_links.get_by_company.call_args_list,
            [
                call('Ranch 1029', insert_sector=4, insert=True),
                call('Knight Feedlot', insert_sector=6, insert=True),
                call('Tyson Meats', insert_sector=7, insert=True)
            ]
        )

        self.assertListEqual(
            handler.emitted_blocks,
            []
        )
