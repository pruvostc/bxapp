#!/usr/bin/env python3.7
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
    
    RUNNING_ENV = 'prod' #default
    if (len(sys.argv) > 1 and sys.argv[1] == 'runserver'):
        RUNNING_ENV = 'dev' # running in dev environment
    os.environ.setdefault('RUNNING_ENV', RUNNING_ENV)
    print("Running in mode = ", RUNNING_ENV)
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
