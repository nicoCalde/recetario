"""
WSGI config for recetario project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import sys

path = '/home/caldegol/caldegol.pythonanywhere.com/recetario'
if path not in sys.path:
    sys.path.insert(0, path)

from django.core.wsgi import get_wsgi_application

os.environ["DJANGO_SETTINGS_MODULE"] = "recetario.settings"

application = get_wsgi_application()
