from __future__ import absolute_import

from .base import *
# import psycopg2.extensions
import os
import sys

# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'umu8tj3a&k_6zv69-(8w!xj32a64m$kaiu@76wj3!6vvr)1qv^'

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


# Testing
#SELENIUM_WEBDRIVER = 'firefox'
#SELENIUM_WEBDRIVER = 'phantomjs'
# LETTUCE_APPS = ('ffooty')
#LETTUCE_TEST_SERVER = 'lettuce.django.server.DjangoServer'
LETTUCE_SERVER_PORT = 8999
LETTUCE_USE_TEST_DATABASE = True

# from previous settings
# ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# as recommended for openshift deployment:
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, '../wsgi', 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, '../wsgi', 'static', 'media')
STATICFILES_DIRS = (os.path.join(BASE_DIR, '../static'),)
TEMPLATE_DIRS = (os.path.join(BASE_DIR, '../templates'),)

# further openshift config:

ON_OPENSHIFT = False
if 'OPENSHIFT_REPO_DIR' in os.environ:
    ON_OPENSHIFT = True

if ON_OPENSHIFT:
    DJ_PROJECT_DIR = os.path.dirname(__file__)
    BASE_DIR = os.path.join('..', os.path.dirname(DJ_PROJECT_DIR))
    WSGI_DIR = os.path.join(BASE_DIR, 'wsgi')
    REPO_DIR = os.environ.get('OPENSHIFT_REPO_DIR', BASE_DIR)
    DATA_DIR = os.environ.get('OPENSHIFT_DATA_DIR', BASE_DIR)

    print "DJ_PROJECT_DIR =", DJ_PROJECT_DIR
    print "BASE_DIR =", BASE_DIR
    print "WSGI_DIR =", WSGI_DIR
    print "REPO_DIR =", REPO_DIR
    print "DATA_DIR =", DATA_DIR

    DEBUG = True
    TEMPLATE_DEBUG = False
    ALLOWED_HOSTS = ['*']
    # SECRET_KEY = os.environ['OPENSHIFT_SECRET_TOKEN']
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #         'NAME': 'ffooty',
    #         'USER': os.getenv('OPENSHIFT_POSTGRESQL_DB_USERNAME'),
    #         'PASSWORD': os.getenv('OPENSHIFT_POSTGRESQL_DB_PASSWORD'),
    #         'HOST': os.getenv('OPENSHIFT_POSTGRESQL_DB_HOST'),
    #         'PORT': os.getenv('OPENSHIFT_POSTGRESQL_DB_PORT'),
    #     }
    # }
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(DATA_DIR, 'db.sqlite3'),
        }
    }

    sys.path.append(os.path.join(REPO_DIR, 'libs'))
    from libs import secrets
    SECRETS = secrets.getter(os.path.join(DATA_DIR, 'secrets.json'))

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = SECRETS['secret_key']


    # PHANTOMJS_PATH = './footy/phantomjs64'

# Openshift logging config (https://blog.openshift.com/migrating-django-applications-openshift-3/)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}
