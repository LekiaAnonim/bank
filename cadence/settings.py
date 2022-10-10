"""
Django settings for cadence project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
import environ
import sys
import cloudinary
import cloudinary.uploader
import cloudinary.api
# import cloudinary_storage
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECRET_KEY = env('SECRET_KEY')
# SECRET_KEY = os.environ.get('SECRET_KEY')
from django.core.management.utils import get_random_secret_key


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# DEBUG = 'RENDER' not in os.environ
# DEBUG = os.getenv("DEBUG", False) == True

ALLOWED_HOSTS = ['bank-production.up.railway.app', '127.0.0.1', '127.0.0.1:8000', 'cadenceportal.com']

# ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
# RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')if RENDER_EXTERNAL_HOSTNAME:    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap_datepicker_plus',
    'cloudinary_storage',
    'cloudinary', 
    'bank.apps.BankConfig',
    'localflavor',
    'phonenumber_field',
    'mathfilters',
    
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cadence.urls'

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
OTP_EMAIL_TOKEN_VALIDITY = 3600
OTP_EMAIL_SENDER = os.getenv('OTP_EMAIL_SENDER')
WSGI_APPLICATION = 'cadence.wsgi.application'
OTP_EMAIL_BODY_TEMPLATE = 'Use the OTP provided below verify your transaction'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': dj_database_url.config(default='postgresql://postgres:postgres@localhost:5432/cadence', conn_max_age=600)}

# DATABASE_URL = os.getenv('DATABASE_URL')
# DEVELOPMENT_MODE = False
# if DEVELOPMENT_MODE is True:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#         }
#     }
# elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
#     if os.getenv("DATABASE_URL", None) is None:
#         raise Exception("DATABASE_URL environment variable not defined")
DATABASES = {
    "default": dj_database_url.config(default='postgresql://postgres:ZZcOfjZpOKSQMF5W02ej@containers-us-west-66.railway.app:7303/railway', conn_max_age=1800),
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
# STATICFILES_STORAGE = 'cloudinary_strorage.storage.StaticHashedCloudCloudinaryStorage'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# STATIC_ROOT = "/var/www/bank-production.up.railway.app/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "bank/static"),)
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': 'lekiaprosper',
#     'API_KEY': os.getenv('API_KEY'),
#     'API_SECRET': os.getenv('API_SECRET'),
# }
cloudinary.config( 
  cloud_name = "lekiaprosper", 
  api_key = "666558139559246", 
  api_secret = "msWiQ9tiGPF5oT28VwwaZz_bXSA",
)
# CLOUDINARY_URL='cloudinary://666558139559246:msWiQ9tiGPF5oT28VwwaZz_bXSA@lekiaprosper'
# MEDIA SETTINGS
MEDIA_URL = '/media/'
# DEFAULT_FILE_STORAGE = 'cloudinary_strorage.storage.MediaCloudinaryStorage'
# 
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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



CSRF_TRUSTED_ORIGINS = ['https://bank-production.up.railway.app', 'https://cadenceportal.com']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')
CSRF_USE_SESSIONS = False
# SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_DOMAIN = 'bank-production.up.railway.app'
SECURE_BROWSER_XSS_FILTER = True

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True


SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_FRAME_DENY = True
SECURE_HSTS_SECONDS = 2592000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'same-origin'

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

USE_L10N = True
DATE_INPUT_FORMATS = ['%m/%d/%Y']


ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "/customer/%s/update/" % u.id,
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('OTP_EMAIL_SENDER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = "Lekiaprosper@gmail.com"

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = ''
LOGIN_REDIRECT_URL = '/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
