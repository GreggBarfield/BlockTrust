import pytest
from unittest import TestCase
from unittest.mock import Mock, patch, call
from core.database.objects.match import MatchFactory
from ....exceptions import ExecutionException

from ..Packer import PackerType


class TestPacker(TestCase):

    def test_block_key(self):
        mdb = Mock()
        minserts = Mock()

        d = {}

        handler = PackerType(mdb, minserts, d)

        self.assertIs(handler.block_key(), None)

    def test_handle_1(self):
        mdb = Mock()
        f = MatchFactory(mdb)
        mdb.matches.factory = f
        minserts = Mock()

        d = {
            "account": 62,
            "fields": {
                "EIDNum": "982000418411463",
                "Packer": "Tyson",
                "Company": "kni",
                "DeadInd": "0",
                "EIDDate": "3/13/2019 12:00:00 AM",
                "PlantID": "010",
                "RailCause": "0",
                "RailedInd": "0",
                "DeathCause": "0",
                "CarcassWeight": "767",
                "TreatmentCount": "0",
                "USDAYieldGrade": "4.0",
                "USDAQualityGrade": "Choice"
            }
        }

        companyILS = Mock()
        company2 = Mock()

        mdb.account_links.get_by_company.side_effect = [[companyILS], [company2]]

        handler = PackerType(mdb, minserts, d)
        handler.handle()

        self.assertListEqual(
            handler.emitted_matches,
            [
                f.create_sighting(
                    eid=982000418411463,
                    account_id=62,
                    account_link_id=companyILS.id.return_value,
                ),
                f.create_sighting(
                    eid=982000418411463,
                    account_id=62,
                    account_link_id=company2.id.return_value,
                ),
                f.create_usda_yield_grade(
                    eid=982000418411463,
                    account_id=62,
                    grade=4
                ),
                f.create_usda_quality_grade(
                    eid=982000418411463,
                    account_id=62,
                    grade="Choice"
                ),
                f.create_packer(
                    eid=982000418411463,
                    account_id=62,
                    packer_str="Tyson;010"
                ),
            ]
        )

        self.assertListEqual(
            handler.emitted_blocks,
            []
        )
