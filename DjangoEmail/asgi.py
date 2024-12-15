"""
ASGI config for DjangoEmail project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
import logging

logger = logging.getLogger('notification')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoEmail.settings')

logger.info('ASGI application is starting up.')
application = get_asgi_application()
logger.info('ASGI application is ready.')
