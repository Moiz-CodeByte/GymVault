"""WSGI config for gymvaultproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Check if we're running on Heroku
if 'DYNO' in os.environ:
    # Use production settings for Heroku
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gymvaultproject.settings_production')
else:
    # Use development settings for local environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gymvaultproject.settings')

application = get_wsgi_application()
