"""Common settings and globals."""


from datetime import timedelta
import os
from os.path import abspath, basename, dirname, join, normpath, exists
from sys import path
from django.core.files.storage import FileSystemStorage

from djcelery import setup_loader


########## PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

APP_TITLE_SHORT = 'Django Full stack UI Development'

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
########## END PATH CONFIGURATION


DEBUG = bool(os.environ.get('DJANGO_DEBUG', ''))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION

OFFLINE = False

TEST = False

########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Adam Spence', 'aspence1@gmail.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
########## END DATABASE CONFIGURATION

########## JOHNNY CACHE ############
CACHES = {
    'default': dict(
        BACKEND='johnny.backends.memcached.MemcachedCache',
        LOCATION=['127.0.0.1:11211'],
        JOHNNY_CACHE=True,
    )
}

#DISABLE_QUERYSET_CACHE = True
JOHNNY_MIDDLEWARE_KEY_PREFIX = 'jc_uidev'

# may be able to remove this list
MAN_IN_BLACKLIST = ['auth_group', 'auth_group_permissions', 'auth_permissions',
                    'auth_user', 'auth_user_groups', 'auth_user_user_permissions']

CACHE_KEY_PREFIX = SITE_NAME

# this setting shouldn't be overriden
CACHE_PAGES = False

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)


########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'Europe/London'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-gb'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
########## END GENERAL CONFIGURATION


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(DJANGO_ROOT, 'static'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
#STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    normpath(join(DJANGO_ROOT, 'assets')),
    normpath(join(SITE_ROOT, '_generated_media')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
########## END STATIC FILE CONFIGURATION

MEDIA_ROOT = normpath(join(DJANGO_ROOT, 'assets'))
MEDIA_URL = '/media/'

########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = r"h60%xcepe2v89$y#(q$wh+8^l1m0$ob4%8y11-_#(2slxha_h)"
########## END SECRET CONFIGURATION


########## FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    normpath(join(DJANGO_ROOT, 'fixtures')),
)
########## END FIXTURE CONFIGURATION


########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'apps.utils.context_processors.addvars',
    'apps.utils.context_processors.menu_items',
#    'apps.utils.context_processors.tweets',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    normpath(join(DJANGO_ROOT, 'templates')),
)
########## END TEMPLATE CONFIGURATION


########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    'mediagenerator.middleware.MediaMiddleware',
    'johnny.middleware.LocalStoreClearMiddleware',
    'johnny.middleware.QueryCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',

    # Default Django middleware.
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
########## END MIDDLEWARE CONFIGURATION


########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % SITE_NAME
########## END URL CONFIGURATION


########## APP CONFIGURATION
DJANGO_APPS = (
    'mediagenerator',
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.comments',

    # Useful template tags:
    'django.contrib.humanize',

    # Admin panel and documentation:
    'django.contrib.admin',
    'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    # Database migration helpers:
    'south',
    'djcelery',
    'ckeditor',
    'mustachejs',
    'tastypie',
    'django_nose',
    'memcache_status',
    'django_extensions',
    'taggit',
)

LOCAL_APPS = (
    'apps.utils',
    'apps.base',
    'apps.pages',
    'apps.api',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
########## END APP CONFIGURATION


########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'plain': {
            'format': '%(asctime)s %(message)s'},
        },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        },
#        'file': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': join(SITE_ROOT, 'logs', 'uidev.log'),
#             'maxBytes': 1024*1024*5, # 5 MB
#             'backupCount': 5,
#        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'propagate': True,
        },
        'whitelabel': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.middleware.cache': {
            'handlers': ['console'],
            'propagate': False,
        },
        'johnny.middleware': {
            'handlers': ['console'],
            'propagate': False,
        }
    }
}
########## END LOGGING CONFIGURATION


########## CELERY CONFIGURATION
# See: http://celery.readthedocs.org/en/latest/configuration.html#celery-task-result-expires
#CELERY_TASK_RESULT_EXPIRES = timedelta(minutes=30)

# See: http://celery.github.com/celery/django/
#setup_loader()
########## END CELERY CONFIGURATION


########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'
########## END WSGI CONFIGURATION

# we use nosetests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_PLUGINS = [
     ('nose_plugins.SilenceSouth'),
]


########## COMPRESSION CONFIGURATION
# See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_ENABLED
###MEDIAGENERATOR
PROJECT_ROOT = SITE_ROOT
#Configure yuicompressor if available
YUICOMPRESSOR_PATH = join(PROJECT_ROOT, 'yuicompressor-2.4.7.jar')
if exists(YUICOMPRESSOR_PATH) and not DEBUG:

    ROOT_MEDIA_FILTERS = {
        'js': 'mediagenerator.filters.yuicompressor.YUICompressor',
        'css': 'mediagenerator.filters.yuicompressor.YUICompressor',
    }

MEDIA_DEV_MODE = False

GLOBAL_MEDIA_DIRS = (
    join(PROJECT_ROOT, 'imported-sass-frameworks'),
)

SASS_FRAMEWORKS = (
    'compass',
    'blueprint',
    'susy',
)

from bundles import MEDIA_BUNDLES

########## END COMPRESSION CONFIGURATION

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            [      'Undo', 'Redo',
              '-', 'Bold', 'Italic', 'Underline',
              '-', 'Link', 'Unlink', 'Anchor',
              '-', 'Format',
              '-', 'SpellChecker', 'Scayt',
              '-', 'Maximize',
            ],
            [      'HorizontalRule',
              '-', 'BulletedList', 'NumberedList',
              '-', 'Cut','Copy','Paste','PasteText','PasteFromWord',
              '-', 'SpecialChar',
              '-', 'Source',
              '-', 'About',
            ]
        ],
        'width': 840,
        'height': 300,
        'toolbarCanCollapse': False,
    }
}

CKEDITOR_UPLOAD_PATH = normpath(join(DJANGO_ROOT, 'assets'))
ALLOWED_TAGS = ['a', 'img', 'em', 'strong', 'h1', 'h2', 'h3', 'ul', 'li', 'p', 'ol', 'div', 'hr', 'span']

MUSTACHEJS_DIRS = [
    join(DJANGO_ROOT, "templates", "pages", "js"),
]

#MUSTACHEJS_PREPROCESSORS = [
#    'apps.utils.template_preprocessors.PageContent'
#]
