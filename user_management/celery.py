from __future__ import absolute_import

import os

from celery import Celery
from user_management.settings import base

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_management.settings.development')

app = Celery("user_management")

app.config_from_object("user_management.settings.development", namespace="CELERY"),

app.autodiscover_tasks(lambda: base.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))