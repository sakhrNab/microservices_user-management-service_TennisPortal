from __future__ import absolute_import, unicode_literals
from celery import shared_task
from apps.profiles.models import Profile
from django.contrib.auth import get_user_model


@shared_task
def post_signup_welcome_mail(userpk=None):

    print("Welcome user with id: ", userpk['id'])

