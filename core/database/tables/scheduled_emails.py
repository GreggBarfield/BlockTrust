import json
from ..no_value import NoValue
from .users import Users
from ...utilities.email import send_email
from datetime import datetime


NO_VALUE = NoValue()

SCHEDULED_EMAIL_COLUMNS = ("id", "user_id", "account_id" "subject", "body", "variables", "template_name", "status_id", "error_details", "sent_date_time")

SCHEDULED_EMAIL_STATUS_NAME_TO_ID = {
    "Not Sent": 0,
    "Sent": 1,
    "Error": 2
}

SCHEDULED_EMAIL_STATUS_ID_TO_NAME = {
    value: key
    for key, value in SCHEDULED_EMAIL_STATUS_NAME_TO_ID.items()
}

EMAILS = {
    "MATCH FOUND": {
        "SUBJECT": "Congratulations, match found!",
        "BODY": "Congratulations, one or more of your cattle has been matched in the beef supply chain. Go to your account to see details"
    }
}


class ScheduledEmails:

    def __init__(self, db):
        self._db = db

    def get_scheduled_emails(self, id=NO_VALUE, user_id=NO_VALUE, account_id=NO_VALUE, subject=NO_VALUE, body=NO_VALUE, 
                             template_name=NO_VALUE, status_id=NO_VALUE, error_details=NO_VALUE,
                             sent_date_time=NO_VALUE, scheduled_emails_order_by=NO_VALUE,
                             scheduled_emails_sort_by=NO_VALUE, sent_date=NO_VALUE):
        """
        Gets the scheduled emails based on attributes provided

        Params:
            id: ID of the email row
            user_id: User ID of the recipient user for the email
            subject: Email subject line
            body: Body of the email
            template_name: Email template name
            status_id: Indicates whether is email is sent or not(0-Not sent, 1-Sent)
            error_details: Error details if any (Default null)
            sent_date_time: Date/Time when email was sent

        Returns:
            A list of scheduled email rows or an empty list
        """
        base_query = "SELECT * FROM scheduled_emails"

        query_conditions = []
        query_values = {}
        order_by_clause = ""

        if id is not NO_VALUE:
            query_conditions.append(" id = %(id)s")
            query_values["id"] = id
        if user_id is not NO_VALUE:
            query_conditions.append(" user_id = %(user_id)s")
            query_values["user_id"] = user_id
        if account_id is not NO_VALUE:
            query_conditions.append(" account_id = %(account_id)s")
            query_values["account_id"] = account_id
        if subject is not NO_VALUE:
            query_conditions.append(" subject = %(subject)s")
            query_values["subject"] = subject
        if body is not NO_VALUE:
            query_conditions.append(" body = %(body)s")
            query_values["body"] = body
        if template_name is not NO_VALUE:
            query_conditions.append(" template_name = %(template_name)s")
            query_values["template_name"] = template_name
        if status_id is not NO_VALUE:
            query_conditions.append(" status_id = %(status_id)s")
            query_values["status_id"] = status_id
        if error_details is not NO_VALUE:
            query_conditions.append(" error_details = %(error_details)s")
            query_values["error_details"] = error_details
        if sent_date_time is not NO_VALUE:
            query_conditions.append(" sent_date_time = %(sent_date_time)s")
            query_values["sent_date_time"] = sent_date_time
        if sent_date is not NO_VALUE:
            query_conditions.append(" DATE(sent_date_time) = %(sent_date)s")
            query_values["sent_date"] = sent_date

        if scheduled_emails_order_by is not NO_VALUE:
            if scheduled_emails_order_by not in SCHEDULED_EMAIL_COLUMNS:
                raise Exception("scheduled_emails_order_by column doesn't exist")
            order_by_clause = "ORDER BY " + scheduled_emails_order_by
            if scheduled_emails_sort_by is not NO_VALUE:
                if scheduled_emails_sort_by not in ("ASC", "DESC"):
                    raise Exception("Incorrect value for scheduled_emails_sort_by")
                order_by_clause += " " + scheduled_emails_sort_by

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions) + " " + order_by_clause
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        email_rows = self._db.execute_d(query, query_values)
        if len(email_rows) > 0:
            return email_rows
        else:
            return []

    def insert_scheduled_email(self, user_id=None, account_id=None, subject=None, body=None, variables=None,
                               template_name=None, status_id=None):
        """
        Inserts a new scheduled email to be sent out

        Params:
            user_id: User ID of the recipient user for the email
            subject: Email subject line
            body: Body of the email
            variables: Variables required for the email template
            template_name: Email template name
            status_id: Indicates whether email is sent, not sent or error(0-Not sent, 1-Sent, 2-Error)
        """
        self._db.execute(
            """
            INSERT INTO scheduled_emails (user_id, account_id, subject, body, variables, template_name, status_id)
            VALUES (%(user_id)s, %(account_id)s, %(subject)s, %(body)s, %(variables)s, %(template_name)s, %(status_id)s)
            """,
            {
                "user_id": user_id,
                "account_id": account_id,
                "subject": subject,
                "body": body,
                "variables": json.dumps(variables) if variables is not None else None,
                "template_name": template_name,
                "status_id": status_id
            }
        )

    def update_scheduled_emails(self, id, user_id=NO_VALUE, account_id=NO_VALUE, subject=NO_VALUE, body=NO_VALUE, template_name=NO_VALUE,
                                variables=NO_VALUE, status_id=NO_VALUE, error_details=NO_VALUE, sent_date_time=NO_VALUE):
        """
        Updates a scheduled email row

        Params:
            id: ID of the email row
            user_id: User ID of the recipient user for the email
            subject: Email subject line
            body: Body of the email
            template_name: Email template name
            status_id: Indicates whether is email is sent or not(0-Not sent, 1-Sent)
            error_details: Error details if any (Default null)
            sent_date_time: Date/Time when email was sent
        """
        base_query = "UPDATE scheduled_emails "

        query_conditions = []
        query_values = {}
        query_values["id"] = id
        if user_id is not NO_VALUE:
            query_conditions.append(" user_id = %(user_id)s")
            query_values["user_id"] = user_id
        if account_id is not NO_VALUE:
            query_conditions.append(" account_id = %(account_id)s")
            query_values["account_id"] = account_id
        if subject is not NO_VALUE:
            query_conditions.append(" subject = %(subject)s")
            query_values["subject"] = subject
        if body is not NO_VALUE:
            query_conditions.append(" body = %(body)s")
            query_values["body"] = body
        if template_name is not NO_VALUE:
            query_conditions.append(" template_name = %(template_name)s")
            query_values["template_name"] = template_name
        if variables is not NO_VALUE:
            query_conditions.append(" variables = %(variables)s")
            query_values["variables"] = json.dumps(variables)
        if status_id is not NO_VALUE:
            query_conditions.append(" status_id = %(status_id)s")
            query_values["status_id"] = status_id
        if error_details is not NO_VALUE:
            query_conditions.append(" error_details = %(error_details)s")
            query_values["error_details"] = error_details
        if sent_date_time is not NO_VALUE:
            query_conditions.append(" sent_date_time = %(sent_date_time)s")
            query_values["sent_date_time"] = sent_date_time

        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("Must give values for fields to update on Scheduled Emails")

    def process_pending_emails(self):
        """
        Checks for unsent emails in the table and sends out an email marking it as sent 
        """
        unprocessed_emails = self.get_scheduled_emails(status_id=SCHEDULED_EMAIL_STATUS_NAME_TO_ID["Not Sent"])
        for unprocessed_email in unprocessed_emails:
            try:
                user_rows = Users(self._db).get_users(id=unprocessed_email["user_id"], is_email_verified=1)
                if len(user_rows) == 1:
                    user_row = user_rows[0]
                    send_email(
                        unprocessed_email["subject"],
                        unprocessed_email["body"],
                        user_row["email"]
                    )
                    self.update_scheduled_emails(id=unprocessed_email["id"], status_id=SCHEDULED_EMAIL_STATUS_NAME_TO_ID["Sent"], sent_date_time=datetime.now())
                else:
                    raise Exception("User not found or has an unverified email")
            except Exception as e:
                self.update_scheduled_emails(id=unprocessed_email["id"], status_id=SCHEDULED_EMAIL_STATUS_NAME_TO_ID["Error"], error_details=str(e))
