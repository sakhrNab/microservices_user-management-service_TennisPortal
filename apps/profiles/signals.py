# to ensure a user's profile is created whenever a user instance
# is created.
# ---
# Signals in a nuttshell:
# Signals allow certain senders to notify a set of receivers
# that some action has taken place
import ast
import json
import logging
from json import JSONEncoder
from uuid import UUID

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.profiles.models import Profile
from apps.profiles.serializers import ProfileSerializer
from user_management.settings.base import AUTH_USER_MODEL

from .producer import RabbitMq

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()

        profile_id_str = str(instance.profile)
        data = {'id': profile_id_str,
                "username": instance.username,
                'is_admin': str(instance.is_staff)}
        p = RabbitMq()
        RabbitMq.publish(p, 'profile_created', data)

        logger.info(f"{instance}'s profile created {dict}")

