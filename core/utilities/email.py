from .aws.aws import get_ses_client
from ..config import EMAIL_SENDER
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


def send_raw_email(subject, recipients, body, attachment, filename):
    for recipient in recipients:
        mime_msg = _format_mime_message(
            subject, recipient, body, attachment, filename
        )
        get_ses_client().send_raw_email(
            Source=EMAIL_SENDER,
            Destinations=[recipient],
            RawMessage={"Data": mime_msg.as_string()},
        )


def _format_mime_message(subject, recipient, html, attachment, filename, charset="utf-8"):
    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = recipient
    msg_body = MIMEMultipart("alternative")

    htmlpart = MIMEText(html.encode(charset), "html", charset)

    msg_body.attach(htmlpart)

    att = MIMEApplication(attachment.encode(charset))
    att.add_header("Content-Disposition", "attachment", filename=filename)
    msg.attach(msg_body)
    msg.attach(att)
    return msg


def send_email(subject, html, to_address):
    """Sends an email.
    Params:
        subject: Subject for the email which needs to be sent
        html: The file which needs to be displayed as a part of the email body
        to_address: The email address to which the email is being sent
    Raises:
        botocore.exceptions.ClientError on failure
    """
    # Please check if the user is verified if the mail needs to be sent out to verified users only
    return get_ses_client().send_email(
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


def send_tag_store_email(subject, html, to_address, source):
    """Sends an email.
    Params:
        subject: Subject for the email which needs to be sent
        html: The file which needs to be displayed as a part of the email body
        to_address: The email address to which the email is being sent
        override: Set override=True if email is to be sent to an unverified user
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
        Source=source
    )


def send_multiple_tag_store_email(subject, html, to_addresses, source):
    """Sends an email.
    Params:
        subject: Subject for the email which needs to be sent
        html: The file which needs to be displayed as a part of the email body
        to_addresses: The email addresses to which the email is being sent
        override: Set override=True if email is to be sent to an unverified user
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
        Source=source
    )
