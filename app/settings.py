"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
# os
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-bc9)h+z&=ikl8z14hhi_ya1reb@91*a+)0r&0()!*2%y7ps1(&"

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'RENDER' not in os.environ
# 'api.westudy.global', '3.85.123.242', 
ALLOWED_HOSTS = ['*','localhost',]
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
# CORS Settings

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

X_FRAME_OPTIONS = "SAMEORIGIN"

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]


# Application definition

INTERNAL_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

PROJECT_APPS = [
    "westudy",
    "user",
    "university",
    "course",	
    "category",
    "modality",
    "typeofprogram",
    "shift",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "rest_framework.authtoken",
    "drf_spectacular",
    "corsheaders",
    "storages",
]

INSTALLED_APPS = INTERNAL_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'westudyapp',
        'USER': 'westudyapp_user',
        'PASSWORD': 'Qj2DfgdfgdfgDbzMrBPaSnVjz1ZXuznofBMeHb8q',
        'HOST': 'dpg-cha7fsak728rfdgfgfdgf885dk8h0-a.oregon-postgres.render.com',
        'PORT': '5432',
    },
    "old_default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')
MEDIA_URLS ='/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = (
    "westudy.User" # Cambiar el modelo de usuario para decirles que usen core
)

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema", # AutoSchema Swagger
}

# Django REST Framework

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        'westudy.jwt.CombinedJWTAuthentication',
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",

}

AUTHENTICATION_BACKENDS = [ 
    'westudy.auth.UniversityAuthenticationBackend',  # Backend personalizado de University
    'django.contrib.auth.backends.ModelBackend', # Backend por defecto de Django
]

# Django-Spectacular

SPECTACULAR_SETTINGS = {
    "TITLE": "Westudy API",
    "DESCRIPTION": "API for Westudy",
    "VERSION": "1.0.0",
    "CONTACT": {
        "name": "Westudy",
        "url": "https://westudy.com",
    },
    "LICENSE": {
        "name": "MIT",
        "url": "miguelalfaro2017@gmail.com",
    },
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
    },

}

# JWT USER AUTHENTICATION

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=600),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# Configuración para Backblaze B2
AWS_ACCESS_KEY_ID = #'fgdfgfg004117bd9eed44d0000000002'
AWS_SECRET_ACCESS_KEY = #'dfgfgK0048Lr5PwOZbYDI1EP5wzU/z59TtaI'
AWS_STORAGE_BUCKET_NAME = 'westudystorage'
AWS_S3_ENDPOINT_URL = 'https://s3.us-west-004.backblazeb2.com'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.us-west-004.backblazeb2.com' % AWS_STORAGE_BUCKET_NAME

""" AWS_ACCESS_KEY_ID = 'AKIA5F5H5ZWNXEPFGFGX'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'westudyglobal'
AWS_CUSTOME_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_S3_SIGNATURE_NAME = 's3v4',
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage' """




