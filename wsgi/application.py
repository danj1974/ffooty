#!/usr/bin/env python

from distutils.sysconfig import get_python_lib
import os
import sys

import django.core.wsgi

# GETTING-STARTED: make sure the next line points to your settings.py:
os.environ['DJANGO_SETTINGS_MODULE'] = 'ffooty.settings.openshift'

# GETTING-STARTED: make sure the next line points to your django project dir:
sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'ffooty'))

os.environ['PYTHON_EGG_CACHE'] = get_python_lib()

application = django.core.wsgi.get_wsgi_application()