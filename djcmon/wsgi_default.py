import os
import sys

# python
sys.path.append('/data2/python_venv/3.6/djcmon/lib/python3.6/')
sys.path.append('/data2/python_venv/3.6/djcmon/lib/python3.6/site-packages/')
# django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djcmon.settings")
os.environ.setdefault("PYTHON_EGG_CACHE", "/var/cache/python/.python-eggs")
os.environ.setdefault("TZ", "America/Chicago")
# wsgi
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
