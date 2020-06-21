from .dev import *
from dotenv import load_dotenv
load_dotenv()

import dj_database_url

try:
    from .local import *
except ImportError:
    pass

from decouple import config

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURITY WARNING: define the correct hosts in production!


DEBUG = False
SECRET_KEY = config('SECRET_KEY')

MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

ALLOWED_HOSTS = ['datamaelstrom.herokuapp.com','localhost', '127.0.0.1',]
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
BASE_URL = 'http://localhost:8000'
