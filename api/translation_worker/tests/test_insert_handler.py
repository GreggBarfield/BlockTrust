import pytest
from unittest import TestCase
from unittest.mock import Mock, patch, call
from ..insert_handler import (
    InsertHandlerErrorBadType,
    InsertHandlerErrorBlocked,
    handle_insert
)
from ..exceptions import ExecutionException


class TestInsertHandler(TestCase):

    def test_bad_ns_type(self):
        mdb = Mock()
        minserts = Mock()
        n1t1mock = Mock()

        with patch(
            "api.translation_worker.insert_handler.types_lookup",
            {
                ("n1", "t1"): n1t1mock,
                ("n2", "t2"): "on2t2"
            }
        ):
            with pytest.raises(InsertHandlerErrorBadType):
                handle_insert(
                    mdb,
                    minserts,
                    {
                        "namespace": "n1",
                        "type": "5"
                    }
                )
            with pytest.raises(InsertHandlerErrorBadType):
                handle_insert(
                    mdb,
                    minserts,
                    {
                        "namespace": "n6",
                        "type": "5"
                    }
                )
            with pytest.raises(InsertHandlerErrorBadType):
                handle_insert(
                    mdb,
                    minserts,
                    {
                        "namespace": "ee",
                        "type": "t1"
                    }
                )
            n1t1mock.side_effect = AssertionError
            with pytest.raises(AssertionError):
                handle_insert(
                    mdb,
                    minserts,
                    {
                        "namespace": "n1",
                        "type": "t1"
                    }
                )
            self.assertTrue(n1t1mock.called)

    def test_block_key_available_searched(self):
        mdb = Mock()
        minserts = Mock()
        n1t1mock = Mock()
        handler = n1t1mock.return_value

        with patch(
            "api.translation_worker.insert_handler.types_lookup",
            {
                ("n1", "t1"): n1t1mock,
                ("n2", "t2"): "on2t2"
            }
        ):
            insert_dict = {
                "id": 623,
                "namespace": "n1",
                "type": "t1",
                "api_blocks.resolved": None
            }

            handler.block_key.return_value = "asdfj43g"
            minserts.blocked_on.return_value = 65

            emitted_matches, emitted_blocks = handle_insert(
                mdb,
                minserts,
                insert_dict
            )

            self.assertEqual(emitted_matches, handler.emitted_matches)
            self.assertEqual(emitted_blocks, handler.emitted_blocks)
            self.assertEqual(65, handler.block_value)

            self.assertListEqual(minserts.blocked_on.call_args_list, [call(
                "asdfj43g",
                623
            )])

            self.assertListEqual(n1t1mock.call_args_list, [call(
                db=mdb,
                inserts_model=minserts,
                insert=insert_dict
            )])

    def test_block_key_none(self):
        mdb = Mock()
        minserts = Mock()
        n1t1mock = Mock()
        handler = n1t1mock.return_value

        with patch(
            "api.translation_worker.insert_handler.types_lookup",
            {
                ("n1", "t1"): n1t1mock,
                ("n2", "t2"): "on2t2"
            }
        ):
            insert_dict = {
                "id": 623,
                "namespace": "n1",
                "type": "t1",
                "api_blocks.resolved": None
            }

            handler.block_key.return_value = None

            emitted_matches, emitted_blocks = handle_insert(
                mdb,
                minserts,
                insert_dict
            )

            self.assertEqual(emitted_matches, handler.emitted_matches)
            self.assertEqual(emitted_blocks, handler.emitted_blocks)
            self.assertEqual(None, handler.block_value)

            self.assertListEqual(minserts.blocked_on.call_args_list, [])

            self.assertListEqual(n1t1mock.call_args_list, [call(
                db=mdb,
                inserts_model=minserts,
                insert=insert_dict
            )])

    def test_block_key_api_resolved(self):
        mdb = Mock()
        minserts = Mock()
        n1t1mock = Mock()
        handler = n1t1mock.return_value

        with patch(
            "api.translation_worker.insert_handler.types_lookup",
            {
                ("n1", "t1"): n1t1mock,
                ("n2", "t2"): "on2t2"
            }
        ):
            insert_dict = {
                "id": 623,
                "namespace": "n1",
                "type": "t1",
                "api_blocks.resolved": 1,
                "api_blocks.value": 6223
            }

            handler.block_key.return_value = "g4sew4ser"

            emitted_matches, emitted_blocks = handle_insert(
                mdb,
                minserts,
                insert_dict
            )

            self.assertEqual(emitted_matches, handler.emitted_matches)
            self.assertEqual(emitted_blocks, handler.emitted_blocks)
            self.assertEqual(6223, handler.block_value)

            self.assertListEqual(minserts.blocked_on.call_args_list, [])

            self.assertListEqual(n1t1mock.call_args_list, [call(
                db=mdb,
                inserts_model=minserts,
                insert=insert_dict
            )])
