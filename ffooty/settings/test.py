from __future__ import absolute_import
import os

from .base import *

# #from splinter import Browser
# 
# ########## TEST SETTINGS
# TEST_DISCOVER_TOP_LEVEL = BASE_DIR
# TEST_DISCOVER_ROOT = BASE_DIR
# TEST_DISCOVER_PATTERN = "tests/test_*.py"

DEBUG = True

TEMPLATE_DEBUG = True

########## IN-MEMORY TEST DATABASE CONFIGURATION
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        # "NAME": ":memory:",
        "NAME": os.path.join(BASE_DIR, "../data", "db.sqlite3"),
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
#         "ATOMIC_REQUESTS": True,
    },
}

########## END IN-MEMORY TEST DATABASE CONFIGURATION

########## LETTUCE TESTING CONFIGURATION
SELENIUM_WEBDRIVER = 'firefox'
# SELENIUM_WEBDRIVER = 'phantomjs'
LETTUCE_APPS = ('ffooty')
LETTUCE_AVOID_APPS = DJANGO_APPS + THIRD_PARTY_APPS
LETTUCE_TEST_SERVER = 'lettuce.django.server.DjangoServer'
LETTUCE_SERVER_PORT = 8999
LETTUCE_USE_TEST_DATABASE = True

# Setting for adding some test URLS for pluggable app tests
USE_TEST_URLS = True
########## END LETTUCE TESTING CONFIGURATION
