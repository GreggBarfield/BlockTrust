import boto3
from ...config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_REGION_NAME

def _get_new_session():
    """Gets a new session.

    Returns:
        boto3.Session
    """
    return boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

def get_s3_client():
    """Gets a boto3 s3 client on a new session.

    Returns:
        boto3.Client
    """
    return _get_new_session().client(
        's3',
        region_name=AWS_S3_REGION_NAME,
    )

def get_ses_client():
    """Gets a boto3 SES client on a new session.

    Returns:
        boto3.Client
    """
    return _get_new_session().client(
        'ses',
        region_name=AWS_S3_REGION_NAME,
    )

