from .base import *

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'user_management',
#         'USER': 'root',
#         'PASSWORD': 'root',
#         'HOST': 'mysql-db',   # Or an IP Address that your DB is hosted on
#         'PORT': '3306', # the port used in our service
#     }
# }

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
