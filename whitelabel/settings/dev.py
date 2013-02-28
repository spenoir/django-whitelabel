"""Development settings and globals."""
from django.core.urlresolvers import reverse

from os.path import join, normpath

from common import *


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION

OFFLINE = False

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
       'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': 'default.db',
       'USER': '',
       'PASSWORD': '',
       'HOST': '',
       'PORT': '',
   }
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PASSWORD': 'spin',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION


########## CELERY CONFIGURATION
# See: http://docs.celeryq.org/en/latest/configuration.html#celery-always-eager
CELERY_ALWAYS_EAGER = True
########## END CELERY CONFIGURATION


########## TOOLBAR CONFIGURATION
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INSTALLED_APPS += (
    'debug_toolbar',
    'milkman',
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INTERNAL_IPS = ('127.0.0.1',)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
########## END TOOLBAR CONFIGURATION

PAGE_CACHE_TIME = 60*1 # 1 min for staging, increase this in production
CACHE_KEY_PREFIX = 'a'

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS' : False
}

STATIC_URL = '/static/'

MEDIA_DEV_MODE = True
DEV_MEDIA_URL = '/devmedia/'

NOSE_ARGS = ('-s', '--exe',
#             '--exclude-dir-file=nose-exclude.txt',
             '--with-progressive'
)

JS_GLOBAL_VARS = {
    'DEBUG': DEBUG,
    'MEDIA_URL': MEDIA_URL,
    'defaultSlug': 'home',
    'pageLoad': True
}
