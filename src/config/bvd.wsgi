import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'bvd.settings'
sys.path.append('/opt/bvd/src')
sys.path.append('/opt/bvd/src/bvd')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()