import os

DEBUG=True
TIME_ZONE='Asia/Shanghai'
#LANGUAGE_CODE = 'zh-cn'

ROOT_URLCONF = 'urls'  # Replace 'project.urls' with just 'urls'

appdir = os.path.abspath(os.path.dirname(__file__))
LOCALE_PATHS = (
    os.path.join(appdir, 'i18n', 'locale'),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
#    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

INSTALLED_APPS = (
#    'django.contrib.auth',
    'django.contrib.contenttypes',
#    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize'
)

ROOT_PATH = os.path.dirname(__file__)
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".  Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ROOT_PATH + '/templates',
)
