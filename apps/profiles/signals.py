# to ensure a user's profile is created whenever a user instance
# is created.
# ---
# Signals in a nuttshell:
# Signals allow certain senders to notify a set of receivers
# that some action has taken place
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.profiles.models import Profile
from user_management.settings.base import AUTH_USER_MODEL

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    logger.info(f"{instance}'s profile created")