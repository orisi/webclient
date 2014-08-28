"""
Django settings for orisiclient project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


from orisiclient.settings_local import (
    SECRET_KEY,
    DEBUG,
    LESSC_PATH,
    USE_SYSLOG,
    TEMPLATE_DEBUG,
    ALLOWED_HOSTS,
    COMPRESS_ENABLED,
    DATABASES,
    ADMINS)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'orisiclient.apps.main',
    'orisiclient.apps.fastcast',

    'widget_tweaks',
    'compressor',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'orisiclient.middleware.ExceptionLoggingMiddleware',
)

ROOT_URLCONF = 'orisiclient.urls'

WSGI_APPLICATION = 'orisiclient.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    'orisiclient/templates/',
)

COMPRESS_ROOT = os.path.join(BASE_DIR, 'orisiclient', 'static')

COMPRESS_PRECOMPILERS = (
    ('text/less', '%s {infile} {outfile}' % LESSC_PATH),
)
