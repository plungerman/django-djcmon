# -*- coding: utf-8 -*-
import os

DEBUG = False
#DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('larry@example.com'),
)
MANAGERS = ADMINS

AUTH_PROFILE_MODULE = 'core.UserProfile'
# databases
DATABASES = {
    'default': {
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': '',
        'ENGINE': 'django.db.backends.mysql',
        'USER': '',
        'PASSWORD': ''
    },
}
# SQL Alchemy connection string values
SQLALQ_USERNAME=""
SQLALQ_PASSWORD=""
SQLALQ_HOST=""
SQLALQ_PORT=""
SQLALQ_DATABASE=""
# language & date/time
TIME_ZONE = 'America/Chicago'
USE_TZ = False
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'
MEDIA_ROOT = '/data2/django_projects/communications/assets'
MEDIA_URL = '/assets/'
STATIC_URL = '/sdjmedia/'
ROOT_URL = '/communications/'
SERVER_URL = "www.example.com"
API_URL = "%s/%s" % (SERVER_URL, "api")
STATIC_ROOT = ''
ROOT_URLCONF = 'communications.urls'
SECRET_KEY = ''
# Additional locations of static files
STATICFILES_DIRS = (
    # Don't forget to use absolute paths, not relative paths.
)
# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
EMAIL_HOST = 'smtp.example.com'
EMAIL_HOST_USER = 'smtpuser@example.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_NOTIFICATION = ["arobillard@carthage.edu",]
DEFAULT_FROM_EMAIL = 'support@example.com'
SERVER_EMAIL = 'support@example.com'
SERVER_MAIL='support@example.com'
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
# template stuff
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.dirname(__file__), 'templates'),
            "/data2/django_templates/djkorra/",
            "/data2/django_templates/djcher/",
            "/data2/django_templates/",
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "djtools.context_processors.sitevars",
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.core.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                #'allauth specific context processors',
                #'allauth.account.context_processors.account',
                #'allauth.socialaccount.context_processors.socialaccount',
            ],
            #'loaders': [
            #    # insert your TEMPLATE_LOADERS here
            #]
        },
    },
]
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.admin',
    'communications',
)
# LDAP Constants
LDAP_SERVER = ""
LDAP_PORT = "389"
LDAP_PROTOCOL = "ldap"
LDAP_BASE = "o="
LDAP_USER = "cn=, o="
LDAP_PASS = ""
LDAP_EMAIL_DOMAIN = "example.com"
LDAP_OBJECT_CLASS = "carthageUser"
# auth backends
AUTHENTICATION_BACKENDS = (
    'djauth.ldapBackend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = '/communications/accounts/login/'
LOGOUT_URL = '/communications/accounts/logout/'
LOGIN_REDIRECT_URL = '/communications/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_DOMAIN=".example.com"
SESSION_COOKIE_NAME ='django_cookie'
SESSION_COOKIE_AGE = 86400
# Campaign Monitor API
CARTHAGE_CM_ID = ''
HIDDEN_CM_ID = ''
API_KEY = ''
# we use a list of tuples so that we can control the order,
# whereas a dictionary would not that.
DESCRIPTIONS = [
    ("",""),
]
# Logging
LOG_FILEPATH = os.path.join(os.path.dirname(__file__), "logs/")
LOG_FILENAME = LOG_FILEPATH + "debug.log"
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
