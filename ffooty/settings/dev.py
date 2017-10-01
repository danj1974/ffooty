from __future__ import absolute_import

import os

from .base import *
# import psycopg2.extensions

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'umu8tj3a&k_6zv69-(8w!xj32a64m$kaiu@76wj3!6vvr)1qv^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'HOST': 'localhost',
#         'NAME': 'ffooty',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres101',
#         'OPTIONS': {'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_READ_UNCOMMITTED}
#     }
# }
# DATABASE_OPTIONS = {
#     "autocommit": True,
# }
DEFAULT_FILE_STORAGE = 'storage.handlers.DatabaseStorage'

########## IN-MEMORY TEST DATABASE CONFIGURATION
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
#         "ATOMIC_REQUESTS": True,
    },
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'noreply.azff@gmail.com'
EMAIL_HOST_PASSWORD = 'astraffootyzeneca'
DEFAULT_FROM_EMAIL = 'noreply.azff@gmail.com'
DEFAULT_TO_EMAIL = 'danj1974@gmail.com'
