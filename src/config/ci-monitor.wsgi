import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'ci_monitor.settings'
#sys.path.append('/Users/devroot/.virtualenvs/ci-monitor/lib/python2.7/site-packages')
sys.path.append('/opt/ci-monitor/src')
sys.path.append('/opt/ci-monitor/src/ci_monitor')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
