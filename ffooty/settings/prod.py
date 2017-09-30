from __future__ import absolute_import

from .base import *
import psycopg2.extensions


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': 'ffooty',
        'USER': 'postgres',
        'PASSWORD': 'postgres101',
        'OPTIONS': {'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_READ_UNCOMMITTED}
    }
}
DATABASE_OPTIONS = {
    "autocommit": True,
}
DEFAULT_FILE_STORAGE = 'storage.handlers.DatabaseStorage'


