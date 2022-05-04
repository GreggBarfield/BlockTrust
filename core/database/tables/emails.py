import json
from ..no_value import NoValue
from .users import Users
from ...utilities.email import send_email
from ...renderers.email import render_email


NO_VALUE = NoValue()
email_cols = ("id", "user_id", "subject", "body", "variables", "template_name", "email_type", "is_processed")
email_processing_status_by_name = {
    "Not Processed": 0,
    "Processed": 1,
    "Failed": 2
}
email_processing_status_by_id = {
    value: key
    for key, value in email_processing_status_by_name.items()
}
email_type_by_name = {
    "Match Found": 1
}
email_type_by_id = {
    value: key
    for key, value in email_type_by_name.items()
}


class Emails:

    def __init__(self, db):
        self._db = db

    def get_emails(self, id=NO_VALUE, user_id=NO_VALUE, subject=NO_VALUE, body=NO_VALUE, template_name=NO_VALUE,
                   email_type=NO_VALUE, is_processed=NO_VALUE, emails_order_by=NO_VALUE, emails_sort_by=NO_VALUE):
        """
        Gets the emails based on attributes provided

        Params:
            id: ID of the email row
            user_id: User ID of the recipient user for the email
            subject: Email subject line
            body: Body of the email
            template_name: Email template name
            email_type: Type of email being sent out
            is_processed: Indicates whether is email is sent or not(0-Not sent, 1-Sent)

        Returns:
            A list of email rows or an empty list
        """
        base_query = "SELECT * FROM emails"

        query_conditions = []
        query_values = {}
        order_by_clause = ""

        if id is not NO_VALUE:
            query_conditions.append(" id = %(id)s")
            query_values["id"] = id
        if user_id is not NO_VALUE:
            query_conditions.append(" user_id = %(user_id)s")
            query_values["user_id"] = user_id
        if subject is not NO_VALUE:
            query_conditions.append(" subject = %(subject)s")
            query_values["subject"] = subject
        if body is not NO_VALUE:
            query_conditions.append(" body = %(body)s")
            query_values["body"] = body
        if template_name is not NO_VALUE:
            query_conditions.append(" template_name = %(template_name)s")
            query_values["template_name"] = template_name
        if email_type is not NO_VALUE:
            query_conditions.append(" email_type = %(email_type)s")
            query_values["email_type"] = email_type
        if is_processed is not NO_VALUE:
            query_conditions.append(" is_processed = %(is_processed)s")
            query_values["is_processed"] = is_processed

        if emails_order_by is not NO_VALUE:
            if emails_order_by not in email_cols:
                raise Exception("emails_order_by column doesn't exist")
            order_by_clause = "ORDER BY " + emails_order_by
            if emails_sort_by is not NO_VALUE:
                if emails_sort_by not in ("ASC", "DESC"):
                    raise Exception("Incorrect value for emails_sort_by")
                order_by_clause += " " + emails_sort_by

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

    def insert_email(self, user_id=NO_VALUE, subject=NO_VALUE, body=NO_VALUE, variables=NO_VALUE,
                     template_name=NO_VALUE, email_type=NO_VALUE, is_processed=NO_VALUE):
        """
        Inserts a new email to be sent out

        Params:
            user_id: User ID of the recipient user for the email
            subject: Email subject line
            body: Body of the email
            variables: Variables required for the email template
            template_name: Email template name
            email_type: Type of email being sent out
            is_processed: Indicates whether is email is sent or not(0-Not sent, 1-Sent)
        """
        if email_type == email_type_by_name["Match Found"]:
            unprocessed_match_emails_in_past_day = self.check_for_scheduled_emails_in_past_day(
                user_id=user_id,
                number_of_days=1,
                email_type=email_type_by_name["Match Found"],
                is_processed=email_processing_status_by_name["Not Processed"]
            )
            if unprocessed_match_emails_in_past_day is not None:
                return
        self._db.execute(
            """
            INSERT INTO emails (user_id, subject, body, variables, template_name, email_type, is_processed)
            VALUES (%(user_id)s, %(subject)s, %(body)s, %(variables)s, %(template_name)s, %(email_type)s, %(is_processed)s)
            """,
            {
                "user_id": user_id,
                "subject": subject,
                "body": body,
                "variables": json.dumps(variables),
                "template_name": template_name,
                "email_type": email_type,
                "is_processed": is_processed
            }
        )

    def update_emails(self, id, user_id=NO_VALUE, subject=NO_VALUE, body=NO_VALUE, template_name=NO_VALUE,
                      email_type=NO_VALUE, variables=NO_VALUE, is_processed=NO_VALUE):
        """
        Updates an email row

        Params:
            id: ID of the email row
            user_id: User ID of the recipient user for the email
            subject: Email subject line
            body: Body of the email
            template_name: Email template name
            email_type: Type of email being sent out
            is_processed: Indicates whether is email is sent or not(0-Not sent, 1-Sent)
        """
        base_query = "UPDATE emails "

        query_conditions = []
        query_values = {}
        query_values["id"] = id
        if user_id is not NO_VALUE:
            query_conditions.append(" user_id = %(user_id)s")
            query_values["user_id"] = user_id
        if subject is not NO_VALUE:
            query_conditions.append(" subject = %(subject)s")
            query_values["subject"] = subject
        if body is not NO_VALUE:
            query_conditions.append(" body = %(body)s")
            query_values["body"] = body
        if template_name is not NO_VALUE:
            query_conditions.append(" template_name = %(template_name)s")
            query_values["template_name"] = template_name
        if email_type is not NO_VALUE:
            query_conditions.append(" email_type = %(email_type)s")
            query_values["email_type"] = email_type
        if variables is not NO_VALUE:
            query_conditions.append(" variables = %(variables)s")
            query_values["variables"] = json.dumps(variables)
        if is_processed is not NO_VALUE:
            query_conditions.append(" is_processed = %(is_processed)s")
            query_values["is_processed"] = is_processed

        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("Must give values for fields to update on Emails")

    def check_for_scheduled_emails_in_past_day(self, user_id=NO_VALUE, number_of_days=NO_VALUE, email_type=NO_VALUE, is_processed=NO_VALUE):
        """
        Checks if the user has emails scheduled in the past 24 hours

        Params:
            user_id: User ID of the email recipient

        Returns:
            Email dictionary if recent scheduled email is found. None if no recent scheduled emails present.
        """
        email_row = self._db.execute_d(
            """
            SELECT * FROM emails
            WHERE user_id = %(user_id)s AND is_processed = %(is_processed)s
            AND DAY(created_timestamp) > DAY(current_date())-%(number_of_days)s AND email_type = %(email_type)s
            """, {
                "user_id": user_id,
                "is_processed": is_processed,
                "number_of_days": number_of_days,
                "email_type": email_type
            })
        if len(email_row) > 0:
            return email_row[0]
        return None

    def process_pending_emails(self):
        """
        Checks for unsent emails in the table and sends out an email marking it as porcessed 
        """
        unprocessed_emails = self.get_emails(is_processed=email_processing_status_by_name["Not Processed"])
        for unprocessed_email in unprocessed_emails:
            try:
                user_rows = Users(self._db).get_users(id=unprocessed_email["user_id"])
                if len(user_rows) == 1:
                    user_row = user_rows[0]
                    if user_row["is_email_verified"] == 1:
                        email_variables = json.loads(unprocessed_email["variables"])
                        email_variables["body"] = unprocessed_email["body"]
                        send_email(
                            unprocessed_email["subject"],
                            # render_email(unprocessed_email["template_name"], email_variables),
                            "test body",
                            # user_row["email"]
                            "nisheet.thakur@blocktrustnetwork.com"
                            )
                        self.update_emails(id=unprocessed_email["id"], is_processed=email_processing_status_by_name["Processed"])
            except Exception as e:
                self.update_emails(id=unprocessed_email["id"], is_processed=email_processing_status_by_name["Failed"])
