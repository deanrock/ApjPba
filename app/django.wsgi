import os
import sys

sys.path.append('/websites/apjpba/app')
sys.path.append('/websites/apjpba/app/apjpba')
#os.environ['PYTHON_EGG_CACHE'] = '/websites/apjpba/app/.python-egg'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
