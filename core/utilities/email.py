from .aws.aws import get_ses_client
from ..config import EMAIL_SENDER
from ..utilities import auth


def send_email(subject, html, to_address, override=False):
    """Sends an email.
    Params:
        subject: Subject for the email which needs to be sent
        html: The file which needs to be displayed as a part of the email body
        to_address: The email address to which the email is being sent
        override: Set override=True if email is to be sent to an unverified user
    Raises:
        botocore.exceptions.ClientError on failure
    """

    if override or auth.get_email_verified_value(email=to_address) is True:
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

    
def send_email_to_many(subject, html, to_addresses):
    """Sends an email.
    Params:
        subject: Subject for the email which needs to be sent
        html: The file which needs to be displayed as a part of the email body
        to_address: The list of email addresses to which the email is being sent
    Raises:
        botocore.exceptions.ClientError on failure
    """
    get_ses_client().send_email(
        Destination={
            'BccAddresses': to_addresses,
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