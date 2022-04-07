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
       'ENGINE': env("POSTGRES_ENGINE"),
       'NAME': env("POSTGRES_DB"),
       'USER': env("POSTGRES_USER"),
       'PASSWORD': env("POSTGRES_PASSWORD"),
       'HOST': env("PG_HOST"),   # Or an IP Address that your DB is hosted on
       'PORT': env("PG_PORT"),
   }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# MYSQL_ENGINE=django.db.backends.mysql
# MYSQL_DB=user_management
# MYSQL_USER=root
# MYSQL_PASSWORD=root
# MYSQL_HOST=mysql-db
# MYSQL_PORT=3306
