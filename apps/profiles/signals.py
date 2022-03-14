# to ensure a user's profile is created whenever a user instance
# is created.
# ---
# Signals in a nuttshell:
# Signals allow certain senders to notify a set of receivers
# that some action has taken place
import logging, json, ast
from json import JSONEncoder
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import UUID
from apps.profiles.models import Profile
from user_management.settings.base import AUTH_USER_MODEL
from .producer import publish
from apps.profiles.serializers import ProfileSerializer

logger = logging.getLogger(__name__)


# class UUIDEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, UUID):
#             # if the obj is uuid, we simply return the value of uuid
#             return obj.hex
#         return json.JSONEncoder.default(self, obj)


# def JSONEncode
@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    # this gives the id i need: instance.profile.id
    # need to be serialized
    user_profile = Profile.objects.get(id=instance.profile.id)
    print("!!!!!!!!!!!!!!!!!!!!!!!!", user_profile.id)
    serializer = ProfileSerializer(user_profile)

    print("@@@@@@@@@ Serializer data",serializer.data)

    print("%%%%%%%%%%% Serialzer", serializer)
    profile_id = instance.profile.id
    profile_id_str = str(profile_id)
    users_username = user_profile.user.username
    data = {'profile_id': profile_id_str,
            "users_username": users_username}
    uuid_str = str(data)
    dict = ast.literal_eval(uuid_str)

    print(instance.profile)
    publish('profile_created', serializer.data)

    logger.info(f"{instance}'s profile created {dict}")
