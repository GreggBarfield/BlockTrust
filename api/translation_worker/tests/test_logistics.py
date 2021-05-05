import pytest
from unittest import TestCase
from unittest.mock import Mock, patch, call
from ..insert_handler import (
    InsertHandlerErrorBadType,
    InsertHandlerErrorBlocked
)
from core.config import (
    BLOCKCHAIN_TRANSLATION_WORKER_UPLOADS,
    BLOCKCHAIN_RECOMMENDED_BATCH_SIZE
)
from ..exceptions import ExecutionException
from ..logistics import run, _get_batch, _submit_batch


# Extensive tests due to expensive empirical calls.


class SleepThrowAfter(Exception):
    pass


def throwAfter(exception_class, num_times):
    for i in range(num_times):
        yield
    raise exception_class()


class TestLogistics(TestCase):

    # Test run

    @patch("api.translation_worker.logistics.sleep")
    @patch("api.translation_worker.logistics.handle_insert")
    @patch("api.translation_worker.logistics.transmit")
    def test_run_bad_batch_size(self, mtransmit, mhandle_insert, msleep):
        with pytest.raises(ValueError):
            run(Mock(), Mock(), blockchain_recommended_batch_size=0)
        with pytest.raises(ValueError):
            run(Mock(), Mock(), blockchain_recommended_batch_size=-1)
        with pytest.raises(ValueError):
            run(Mock(), Mock(), blockchain_recommended_batch_size=-5000)

    @patch("api.translation_worker.logistics._get_batch")
    @patch("api.translation_worker.logistics._submit_batch")
    @patch("api.translation_worker.logistics.sleep")
    @patch("api.translation_worker.logistics.handle_insert")
    @patch("api.translation_worker.logistics.transmit")
    def test_run_single(self, mtransmit, mhandle_insert, msleep, msubmit, mget):
        minserts_model = Mock()
        mdb = Mock()

        mget.return_value = (Mock(), Mock(), Mock())

        minserts_model.get_by_id.return_value = None

        run(mdb, minserts_model, insert_id=63)

        self.assertFalse(mhandle_insert.emit_block.called)
        self.assertListEqual(
            mget.call_args_list,
            [
                call(
                    db=mdb,
                    inserts_model=minserts_model,
                    verbose=False,
                    insert_id=63,
                    blockchain_recommended_batch_size=BLOCKCHAIN_RECOMMENDED_BATCH_SIZE
                )
            ]
        )
        self.assertListEqual(
            msubmit.call_args_list,
            [
                call(
                    db=mdb,
                    inserts_model=minserts_model,
                    verbose=False,
                    batch_insert_ids=mget.return_value[0],
                    batch_emitted_matches=mget.return_value[1],
                    batch_emitted_blocks=mget.return_value[2],
                )
            ]
        )
        self.assertFalse(msleep.called)

    @patch("api.translation_worker.logistics._get_batch")
    @patch("api.translation_worker.logistics._submit_batch")
    @patch("api.translation_worker.logistics.sleep")
    @patch("api.translation_worker.logistics.handle_insert")
    @patch("api.translation_worker.logistics.transmit")
    def test_run_multi(self, mtransmit, mhandle_insert, msleep, msubmit, mget):
        minserts_model = Mock()
        mdb = Mock()

        mget_yields = [
            ([], [Mock()], [Mock()]),
            ([5, 6, 1], [Mock()], [Mock()]),
            ([8, 2, 3], [Mock()], [Mock()]),
            ([], [Mock()], [Mock()]),
            ([], [Mock()], [Mock()]),
            ([], [Mock()], [Mock()]),
            ([], [Mock()], [Mock()]),
            ([], [Mock()], [Mock()]),
            ([], [Mock()], [Mock()]),
            ([], [Mock()], [Mock()]),
            ([], [Mock()], [Mock()]),
            ([8], [Mock()], [Mock()]),
            ([], [Mock()], [Mock()]),
            ([], [Mock()], [Mock()])
        ]

        sleep_count = 11

        mget.side_effect = mget_yields
        msleep.side_effect = throwAfter(SleepThrowAfter, sleep_count - 1)

        minserts_model.get_by_id.return_value = None

        with pytest.raises(SleepThrowAfter):
            run(mdb, minserts_model)

        self.assertFalse(mhandle_insert.emit_block.called)
        self.assertListEqual(
            mget.call_args_list,
            [
                call(
                    db=mdb,
                    inserts_model=minserts_model,
                    verbose=False,
                    insert_id=None,
                    blockchain_recommended_batch_size=BLOCKCHAIN_RECOMMENDED_BATCH_SIZE
                ) for i in range(len(mget_yields))
            ]
        )
        self.assertListEqual(
            msubmit.call_args_list,
            [
                call(
                    db=mdb,
                    inserts_model=minserts_model,
                    verbose=False,
                    batch_insert_ids=mget_yields[i][0],
                    batch_emitted_matches=mget_yields[i][1],
                    batch_emitted_blocks=mget_yields[i][2],
                ) for i in range(len(mget_yields))
            ]
        )
        self.assertEqual(msleep.call_count, sleep_count)

    # Test submit batch

    @patch("api.translation_worker.logistics.handle_insert")
    @patch("api.translation_worker.logistics.transmit")
    def test_submit_empty_ids(self, mtransmit, mhandle_insert):
        minserts_model = Mock()
        mdb = Mock()

        mock_match = Mock()

        _submit_batch(mdb, minserts_model, [], [mock_match], [Mock()], False, True)
        _submit_batch(mdb, minserts_model, [], [mock_match], [Mock()], False, False)
        _submit_batch(mdb, minserts_model, [], [], [], False, True)
        _submit_batch(mdb, minserts_model, [], [], [], False, False)

        self.assertFalse(mtransmit.called)
        self.assertFalse(mock_match.generate_bc_hash.called)

    @patch("api.translation_worker.logistics.handle_insert")
    @patch("api.translation_worker.logistics.transmit")
    def test_submit_good_no_blockchain(self, mtransmit, mhandle_insert):
        minserts_model = Mock()
        mdb = Mock()

        mock_match1 = Mock()
        mock_match1.generate_bc_hash.return_value = 1
        mock_match2 = Mock()
        mock_match2.generate_bc_hash.return_value = 2
        mock_match3 = Mock()
        mock_match3.generate_bc_hash.return_value = 3

        _submit_batch(
            mdb,
            minserts_model,
            [53, 6, 7],
            [mock_match1, mock_match3, mock_match2],
            [(8, 3), (51, 12)],
            False,
            False
        )

        self.assertFalse(mtransmit.called)
        self.assertTrue(mdb.matches.insert_match_object.called)

    @patch("api.translation_worker.logistics.handle_insert")
    @patch("api.translation_worker.logistics.transmit")
    def test_submit_good_yes_blockchain(self, mtransmit, mhandle_insert):
        minserts_model = Mock()
        mdb = Mock()

        mock_match1 = Mock()
        mock_match1.generate_bc_hash.return_value = 1
        mock_match2 = Mock()
        mock_match2.generate_bc_hash.return_value = 2
        mock_match3 = Mock()
        mock_match3.generate_bc_hash.return_value = 3
        mock_match4 = Mock()
        mock_match4.generate_bc_hash.return_value = 4

        _submit_batch(
            mdb,
            minserts_model,
            [53, 6, 7],
            [mock_match1, mock_match3, mock_match2, mock_match4],
            [(8, 3), (51, 12)],
            False,
            True
        )

        self.assertListEqual(
            mtransmit.call_args_list,
            [
                call([1, 3, 2, 4])
            ]
        )

        self.assertListEqual(
            mdb.matches.insert_match_object.call_args_list,
            [
                call(mock_match1),
                call(mock_match3),
                call(mock_match2),
                call(mock_match4)
            ]
        )

        self.assertListEqual(
            minserts_model.emit_block.call_args_list,
            [
                call(8, 3),
                call(51, 12)
            ]
        )

        self.assertListEqual(
            minserts_model.set_status.call_args_list,
            [
                call(53, "Done"),
                call(6, "Done"),
                call(7, "Done"),
            ]
        )

        self.assertTrue(mock_match1.generate_bc_hash.called)
        self.assertEqual(mock_match1.bc_record, mtransmit.return_value)
        self.assertTrue(mock_match2.generate_bc_hash.called)
        self.assertEqual(mock_match2.bc_record, mtransmit.return_value)
        self.assertTrue(mock_match3.generate_bc_hash.called)
        self.assertEqual(mock_match3.bc_record, mtransmit.return_value)
        self.assertTrue(mock_match4.generate_bc_hash.called)
        self.assertEqual(mock_match4.bc_record, mtransmit.return_value)

    @patch("api.translation_worker.logistics.transmit")
    def test_submit_crash(self, mtransmit):
        minserts_model = Mock()
        mdb = Mock()

        minserts_model.set_status.side_effect = SleepThrowAfter

        mock_match1 = Mock()
        mock_match1.generate_bc_hash.return_value = 1
        mock_match2 = Mock()
        mock_match2.generate_bc_hash.return_value = 2
        mock_match3 = Mock()
        mock_match3.generate_bc_hash.return_value = 3
        mock_match4 = Mock()
        mock_match4.generate_bc_hash.return_value = 4

        with pytest.raises(SleepThrowAfter):
            _submit_batch(
                mdb,
                minserts_model,
                [53, 6, 7],
                [mock_match1, mock_match3, mock_match2, mock_match4],
                [(8, 3), (51, 12)],
                False,
                True
            )

        self.assertListEqual(
            mtransmit.call_args_list,
            [
                call([1, 3, 2, 4])
            ]
        )

        self.assertListEqual(
            mdb.matches.insert_match_object.call_args_list,
            [
                call(mock_match1),
                call(mock_match3),
                call(mock_match2),
                call(mock_match4)
            ]
        )

        self.assertListEqual(
            minserts_model.emit_block.call_args_list,
            [
                call(8, 3),
                call(51, 12)
            ]
        )

        self.assertListEqual(
            minserts_model.set_status.call_args_list,
            [call(53, "Done")]  # The first submission crashes the program
            # This is important! Everything else should happen BEFORE
            # 'Done' is marked!
        )

        self.assertTrue(mock_match1.generate_bc_hash.called)
        self.assertEqual(mock_match1.bc_record, mtransmit.return_value)
        self.assertTrue(mock_match2.generate_bc_hash.called)
        self.assertEqual(mock_match2.bc_record, mtransmit.return_value)
        self.assertTrue(mock_match3.generate_bc_hash.called)
        self.assertEqual(mock_match3.bc_record, mtransmit.return_value)
        self.assertTrue(mock_match4.generate_bc_hash.called)
        self.assertEqual(mock_match4.bc_record, mtransmit.return_value)

    # Test get batch

    @patch("api.translation_worker.logistics.handle_insert")
    def test_get_single_failed(self,  mhandle):
        minserts_model = Mock()
        mdb = Mock()

        minserts_model.get_by_id.return_value = None

        self.assertEqual(
            _get_batch(
                mdb,
                minserts_model,
                False,
                53,
                20
            ),
            ([], [], [])
        )

        self.assertFalse(minserts_model.get_next.called)
        self.assertFalse(mhandle.called)

    @patch("api.translation_worker.logistics.handle_insert")
    def test_get_multi_failed(self,  mhandle):
        minserts_model = Mock()
        mdb = Mock()

        minserts_model.get_next.return_value = None

        self.assertEqual(
            _get_batch(
                mdb,
                minserts_model,
                False,
                None,
                20
            ),
            ([], [], [])
        )

        self.assertFalse(minserts_model.get_by_id.called)
        self.assertFalse(mhandle.called)

    @patch("api.translation_worker.logistics.handle_insert")
    def test_get_single_good(self, mhandle):
        minserts_model = Mock()
        mdb = Mock()

        minserts_model.get_by_id.return_value = {"id": 62}
        mhandle.return_value = ([Mock(), Mock()], [Mock()])

        self.assertEqual(
            _get_batch(
                mdb,
                minserts_model,
                False,
                53,
                20
            ),
            ([62], mhandle.return_value[0], mhandle.return_value[1])
        )

        self.assertListEqual(
            mhandle.call_args_list,
            [call(mdb, minserts_model, minserts_model.get_by_id.return_value)]
        )
        self.assertFalse(minserts_model.get_next.called)

    @patch("api.translation_worker.logistics.handle_insert")
    def test_get_multi_full(self, mhandle):
        minserts_model = Mock()
        mdb = Mock()

        mnexte = [
            {"id": 62},
            {"id": 52},
            {"id": 63},
            {"id": 222}
        ]
        minserts_model.get_next.side_effect = mnexte
        mse = [
            ([Mock(), Mock()], [Mock()]),
            ([], []),
            ([Mock(), Mock(), Mock(), Mock(), Mock(), Mock()], [Mock(), Mock()]),
        ]
        mhandle.side_effect = mse

        self.assertEqual(
            _get_batch(
                mdb,
                minserts_model,
                False,
                None,
                3
            ),
            (
                [62, 52, 63],
                (
                    mse[0][0] + mse[1][0] +
                    mse[2][0]
                ),
                (
                    mse[0][1] + mse[1][1] +
                    mse[2][1]
                ),
            )

        )

        self.assertListEqual(
            mhandle.call_args_list,
            [
                call(mdb, minserts_model, mnexte[0]),
                call(mdb, minserts_model, mnexte[1]),
                call(mdb, minserts_model, mnexte[2])
            ]
        )
        self.assertFalse(minserts_model.get_by_id.called)
        self.assertFalse(minserts_model.set_status.called)

    @patch("api.translation_worker.logistics.handle_insert")
    def test_get_multi_not_full(self, mhandle):
        minserts_model = Mock()
        mdb = Mock()

        mnexte = [
            {"id": 62},
            {"id": 52},
            {"id": 63},
            None
        ]
        minserts_model.get_next.side_effect = mnexte
        mse = [
            ([Mock(), Mock()], [Mock()]),
            ([], []),
            ([Mock(), Mock(), Mock(), Mock(), Mock(), Mock()], [Mock(), Mock()]),
        ]
        mhandle.side_effect = mse

        self.assertEqual(
            _get_batch(
                mdb,
                minserts_model,
                False,
                None,
                50
            ),
            (
                [62, 52, 63],
                (
                    mse[0][0] + mse[1][0] +
                    mse[2][0]
                ),
                (
                    mse[0][1] + mse[1][1] +
                    mse[2][1]
                ),
            )

        )

        self.assertListEqual(
            mhandle.call_args_list,
            [
                call(mdb, minserts_model, mnexte[0]),
                call(mdb, minserts_model, mnexte[1]),
                call(mdb, minserts_model, mnexte[2])
            ]
        )
        self.assertFalse(minserts_model.get_by_id.called)
        self.assertFalse(minserts_model.set_status.called)

    @patch("api.translation_worker.logistics.handle_insert")
    def test_get_multi_exceptions(self, mhandle):
        minserts_model = Mock()
        mdb = Mock()

        mnexte = [
            {"id": 62},
            {"id": 52},
            {"id": 63},
            {"id": 222},
            {"id": 2232}
        ]
        minserts_model.get_next.side_effect = mnexte
        mse = [
            ([Mock(), Mock()], [Mock()]),
            None,
            None,
            None,
            ([Mock(), Mock(), Mock(), Mock(), Mock(), Mock()], [Mock(), Mock()]),
        ]
        mse_raises = [
            None,
            InsertHandlerErrorBadType(),
            InsertHandlerErrorBlocked(),
            ExecutionException(),
            None
        ]
        returnraisei = -1

        def returnRaise(*args, **kwargs):
            nonlocal returnraisei, mse, mse_raises
            returnraisei += 1
            if mse_raises[returnraisei]:
                raise mse_raises[returnraisei]
            else:
                return mse[returnraisei]

        mhandle.side_effect = returnRaise

        self.assertEqual(
            _get_batch(
                mdb,
                minserts_model,
                False,
                None,
                5
            ),
            (
                [62, 2232],
                (
                    mse[0][0] + mse[4][0]
                ),
                (
                    mse[0][1] + mse[4][1]
                ),
            )

        )

        self.assertListEqual(
            mhandle.call_args_list,
            [
                call(mdb, minserts_model, mnexte[0]),
                call(mdb, minserts_model, mnexte[1]),
                call(mdb, minserts_model, mnexte[2]),
                call(mdb, minserts_model, mnexte[3]),
                call(mdb, minserts_model, mnexte[4])
            ]
        )
        self.assertFalse(minserts_model.get_by_id.called)
        self.assertListEqual(
            minserts_model.set_status.call_args_list,
            [
                call(52, "Bad Type"),
                call(63, "Blocked"),
                call(222, "Exception")
            ]
        )
