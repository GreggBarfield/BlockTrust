import json
import os

# config.py loads environment_config.json
# create environment_config.json from tools/config/environment_config_template.json
# config.py should throw errors if environment_config.json is misconfigured
# store config in config.py if it is shared, else store in environment_config.json

config_file_name = "environment_config.json"
config_file_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    config_file_name
)
config_file = json.load(open(config_file_path))

PROTOCOL = config_file["proxy"]["protocol"]
DOMAIN = config_file["proxy"]["domain"]
ROOT = PROTOCOL + "://" + DOMAIN
PORT = config_file["proxy"]["port"]

FLASK_SESSION_SECRET_KEY = config_file["flask"]["secret_key"]

MYSQL_CONFIG = config_file["mysql"]
API_MYSQL_CONFIG = (
    config_file["mysql"] if config_file["api_mysql"] == "same"
    else config_file["api_mysql"]
)
DEV_MYSQL_CONFIG = config_file["dev_mysql"]

AWS_S3_BUCKET = config_file["aws"]["s3"]["bucket"]
AWS_S3_REGION_NAME = config_file["aws"]["s3"]["region_name"]
AWS_ACCESS_KEY_ID = config_file["aws"]["access_key_id"]
AWS_SECRET_ACCESS_KEY = config_file["aws"]["secret_access_key"]

CSP = {
    'default-src': [
        'https://js.stripe.com',
        'https://polyfill.io',
        'https://i.imgur.com',
        'https://player.vimeo.com/',
        'https://www.youtube.com/',
        'https://www.google.com/',
        'https://www.gstatic.com/',
        'https://www.googletagmanager.com/',
        'https://www.google-analytics.com/',
        'https://unpkg.com/@flatfile/adapter/build/dist/index.min.js',
        'https://portal-2.flatfile.io/',
        'https://ipinfo.io/',
        'https://maps.googleapis.com',
        'https://maps.gstatic.com',
        'https://unpkg.com/@googlemaps/markerclusterer/dist/index.min.js',
        ROOT,
        '\'unsafe-inline\'',
        'fonts.gstatic.com',
        'fonts.googleapis.com',
        'http://localhost:5000',
        'blocktrustnetwork.com',
        'data:',
        "https://cdnjs.cloudflare.com"
    ],
    'frame-ancestors': [
        'blocktrustnetwork.com',
        'uscattletrace.org',
        'www.uscattletrace.org',
        'www-uscattletrace-org.filesusr.com'
    ]
}

if AWS_S3_BUCKET:
    CSP['default-src'].append(AWS_S3_BUCKET + ".s3.amazonaws.com")

EMAIL_SENDER = config_file["email"]["sender"]
SECONDARY_EMAIL_RECIPIENT_FOR_MATCH_FOUND = config_file["email"]["secondary_recipient_for_match_found"]

INTERNAL_API_SECRET = config_file["internal_api"]["secret"]

SUPPORT_GENERAL_EMAIL = config_file["support"]["general_email"]

SUPPORT_TAG_STORE_EMAIL = config_file["support"]["general_tag_store_email"]

ADMIN_EMAIL = config_file["email"]["admin_email"]

SUBSCRIPTION_WEBHOOK_SECRET = config_file["stripe"]["subscription_webhook_secret"]
ACCOUNT_WEBHOOK_SECRET = config_file["stripe"]["account_webhook_secret"]

EMAIL_TOKEN_SALT = config_file["internal_api"]["email_token_salt"]

EMAIL_SECRET_KEY = config_file["internal_api"]["secret_email_key"]
STRIPE_SECRET_KEY = config_file["stripe"]["secret_key"]
STRIPE_PUBLISHABLE_KEY = config_file["stripe"]["publishable_key"]
STRIPE_BASIC_PRICE = config_file["stripe"]["basic"]

USDA_API_KEY = config_file["usda"]["api_key"]
USDA_PUBLIC_ENDPOINT = config_file["usda"]["public_endpoint"]
USDA_MANDATORY_ENDPOINT = config_file["usda"]["mandatory_endpoint"]
USDA_GET_DATA = config_file["usda"]["get_data"]
USDA_CUTOFF_PERIOD_IN_DAYS = config_file["usda"]["report_cutoff_period_in_days"]

FLATFILE_LICENSE = config_file["flatfile_license"]

BLOCKCHAIN_ENDPOINT = config_file["blockchain"]["endpoint"]
BLOCKCHAIN_UPLOADS = config_file["blockchain"]["upload"]
BLOCKCHAIN_BATCH_SIZE = config_file["blockchain"]["batch_size"]

RECAPTCHA_SITE_KEY = config_file["recaptcha"]["site_key"]
RECAPTCHA_SECRET_KEY = config_file["recaptcha"]["secret_key"]
RECAPTCHA_MIN_SCORE = config_file["recaptcha"]["min_score"]

IPINFO_TOKEN = config_file["ipinfo"]["token"]
CHECK_IP = config_file["ipinfo"]["check_ip"]

RUN_NOTIFY_IF_NO_DATA_RECEIVED_FROM_PARTNER = config_file["run_jobs"]["notify_admin_if_no_data_received_from_partner"]

HERDWHISTLE_API_KEY = config_file["herdwhistle"]["api_key"]
HERDWHISTLE_API_ENDPOINT = config_file["herdwhistle"]["api_endpoint"]
HERDWHISTLE_DB = config_file["herdwhistle"]["db"]
HERDWHISTLE_USERNAME = config_file["herdwhistle"]["username"]
HERDWHISTLE_INVOICE_ID = config_file["herdwhistle"]["invoice_id"]
HERDWHISTLE_FETCH_EIDS_FROM_API = config_file["herdwhistle"]["fetch_eids_from_api"]