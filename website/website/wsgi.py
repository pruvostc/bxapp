"""
WSGI config for website project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys

# add your project directory to the sys.path
project_home = u'/home/crispy/website'
if project_home not in sys.path:
    sys.path.insert(0, project_home)
    
# set environment variable to tell django where your settings.py is
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
os.environ.setdefault('RUNNING_ENV', 'prod')

# serve django via WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
