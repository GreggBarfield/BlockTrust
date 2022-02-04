from ..no_value import NoValue
from ..objects.notification import Notification
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
        return Notification(self._db, notification_rows[0])

    def get_notifications_for_user(self, user_id):
        """
        Gets the unarchived system messages for a user in descending order of timestamp

        Params:
            user_id: User ID of user for which messages need to be retrieved

        Returns:
            A list of messages
        """
        notifications = self._db.execute_d(
            """
            SELECT * FROM notification_recipients INNER JOIN notifications
            ON notifications.id = notification_recipients.notification_id
            AND user_id = %(user_id)s AND is_archived= %(is_archived)s
            ORDER BY notifications.created_timestamp DESC
            """,
            {
                "user_id": user_id,
                "is_archived": 0
            }
        )
        return notifications

    def get_unread_notifications_for_user(self, user_id):
        """
        Gets the unarchived system messages for a user in descending order of timestamp

        Params:
            user_id: User ID of user for which messages need to be retrieved

        Returns:
            A list of messages
        """
        notifications = self._db.execute_d(
            """
            SELECT * FROM notification_recipients INNER JOIN notifications
            ON notifications.id = notification_recipients.notification_id
            AND user_id = %(user_id)s AND is_archived= %(is_archived)s AND is_notification_seen = %(is_notification_seen)s
            ORDER BY notifications.created_timestamp DESC
            """,
            {
                "user_id": user_id,
                "is_archived": 0,
                "is_notification_seen": 0
            }
        )
        return notifications

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
