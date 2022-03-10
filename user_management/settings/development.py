from .base import *

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_USE_TLS = True
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = "info@tenniscompanion.com"
DOMAIN = env("DOMAIN")
SITE_NAME = "Tennis Companion"
DATABASES = {
    'default': {
        'ENGINE': env("MYSQL_ENGINE"),
        'NAME': env("MYSQL_DB"),
        'USER': env("MYSQL_USER"),
        'PASSWORD': env("MYSQL_PASSWORD"),
        'HOST': env("MYSQL_HOST"),   # Or an IP Address that your DB is hosted on
        'PORT': env("MYSQL_PORT"),
    }
}
