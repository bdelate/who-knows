import psycopg2
from .base import *


DEBUG = True

SECRET_KEY = '8*(2&rjotxh84$x9jh+o*6!3@ij*^ulfxv!994h$xn3!u@hins'

ADMIN_URL = 'admin/'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'db',
        'PORT': '',
    }
}

# debug toolbar related settings
INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
