import pytest
from unittest import TestCase
from unittest.mock import Mock, patch, call
from ....exceptions import ExecutionException

# Don't remove the H
# If you do, make sure to run pytest again and check for warnings
from ..TestTY import TestTYType as HTestTYType


class TestTestTY(TestCase):

    def test_block_key_block_nonsys(self):
        mdb = Mock()
        minserts = Mock()

        with self.assertRaises(RuntimeError):
            d = {
                "account": 0
            }

            handler = HTestTYType(mdb, minserts, d)

            handler.block_key()

        with self.assertRaises(RuntimeError):
            d = {
                "account": 5
            }

            handler = HTestTYType(mdb, minserts, d)

            handler.block_key()

    def test_block_key_block_val(self):
        mdb = Mock()
        minserts = Mock()

        d = {
            "account": -3,
            "fields": {
                "key": "gse4es4tse4"
            }
        }

        handler = HTestTYType(mdb, minserts, d)
        self.assertEqual(handler.block_key(), d["fields"]["key"])

        d = {
            "account": -3,
            "fields": {
            }
        }

        handler = HTestTYType(mdb, minserts, d)
        self.assertIs(handler.block_key(), None)

    def test_handle_nothing(self):
        mdb = Mock()
        minserts = Mock()

        d = {
            "fields": {

            }
        }

        handler = HTestTYType(mdb, minserts, d)
        handler.handle()

        self.assertListEqual(handler.emitted_blocks, [])

    def test_handle_emit(self):
        mdb = Mock()
        minserts = Mock()

        d = {
            "fields": {
                "emit": "asdf",
                "emit_key": "gaw34w"
            }
        }

        handler = HTestTYType(mdb, minserts, d)
        handler.handle()

        self.assertListEqual(handler.emitted_blocks, [("gaw34w", "asdf")])
