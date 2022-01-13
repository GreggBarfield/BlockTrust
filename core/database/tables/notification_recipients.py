from .. import database
from ..no_value import NoValue
from .accounts import Accounts
from .account_users import AccountUsers
from ...sectors import sectors_by_id


NO_VALUE = NoValue()


class NotificationRecipients:

    def __init__(self, db: 'database.Database'):
        self._db = db

    def insert_notification_recipient(self, notification_id, user_id):
        """
        Inserts a new notification recipient

        Params:
            notifcation_id: ID of the otification in the notifications table
            user_id: User ID of the recipient
        """
        self._db.execute(
            """
            INSERT INTO notification_recipients
            VALUES
            (%(notification_id)s, %(user_id)s)
            """,
            {
                "notification_id": notification_id,
                "user_id": user_id
            }
        )

    def insert_sector_notification_recipients(self, sector, notification_id):
        """
        Inserts notification_recipients for a sector

        Params:
            sector: Sector for which notification is intended
            notification_id: ID of the notification in the notifications table
        """
        account_rows = Accounts(self._db).get_accounts(sector=sector)
        for account_row in account_rows:
            account_users = AccountUsers(self._db).get_account_users(account=account_row.id())
            for account_user in account_users:
                self.insert_notification_recipient(notification_id=notification_id, user_id=account_user["user"])

    def insert_partner_notification_recipients(self, partner_id, notification_id):
        """
        Inserts notification recipients for users related to a partner account

        Params:
            partner_id: ID of partner account
            notifcation_id: ID of the notification in the notifications table
        """
        account_rows = Accounts(self._db).get_accounts(partner_account=partner_id)
        for account_row in account_rows:
            account_users = AccountUsers(self._db).get_account_users(account=account_row.id())
            for account_user in account_users:
                self.insert_notification_recipient(notification_id=notification_id, user_id=account_user["user"])

    def get_notification_recipients(self, notification_id=NO_VALUE, user_id=NO_VALUE):
        """
        Gets the notification_recipients rows based on the attributes provided

        Params:
            notifcation_id: ID of the otification in the notifications table
            user_id: User ID of the recipient

        Returns:
            A list of notification recipients or an empty array
        """
        base_query = "SELECT * FROM notification_recipients "

        query_conditions = []
        query_values = {}

        if notification_id is not NO_VALUE:
            query_conditions.append(" notification_id = %(notification_id)s")
            query_values["notification_id"] = notification_id
        if user_id is not NO_VALUE:
            query_conditions.append(" user_id = %(user_id)s")
            query_values["user_id"] = user_id
        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        notification_recipient_rows = self._db.execute_d(query, query_values)
        if len(notification_recipient_rows) > 0:
            return notification_recipient_rows
        else:
            return []