import os
from django.contrib.auth.models import update_last_login

from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from apps.manage_user.controller.serializers.utils import google
from apps.manage_user.controller.serializers.utils.register_google import \
    register_social_user
from user_management.settings.base import env

User = get_user_model()

class GoogleSocialAuthSerializer(serializers.Serializer):
    token = serializers.CharField()#auth_token
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate_token(self, token):#auth_token
        user_data = google.Google.validate(token)#auth_token
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != env ("GOOGLE_CLIENT_ID"):
            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'
        first_name = user_data['given_name']
        last_name = user_data['family_name']

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name,
            first_name=first_name, last_name=last_name)

class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)

        filtered_user_by_email = User.objects.filter(email=email)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if user is None:
            raise serializers.ValidationError(
                'An user with this email and password is not found.'
            )

        return {
            'email':user.email
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
