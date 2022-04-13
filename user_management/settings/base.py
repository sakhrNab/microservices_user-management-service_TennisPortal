from datetime import timedelta
import os
from pathlib import Path

import environ

env = environ.Env(DEBUG=(bool, False))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()

environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")
#DEBUG = False

ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(" ")


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

SITE_ID = 1

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'phonenumber_field',
    'django_countries',
    'knox',
    'rest_framework_swagger',
    'django_filters'
]

LOCAL_APPS = [
    "apps.manage_user",
    "apps.common",
    'apps.profiles',
    'apps.ratings',
    'apps.email_requests',
    'custom_user',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'user_management.urls'

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

WSGI_APPLICATION = 'user_management.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER': 'custom_user.serializers.ResetPasswordEmailRequestSerializer'
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/staticfiles/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIR = []
MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = BASE_DIR / "mediafiles"

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.renderers.JSONRenderer',
        # 'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAuthenticated',

    ),
}

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
# ]

# CORS_ALLOW_ALL_ORIGINS=True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model
AUTH_USER_MODEL = "manage_user.User"

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': env("SIGNING_KEY"),
    'VERIFYING_KEY': None,
    "AUTH_HEADER_TYPES": (
        "Bearer",
        "JWT",
    ),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

import logging
import logging.config

from django.utils.log import DEFAULT_LOGGING

logger = logging.getLogger(__name__)

LOG_LEVEL = "INFO"

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
            },
            "file": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"},
            "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
            },
            "file": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "formatter": "file",
                "filename": "logs/user_management.log",
            },
            "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
        },
        "loggers": {
            "": {"level": "INFO", "handlers": ["console", "file"], "propagate": False},
            "apps": {"level": "INFO", "handlers": ["console"], "propagate": False},
            "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
        },
    }
)

DEFAULT_FROM_EMAIL="sakhr270@gmail.com"