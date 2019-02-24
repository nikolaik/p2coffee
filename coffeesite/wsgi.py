"""
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coffeesite.settings")

application = get_wsgi_application()
