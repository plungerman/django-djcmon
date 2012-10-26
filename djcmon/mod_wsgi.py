import os, sys

sys.path.append('/usr/lib/python2.6/dist-packages/')
sys.path.append('/usr/lib/python2.6/')
sys.path.append('/data2/django_projects/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'djcmon.settings'
os.environ['PYTHON_EGG_CACHE'] = '/var/cache/python/.python-eggs'
os.environ['TZ'] = 'America/Chicago'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
