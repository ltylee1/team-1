"""
Django settings for unitedairway project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from django.contrib.messages import constants

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&dew+9cr-@+uwd$7c!@ppf9+l2d%q292$u99hnx2f_s8(i(y+m'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['54.190.37.76', '127.0.0.1', 'localhost']

# provide our get_profile()
AUTH_PROFILE_MODULE = 'uw-dashboard.UserProfile'

# URL for @login_required decorator to use
LOGIN_URL = '/login.html'

# redirect authenticated users
LOGIN_REDIRECT_URL = '/profile.html'

SESSION_SECURITY_EXPIRE_AFTER= 10 * 60 # logout after 10 minutes of inactivity
SESSION_SECURITY_WARN_AFTER= 8 * 60 # logout warning after 8 minutes of inactivity
SESSION_EXPIRE_AT_BROWSER_CLOSE=True

# ROOT FOR ALL MEDIA
MEDIA_ROOT = "uw-dashbaord/static/media"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'uw_dashboard',
    'session_security',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
]

ROOT_URLCONF = 'unitedairway.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'unitedairway.wsgi.application'

MESSAGE_TAGS = {
    constants.DEBUG: 'debug',
    constants.INFO: 'info',
    constants.SUCCESS: 'success',
    constants.WARNING: 'warning',
    constants.ERROR: 'danger',
}

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'unitedWay',
        'USER': 'unitedWay',
        'PASSWORD': 'Etfhg8893',
        'HOST': 'uw-test.cromnho1ocid.us-west-2.rds.amazonaws.com',
        'PORT': '3306',
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

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/uw_dashboard/static/'
STATIC_ROOT = ''
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "uw_dashboard/templates"),
]
