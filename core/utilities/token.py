import itsdangerous
from itsdangerous import URLSafeTimedSerializer
from ..config import EMAIL_TOKEN_SALT, EMAIL_SECRET_KEY
from ..common_exceptions import ExportException

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


def confirmToken(token, expiration=86400):
    try:
        serializer = URLSafeTimedSerializer(EMAIL_SECRET_KEY)
        email = serializer.loads(
                token,
                salt=EMAIL_TOKEN_SALT,
                max_age=expiration
            )
    except ExportException as e:
        return False

    return email
