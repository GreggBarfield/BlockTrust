from ..no_value import NoValue
from ...sectors import sectors_by_id

from .accounts import Accounts

NO_VALUE = NoValue()

notification_type_by_name = {
    "Global": 1,
    "Sector": 2,
    "Partner": 3
}
notification_type_by_id = {
    value: key
    for key, value in notification_type_by_name.items()
}


class Notifications:

    def __init__(self, db):
        self._db = db
        self._match_cols = ("id", "subject", "message", "is_archived", "notification_type", "created_timestamp",
                            "last_updated_timestamp")

    def get_notification_by_id(self, notification_id):
        """
        Gets the notification by ID

        Params:
            id: ID of the notification

        Returns:
            A notification id found or None
        """
        notification_rows = self._db.execute_d(
            """
                SELECT * FROM notifications
                WHERE id=%(id)s
            """,
            {
                "id": notification_id
            }
        )
        if len(notification_rows) != 1:
            return None
        return notification_rows[0]

    def insert_notification(self, subject, message, notification_type):
        """
        Inserts a new notification

        Params:
            subject: The subject for the message
            message: Message text
            notification_type: Notification type
        """
        self._db.execute(
            """
            INSERT INTO notifications (subject, message, is_archived, notification_type)
            VALUES (%(subject)s, %(message)s, %(is_archived)s, %(notification_type)s)
            """,
            {
                "subject": subject,
                "message": message,
                "is_archived": 0,
                "notification_type": notification_type
            }
        )
        notification = self.get_notification_by_id(self._db.last_row_id())
        return notification

    def get_notifications(self, subject=NO_VALUE, message=NO_VALUE, is_archived=NO_VALUE,
                          notfication_type=NO_VALUE):
        """
        Gets the notifications based on the provided parameters

        Params:
            subject: The subject for the message
            message: Message text
            is_archived: Message archive status. (0-Not archived, 1-Archived)
            notification_type: Type of notification based on notification_type_by_name dictionary

        Returns:
            A list of notifications or an empty array
        """
        base_query = "SELECT * FROM notifications"

        query_conditions = []
        query_values = {}

        if subject is not NO_VALUE:
            query_conditions.append(" subject = %(subject)s")
            query_values["subject"] = subject
        if message is not NO_VALUE:
            query_conditions.append(" message = %(message)s")
            query_values["message"] = message
        if is_archived is not NO_VALUE:
            query_conditions.append(" is_archived = %(is_archived)s")
            query_values["is_archived"] = is_archived
        if notfication_type is not NO_VALUE:
            query_conditions.append(" notfication_type = %(notfication_type)s")
            query_values["notfication_type"] = notfication_type
        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        notification_rows = self._db.execute_d(query, query_values)
        if len(notification_rows) > 0:
            return notification_rows
        else:
            return []

    def update_notification(self, id, subject=NO_VALUE, message=NO_VALUE, is_archived=NO_VALUE):
        """
        Updates the message based on the id specified

        Params:
            id: The ID of the system message to be updated
            subject: The subject for the message
            message: Message text
            is_archived: Message archive status. (0-Not archived, 1-Archived)

        """
        base_query = "UPDATE notifications "

        query_updated_columns = []
        query_updated_values = {}
        query_updated_values["id"] = id
        if subject is not NO_VALUE:
            query_updated_columns.append(" subject = %(subject)s")
            query_updated_values["subject"] = subject
        if message is not NO_VALUE:
            query_updated_columns.append(" message = %(message)s")
            query_updated_values["message"] = message
        if is_archived is not NO_VALUE:
            query_updated_columns.append(" is_archived = %(is_archived)s")
            query_updated_values["is_archived"] = is_archived
        if len(query_updated_columns) >= 1:
            combined_query_updated_values = " SET " + ",".join(query_updated_columns) + " WHERE id=%(id)s"
            query = base_query + combined_query_updated_values
            self._db.execute(query, query_updated_values)

    def get_notification_and_notification_recipients(self, notification_id=NO_VALUE,subject=NO_VALUE, message=NO_VALUE, is_archived=NO_VALUE,
                        notfication_type=NO_VALUE, notification_recipient_id=NO_VALUE, user_id=NO_VALUE,
                        is_notification_seen=NO_VALUE, notifications_order_by=NO_VALUE, notifications_sort_by=NO_VALUE):
        """
        Gets the notification and notification_recipient rows based on attributes provided

        Params:
            subject: The subject for the message
            message: Message text
            is_archived: Message archive status. (0-Not archived, 1-Archived)
            notification_type: Type of notification based on notification_type_by_name dictionary
            notification_recipient_id: ID in the notification_recipients table
            user_id: User ID in notification_recipients table
            is_notification_seen: Notification seen status (0-Not Seen, 1-Seen)

        Returns:
            A list of notifications or an empty list
        """
        # Need to add nr_id and n_id as "id" columns get over written
        base_query = "SELECT *, nr.id as nr_id, n.id as n_id FROM notification_recipients nr INNER JOIN notifications n ON nr.notification_id=n.id"
        query_conditions = []
        query_values = {}
        order_by_clause = ""

        if notification_id is not NO_VALUE:
            query_conditions.append("n.id = %(notification_id)s")
            query_values["notification_id"] = notification_id
        if subject is not NO_VALUE:
            query_conditions.append("n.subject = %(subject)s")
            query_values["subject"] = subject
        if message is not NO_VALUE:
            query_conditions.append("n.message = %(message)s")
            query_values["message"] = message
        if is_archived is not NO_VALUE:
            query_conditions.append("n.is_archived = %(is_archived)s")
            query_values["is_archived"] = is_archived
        if notfication_type is not NO_VALUE:
            query_conditions.append("n.notfication_type = %(notfication_type)s")
            query_values["notfication_type"] = notfication_type

        if notification_recipient_id is not NO_VALUE:
            query_conditions.append("nr.id = %(notification_recipient_id)s")
            query_values["notification_recipient_id"] = notification_recipient_id
        if user_id is not NO_VALUE:
            query_conditions.append("nr.user_id = %(user_id)s")
            query_values["user_id"] = user_id
        if is_notification_seen is not NO_VALUE:
            query_conditions.append("nr.is_notification_seen = %(is_notification_seen)s")
            query_values["is_notification_seen"] = is_notification_seen

        if notifications_order_by is not NO_VALUE:
            if notifications_order_by not in self._match_cols:
                raise Exception("notifications_order_by column doesn't exist")
            order_by_clause = "ORDER BY n." + notifications_order_by
            if notifications_sort_by is not NO_VALUE:
                if notifications_sort_by not in ("ASC", "DESC"):
                    raise Exception("Incorrect value for notifications_sort_by")
                order_by_clause += " " + notifications_sort_by

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions) + " " + order_by_clause
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition
        result_rows = self._db.execute_d(query, query_values)
        if len(result_rows) > 0:
            return result_rows
        else:
            return []