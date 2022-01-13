from tkinter.messagebox import NO
from .. import database
from ..no_value import NoValue
from .accounts import Accounts
from .users import Users
from .account_users import AccountUsers
from ...sectors import sectors_by_id


NO_VALUE = NoValue()


class NotificationRecipients:

    def __init__(self, db: 'database.Database'):
        self._db = db

    def insert_notification_recipients(self, notification_id, users=[]):
        """
        Inserts a new notification recipient

        Params:
            notifcation_id: ID of the otification in the notifications table
            users: A list of user ID which need to receive the notification
        """
        for user in users:
            self._db.execute(
                """
                INSERT INTO notification_recipients
                VALUES
                (%(notification_id)s, %(user_id)s)
                """,
                {
                    "notification_id": notification_id,
                    "user_id": user
                }
            )

    def insert_global_notification_recipients(self, notification_id):
        """
        Inserts global notification recipients

        Params:
             notification_id: ID of the notification in the notifications table     
        """
        all_users = Users(self._db).get_users()
        users = []
        for user in all_users:
            users.append(user["id"])
        self.insert_notification_recipients(notification_id=notification_id, users=users)

    def insert_sector_notification_recipients(self, sector, notification_id):
        """
        Inserts notification recipients for a sector

        Params:
            sector: Sector for which notification is intended
            notification_id: ID of the notification in the notifications table
        """
        account_rows = Accounts(self._db).get_accounts(sector=sector)
        users = []
        for account_row in account_rows:
            account_users = AccountUsers(self._db).get_account_users(account=account_row.id())
            for account_user in account_users:
                users.append(account_user["user"])
        self.insert_notification_recipients(notification_id=notification_id, users=users)

    def insert_partner_notification_recipients(self, partner_id, notification_id):
        """
        Inserts notification recipients for users related to a partner account

        Params:
            partner_id: ID of partner account
            notifcation_id: ID of the notification in the notifications table
        """
        account_rows = Accounts(self._db).get_accounts(partner_account=partner_id)
        users = []
        for account_row in account_rows:
            account_users = AccountUsers(self._db).get_account_users(account=account_row.id())
            for account_user in account_users:
                users.append(account_user["user"])
        self.insert_notification_recipients(notification_id=notification_id, users=users)

    def get_notification_recipients(self, id=NO_VALUE, notification_id=NO_VALUE, user_id=NO_VALUE, notification_seen=NO_VALUE):
        """
        Gets the notification_recipients rows based on the attributes provided

        Params:
            notifcation_id: ID of the notification in the notifications table
            user_id: User ID of the recipient
            notification_seen: Whether the notification was viewed or not
        Returns:
            A list of notification recipients or an empty array
        """
        base_query = "SELECT * FROM notification_recipients "

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append(" id = %(id)s")
            query_values["id"] = id
        if notification_id is not NO_VALUE:
            query_conditions.append(" notification_id = %(notification_id)s")
            query_values["notification_id"] = notification_id
        if user_id is not NO_VALUE:
            query_conditions.append(" user_id = %(user_id)s")
            query_values["user_id"] = user_id
        if notification_seen is not NO_VALUE:
            query_conditions.append(" notification_seen = %(notification_seen)s")
            query_values["notification_seen"] = notification_seen
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

    def update_notification_recipients(self, id, notification_id=NO_VALUE, user_id=NO_VALUE, notification_seen=NO_VALUE):
        """
        Updates the specified notification recipient row based on ID 

        Params:
            id: Notification recipient ID which needs to be updated
            notifcation_id: ID of the notification in the notifications table
            user_id: User ID of the recipient
            notification_seen: Whether the notification was viewed or not
        """
        base_query = "UPDATE notification_recipients "

        query_updated_columns = []
        query_updated_values = {}
        query_updated_values["id"] = id
        if notification_id is not NO_VALUE:
            query_updated_columns.append(" notification_id = %(notification_id)s")
            query_updated_values["notification_id"] = notification_id
        if user_id is not NO_VALUE:
            query_updated_columns.append(" user_id = %(user_id)s")
            query_updated_values["user_id"] = user_id
        if notification_id is not NO_VALUE:
            query_updated_columns.append(" notification_seen = %(notification_seen)s")
            query_updated_values["notification_seen"] = notification_seen
        if len(query_updated_columns) >= 1:
            combined_query_updated_values = " SET " + ",".join(query_updated_columns) + "WHERE id=%(id)s"
            query = base_query + combined_query_updated_values
            self._db.execute(query, query_updated_values)
