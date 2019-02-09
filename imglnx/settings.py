"""
BSD 3-Clause License

Copyright (c) 2017-2019 Russ 'trdwll' Treadwell. All rights reserved.
"""

import os
FILE_UPLOAD_PERMISSIONS = 0o644
APP_VERSION = '2.1.3'
CSRF_COOKIE_NAME = 'REDACTED'
LOGIN_URL = '/auth/login/'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HASH_LENGTH = 6
IMAGE_MAX_SIZE = 40 * (1024 * 1024) # 40MB
IMAGE_TYPES = [
    'image/gif',
    'image/png', 
    'image/x-citrix-png', # alt
    'image/x-png', # alt
    'image/jpeg',
    'image/x-citrix-jpeg', # alt
    'image/pjpeg', # alt
    'image/tiff',
    'image/x-icon',
    'image/bmp',
    'image/svg+xml',
    #'video/webm', # can contain audio
    #'video/x-webm', # idk lol
    #'audio/webm', # only audio
]
EXT = ['.png', '.gif', '.svg', '.ico', '.tiff', '.bmp', '.jpg', '.jpeg']
EXT_NOT_DOTTED = ['png', 'gif', 'svg', 'ico', 'tiff', 'bmp', 'jpg', 'jpeg']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'REDACTED'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'imglnx',
    'accounts',
    'blog',
    'api',
    'captcha',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'imglnx.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'imglnx.context_processors.global_settings', # gather global settings that we can use in a template
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'imglnx.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'imglnx',
        'USER': 'root',
        'PASSWORD': 'REDACTED',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}



# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
# I don't think this is necessary, but whatever
# STATIC_ROOT = '/var/www/imglnx.com/public_html/static'
STATIC_URL = '/static/'


#MEDIA_ROOT = os.path.join(BASE_DIR, 'i')
MEDIA_ROOT = '/var/www/i.imglnx.com/public_html/i'
#MEDIA_URL = '/i/'
MEDIA_URL = 'https://i.imglnx.com/'
ARCHIVES_ROOT = os.path.join(BASE_DIR, 'archives')
ARCHIVES_URL = '/archives/'

THUMBNAIL_ROOT = '/var/www/i.imglnx.com/public_html/thumbnail'
THUMBNAIL_URL = 'https://i.imglnx.com/thumbnail/'
#THUMBNAIL_ROOT = os.path.join(BASE_DIR, 'thumbnails')
#THUMBNAIL_URL = '/thumbnail/'
