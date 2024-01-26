class SentEmails:

    def __init__(self, db):
        self._db = db

    def insert(self, account_id, subject, user_id, email_address, file=None, routine=None, template_name=None, variables=None):
        """
        Inserts a new scheduled email to be sent out

        Params:
            account_id: Account ID of the recipient
            user_id: User ID of the recipient 
            subject: Email subject line
        """
        self._db.execute(
            """
            INSERT INTO sent_emails (account_id, user_id, email_address, subject, file, routine, template_name, variables)
            VALUES (%(account_id)s, %(user_id)s, %(email_address)s, %(subject)s, %(file)s, %(routine)s, %(template_name)s, %(variables)s)
            """,
            {
                "account_id": account_id,
                "user_id": user_id,
                "email_address": email_address,
                "account_id": account_id,
                "subject": subject,
                "file": file,
                "routine": routine,
                "template_name": template_name,
                "variables": variables
            }
        )
