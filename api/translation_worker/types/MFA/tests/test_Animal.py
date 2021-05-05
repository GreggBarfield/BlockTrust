import pytest
from unittest import TestCase
from unittest.mock import Mock, patch, call
from core.database.objects.match import MatchFactory
from ....exceptions import ExecutionException

from ..Animal import AnimalType


class TestAnimal(TestCase):

    def test_block_key(self):
        mdb = Mock()
        minserts = Mock()

        d = {}

        handler = AnimalType(mdb, minserts, d)

        self.assertIs(handler.block_key(), None)

    def test_handle_1(self):
        mdb = Mock()
        f = MatchFactory(mdb)
        mdb.matches.factory = f
        minserts = Mock()

        d = {
            "account": 62,
            "fields": {
                "Dam": "",
                "EID": "982000423833010",
                "Sire": "",
                "Owner": "JRI",
                "UserID": 20152,
                "BrandID": "",
                "BreedID": 1,
                "TatooID": "",
                "AnimalID": "ff48a617-efe8-4b87-8cc9-7d09f62839c0",
                "DonorCow": "",
                "IsActive": True,
                "VisualID": "E241",
                "WeanDate": "",
                "Birthdate": "2017-10-26T00:00:00",
                "CalfSexID": 1,
                "DeathDate": "",
                "TennantID": 10170,
                "LocationID": "0cfc7453-d915-4983-b8fb-c7a751eea506",
                "BirthWeight": 65,
                "DamAnimalID": "e5b2c5ce-552d-4312-9e20-dca855121bea",
                "HideColorID": 2,
                "AlternateID1": "33010",
                "AlternateID2": "",
                "AnimalTypeID": 3,
                "SireAnimalID": "",
                "AnimalGroupID": "29bbc3a3-56e0-4d75-932a-08d5aed911ed",
                "BrandLocation": "",
                "TatooLocation": "",
                "CastrationDate": "",
                "EraseTimestamp": "",
                "ArchiveTimestamp": "",
                "CreatedTimestamp": "2018-06-27T15:57:35.32",
                "DonorCowAnimalID": "",
                "ModifiedTimestamp": "2019-01-14T20:14:44.323",
                "CastrationMethodID": "",
                "RegistrationNumber": "",
                "OrganizationalUnitID": 10153,
                "ArtificialInseminationBullInventoryID": ""
            }
        }

        handler = AnimalType(mdb, minserts, d)
        handler.handle()

        self.assertListEqual(
            handler.emitted_matches,
            [
                f.create_visual_id(
                    account_id=62,
                    visual_id="E241",
                    eid=982000423833010
                ),
                f.create_born(
                    account_id=62,
                    time=1508976000.0,
                    eid=982000423833010
                )
            ]
        )

        self.assertListEqual(
            handler.emitted_blocks,
            [
                ("MFA:ANEID:62:ff48a617-efe8-4b87-8cc9-7d09f62839c0", "982000423833010")
            ]
        )
