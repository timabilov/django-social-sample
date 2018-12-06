"""
WSGI config for socialplatform project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.conf import settings

from dj_static import Cling, MediaCling

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "socialplatform.settings")

if settings.DEBUG:
    application = get_wsgi_application()

else:
    # FOR production configuration checking with proper static assets handling.
    application = Cling(get_wsgi_application())
