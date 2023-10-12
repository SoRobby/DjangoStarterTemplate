"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import logging
import os
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load and read the environment variables from the .env file
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-bzju(z51ab74xysdqadr&g!ig!pawtlyzz52_pzs)8do+i=io6')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)

# SECURITY WARNING: don't run with debug turned on in production!
ENABLE_DEBUG_TOOLBAR = env.bool('ENABLE_DEBUG_TOOLBAR', default=True)

# Set this value to True to have URLs generated with https instead of http
# SECURITY WARNING: set to True in production
USE_HTTPS_IN_ABSOLUTE_URLS = env.bool("USE_HTTPS_IN_ABSOLUTE_URLS", default=False)

# The fully qualified domain name associated with the website
SITE_ID = 1

# The site domain
SITE_DOMAIN = '127.0.0.1:8000'

ALLOWED_HOSTS = ['127.0.0.1']

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
]

# Third party apps
THIRD_PARTY_APPS = [
    'django_ckeditor_5',
]

# Project apps
PROJECT_APPS = [
    'apps.accounts',
    'apps.adminpanel',
    'apps.analytics',
    'apps.blog',
    'apps.feedback',
    'apps.main',
    'apps.profiles'
]

# Installed apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.analytics.middleware.AnalyticsMiddleware',
]

# Conditional app
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
if ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1']

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # Project / app context_processors
                'apps.main.context_processors.google_analytics_id',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

AUTH_USER_MODEL = 'accounts.Account'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
    'apps.accounts.backends.CaseInsensitiveModelBackend',
)

LOGIN_URL = 'login'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'libs/npm/node_modules/cropperjs/dist/',
    BASE_DIR / 'libs/npm/node_modules/alpinejs/dist/',
    BASE_DIR / 'libs/npm/node_modules/@alpinejs/',
    BASE_DIR / 'libs/npm/node_modules/htmx.org/dist/',
    BASE_DIR / 'libs/npm/node_modules/@ckeditor/',
    BASE_DIR / 'libs/npm/node_modules/jquery/dist/',
]

# Media files (Images, Videos, etc...)
# https://docs.djangoproject.com/en/4.2/topics/files/

MEDIA_ROOT = BASE_DIR / 'media'

MEDIA_URL = 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Session cookie age in seconds. Can be used to avoid log sessions (# days x 24 hrs x 60 min x 60 sec)
# The current value is 7 days until the cookies expire
# Ref 1: https://docs.djangoproject.com/en/4.1/topics/http/sessions/

SESSION_COOKIE_AGE = 7 * 24 * 60 * 60

# Email configuration
# https://docs.djangoproject.com/en/4.1/ref/settings/
# https://docs.djangoproject.com/en/4.1/topics/email/#email-backends

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'localhost'

EMAIL_PORT = '1025'

EMAIL_HOST_USER = ''

EMAIL_HOST_PASSWORD = ''

EMAIL_USE_TLS = False

EMAIL_USE_SSL = False

# Google analytics ID
# https://support.google.com/analytics/answer/9304153
GOOGLE_ANALYTICS_ID = env('GOOGLE_ANALYTICS_ID', default='')

# Google reCAPTCHA secret key
RECAPTCHA_SECRET_KEY = env('RECAPTCHA_SECRET_KEY', default='')

# Django templating multiline template tags
MULTILINE_TEMPLATE_TAGS = env.bool('MULTILINE_TEMPLATE_TAGS', default=False)

# Logging configuration
LOG_LEVEL = env('LOG_LEVEL', default='DEBUG')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'colorize': {
            '()': 'config.configurator.ColorizeFilter'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'custom',
            'filters': ['colorize'],
        },
    },
    'formatters': {
        'custom': {
            'format': '[{asctime}] {levelname} | {message}',
            'style': '{',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': LOG_LEVEL,
    },
}

# Log server errors
# TODO - Make this option into an environment variable. Also test to make sure it works and understand how it works.
# if True:
#     LOGGING['loggers'] = {
#         'django': {
#             'handlers': ['console'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#     }

# CKEditor5 settings
customColorPalette = [
    {'color': 'hsl(4, 90%, 58%)', 'label': 'Red'},
    {'color': 'hsl(340, 82%, 52%)', 'label': 'Pink'},
    {'color': 'hsl(291, 64%, 42%)', 'label': 'Purple'},
    {'color': 'hsl(262, 52%, 47%)', 'label': 'Deep Purple'},
    {'color': 'hsl(231, 48%, 48%)', 'label': 'Indigo'},
    {'color': 'hsl(207, 90%, 54%)', 'label': 'Blue'},
]

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],

    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
                    'code', 'subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                    'bulletedList', 'numberedList', 'todoList', '|', 'blockQuote', 'imageUpload', '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                    'insertTable', ],
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side', '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]

        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells',
                               'tableProperties', 'tableCellProperties'],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3'}
            ]
        }
    },
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        }
    }
}

CKEDITOR_5_FILE_STORAGE = "apps.blog.storage.CustomStorage"
