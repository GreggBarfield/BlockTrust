from .aws.aws import get_ses_client
from ..config import EMAIL_SENDER


def send_email(subject, html, to_address):
    """Sends an email.

    Raises:
        botocore.exceptions.ClientError on failure
    """
    get_ses_client().send_email(
        Destination={
            'ToAddresses': [
                to_address,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': "UTF-8",
                    'Data': html,
                },
                'Text': {
                    'Charset': "UTF-8",
                    'Data': "Please use an email client that supports HTML email to view this email.",
                },
            },
            'Subject': {
                'Charset': "UTF-8",
                'Data': subject,
            },
        },
        Source=EMAIL_SENDER
    )
