#!/usr/bin/env python
import os
import sys

from django.core.wsgi import get_wsgi_application


path = '/home/danj1974/ffooty'

if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'ffooty.settings.python_anywhere'

application = get_wsgi_application()
