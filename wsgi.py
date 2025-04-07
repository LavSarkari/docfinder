import os
import sys

# Add project directory to path
path = '/home/lavsarkari/www/doctorfinder'
if path not in sys.path:
    sys.path.append(path)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'doctorfinder.settings'

# Import Django WSGI handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application() 