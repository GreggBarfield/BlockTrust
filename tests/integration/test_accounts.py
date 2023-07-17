from core.database.tables.accounts import Accounts, HEALTH_TRACK_PARTNER_COMPANY, RED_ANGUS_PARTNER_COMPANY, account_cols


def test_healthtrack_constant(db_connection):
    health_track_account = Accounts(db_connection).get_accounts(company=HEALTH_TRACK_PARTNER_COMPANY)
    assert len(health_track_account) == 1
    assert health_track_account[0]["company"] == HEALTH_TRACK_PARTNER_COMPANY
    assert health_track_account[0]["is_partner"] == 1


def test_red_angus_constant(db_connection):
    red_angus_account = Accounts(db_connection).get_accounts(company=RED_ANGUS_PARTNER_COMPANY)
    assert len(red_angus_account) == 1
    assert red_angus_account[0]["company"] == RED_ANGUS_PARTNER_COMPANY
    assert red_angus_account[0]["is_partner"] == 1


def test_columns(db_connection):
    # getting any account
    health_track_account = Accounts(db_connection).get_accounts(company=HEALTH_TRACK_PARTNER_COMPANY)[0]
    for col in account_cols:
        assert col in health_track_account
        assert len(account_cols) == len(health_track_account)
