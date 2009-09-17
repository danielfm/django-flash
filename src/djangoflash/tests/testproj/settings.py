# Django settings for testproj project.

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'db'

SECRET_KEY = 'g9b@q$)=^xd2g@-7pg=j=h3*8+xd#hgn-9je@iq5_m#seg&d1y'

MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/admin/'
MEDIA_ROOT = os.path.normpath(os.path.dirname(__file__) + '/media/')

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'djangoflash.middleware.FlashMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'djangoflash.context_processors.flash',
    'django.core.context_processors.media',
)

ROOT_URLCONF = 'testproj.urls'

TEMPLATE_DIRS = (
    os.path.normpath(os.path.dirname(__file__) + '/templates'),
)

INSTALLED_APPS = (
    'app',
    'django.contrib.sessions',
)

# FLASH_STORAGE      = 'session' # or 'cookie'
# FLASH_IGNORE_MEDIA = True # or False
