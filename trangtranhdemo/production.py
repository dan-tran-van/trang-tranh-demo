import os

from .settings import *  # noqa
from .settings import BASE_DIR

# Configure the domain name using the environment variable
# that Azure automatically creates for us.
# ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []



if 'CUSTOM_HOSTNAME' in os.environ:
    ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME'],os.environ['CUSTOM_HOSTNAME']]
else:
    ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]

HOST_DOMAIN = "https://" + os.environ['WEBSITE_HOSTNAME'] if 'WEBSITE_HOSTNAME' in os.environ else ""

CUSTOM_DOMAIN = "https://" + os.environ['CUSTOM_HOSTNAME'] if 'CUSTOM_HOSTNAME' in os.environ else ""

STATIC_DOMAIN = "https://" + os.environ['STATIC_HOSTNAME'] if 'STATIC_HOSTNAME' in os.environ else ""

if 'CUSTOM_HOSTNAME' in os.environ:
    CSRF_TRUSTED_ORIGINS = [HOST_DOMAIN, CUSTOM_DOMAIN]
elif 'WEBSITE_HOSTNAME' in os.environ:
    CSRF_TRUSTED_ORIGINS = [HOST_DOMAIN]

if 'STATIC_HOSTNAME' in os.environ:
    CSRF_TRUSTED_ORIGINS.append(STATIC_DOMAIN)

# CSRF_TRUSTED_ORIGINS = ['http://' + os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
DEBUG = False
SECRET_KEY = os.getenv('SECRET_KEY')


# Configure Postgres database based on connection string of the libpq Keyword/Value form
# https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
conn_str = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': conn_str_params['dbname'],
        'HOST': conn_str_params['host'],
        'USER': conn_str_params['user'],
        'PASSWORD': conn_str_params['password'],
    }
}

# CACHES = {
#         "default": {  
#             "BACKEND": "django_redis.cache.RedisCache",
#             "LOCATION": os.environ.get('AZURE_REDIS_CONNECTIONSTRING'),
#             "OPTIONS": {
#                 "CLIENT_CLASS": "django_redis.client.DefaultClient",
#                 "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
#         },
#     }
# }

AZURE_ACCOUNT_NAME = os.getenv('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = os.getenv('AZURE_ACCOUNT_KEY')
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "account_name": AZURE_ACCOUNT_NAME,
            "account_key": AZURE_ACCOUNT_KEY,
            "azure_container": "media",
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "account_name": AZURE_ACCOUNT_NAME,
            "account_key": AZURE_ACCOUNT_KEY,
            "azure_container": "static",
        },
    },
}


STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'

# SECURE_SSL_REDIRECT = True

# SECURE_HSTS_SECONDS = 3600

# SECURE_HSTS_PRELOAD = True

# SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# EMAIL_USE_TLS = True 
# EMAIL_HOST = os.getenv('EMAIL_HOST')  
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  
# EMAIL_PORT = 587  
# DEFAULT_FROM_EMAIL = f"Đàn {EMAIL_HOST_USER}"