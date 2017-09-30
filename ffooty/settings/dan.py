from __future__ import absolute_import

from .base import *
import psycopg2.extensions

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'umu8tj3a&k_6zv69-(8w!xj32a64m$kaiu@76wj3!6vvr)1qv^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

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


# Testing
#SELENIUM_WEBDRIVER = 'firefox'
#SELENIUM_WEBDRIVER = 'phantomjs'
# LETTUCE_APPS = ('ffooty')
#LETTUCE_TEST_SERVER = 'lettuce.django.server.DjangoServer'
LETTUCE_SERVER_PORT = 8999
LETTUCE_USE_TEST_DATABASE = True

# from previous settings
# ALLOWED_HOSTS = ['localhost', '127.0.0.1']


