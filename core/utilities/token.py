from flask import (
    url_for
)
from itsdangerous import BadData, URLSafeTimedSerializer
from ..config import EMAIL_TOKEN_SALT, EMAIL_SECRET_KEY, ROOT
from ..utilities.constants import SECONDS_IN_ONE_DAY

"""
EMAIL_TOKEN_SALT and EMAIL_SECRET_KEY can be changed in core/environment_config.json
Generating Confirmation token using itsdangerous package
"""


def generateConfirmationToken(email):
    serializer = URLSafeTimedSerializer(EMAIL_SECRET_KEY)
    return serializer.dumps(email, salt=EMAIL_TOKEN_SALT)


"""
Confirming if the token is valid and setting an expiration of 1 hour
"""


def confirmToken(token, expiration=SECONDS_IN_ONE_DAY):
    try:
        serializer = URLSafeTimedSerializer(EMAIL_SECRET_KEY)
        if expiration:
            data = serializer.loads(token, salt=EMAIL_TOKEN_SALT, max_age=expiration)
        else:
            data = serializer.loads(token, salt=EMAIL_TOKEN_SALT)
        return data
    except BadData as e:
        raise Exception("The Invite link is invalid or expired")


def create_user_invitation_link(email, account_id, is_admin):
    userToken = generateConfirmationToken(str(
        {"user_email": email, "account_id": account_id, "is_admin": is_admin}
    ))
    invite_url = ROOT + url_for('outside_bp.serve_add_user', invite_token=userToken)
    return invite_url
