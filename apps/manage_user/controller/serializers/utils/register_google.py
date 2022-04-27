
import os
import random

from django.contrib.auth import authenticate, get_user_model
from rest_framework.exceptions import AuthenticationFailed
from apps.profiles.producer import RabbitMq

User=get_user_model()

def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name, first_name, last_name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                email=email, password=os.environ.get('SOCIAL_SECRET'))

            publish_data = {
                'username': registered_user.username,
                "logged_status": "True"
            }

            print("Google Login-status is being shared", registered_user)
            registered_user.is_signed = True
            registered_user.save()
            p = RabbitMq()

            RabbitMq.publish(p, 'user_signed', publish_data)
            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'access_token': registered_user.tokens()['access'],
                'refresh_token': registered_user.tokens()['refresh']
            }

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'username': generate_username(name), 'email': email,
            'password': os.environ.get('SOCIAL_SECRET'),
            'first_name': first_name,
            'last_name': last_name
        }
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()
        new_user = authenticate(
            email=email, password=os.environ.get('SOCIAL_SECRET'))

        publish_data = {
            'username': new_user.username,
        }
        RabbitMq.publish(p, 'profile_created', publish_data)

        return {
            'email': new_user.email,
            'username': new_user.username,
            'tokens': new_user.tokens()
        }
