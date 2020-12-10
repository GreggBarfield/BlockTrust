from urllib.parse import urljoin

# Stripe config

ENDPOINT_SECRET = "whsec_zqBq9a4XgpGnW9fQAjLJLB4j4ntiHQye"

STRIPE_API_KEY = 'sk_test_51HRTwoGWRtomrLg3A2oqpP5mS60M5OAJyjpoUNGm4YjgGmhAWMFBaKx9ezdtk5DGfExhpSrPgd0ESgcbc9hOCpiR0023awyPeX'

# Server config

DOMAIN = 'https://ledgerspacedev.com'

PORT = 443

FLASK_SESSION_SECRET_KEY = "sg3v40n78gvsny3780gsv45n0h87gsv34nh807"

SERVER_COMMUNICATION_API_SECRET = "banana"


# Image config

IMAGE_PATH = "static/images"
IMAGE_JPEG_QUALITY = 70
IMAGE_MAX_PIXEL_COUNT = 1280 * 720
IMAGE_SEARCH_SUGGESTED_DIR = urljoin(DOMAIN, "static/images/")

# SQL config

MYSQL_CONFIG = {
    "host": "mysql",
    "user": "dev",
    "passwd": "ag489jag4p98hj",
    "database": "example_db_1",
    "autocommit": True
}

# Admin password

ADMIN_PASSWORD = "admin4"

AWS_S3_BUCKET = "btndev"

CSP = {
    'default-src': [
        'https://js.stripe.com',
        'https://polyfill.io',
        'https://i.imgur.com',
        DOMAIN,
        '\'unsafe-inline\'',
        'fonts.gstatic.com',
        'fonts.googleapis.com',
        'http://localhost:5000',
        AWS_S3_BUCKET + ".s3.amazonaws.com"
    ]
}