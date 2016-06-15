""" https://docs.djangoproject.com/en/1.9/ref/settings/ """
from django.utils.translation import ugettext_lazy as _
from huey import RedisHuey
from urllib.parse import urlparse
import dj_database_url
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0lw6f3ql#p38p2tt-9=j^!z^95bck35v@cldm+utdq2m&^0@z#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'django_extensions',
    'huey.contrib.djhuey',
    'rest_framework',
]

INSTALLED_APPS += [
    'p2coffee',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'coffeesite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'coffeesite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
if os.getenv('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config()

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGES = [
    ('en', _('English')),
    ('nb', _('Norwegian')),
]
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'en')
TIME_ZONE = os.getenv('TIME_ZONE', 'UTC')
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Huey worker
rconn = urlparse(os.environ.get('REDISTOGO_URL', 'redis://localhost:6379'))
rconn = {'host': rconn.hostname, 'port': rconn.port, 'password': rconn.password}
HUEY = RedisHuey('coffeesite', result_store=False, **rconn)

# Slack
SLACK_API_URL_BASE = 'https://slack.com/api/'
SLACK_API_TOKEN = os.getenv('SLACK_API_TOKEN')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL', '#im-a-coffeepot')
SLACK_BOT_USERNAME = os.getenv('SLACK_BOT_USERNAME', 'Kaffetrakteren')
SLACK_BOT_ICON_URL = os.getenv('SLACK_BOT_ICON_URL', 'https://p2coffee.herokuapp.com/static/images/icon.jpg')

# Lifx
LIFX_TOKEN = ''

# Coffee camera settings
COFFEE_CAMERA_URL = os.getenv('COFFEE_CAMERA_URL', 'http://195.159.182.134:8080/cam/1')
COFFEE_CAMERA_USER = os.getenv('COFFEE_CAMERA_USER')
COFFEE_CAMERA_PASS = os.getenv('COFFEE_CAMERA_PASS')

# Brewing settings
BREWTIME_AVG_MINUTES = int(os.getenv('BREWTIME_AVG_MINUTES', '4'))

try:
    from .local_settings import *
except ImportError:
    pass
