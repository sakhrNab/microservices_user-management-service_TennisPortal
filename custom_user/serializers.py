from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.password_validation import validate_password
from django_countries.serializer_fields import CountryField
from django_filters import rest_framework as filters
from django.core import exceptions
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from rest_framework import serializers, status
# from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed

from apps.profiles.models import Profile
from .forms import PasswordResetForm
from . import google
from .register import register_social_user
import os

# JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
# JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(source="user.username")

    # profile = UserSerializer(required=False)
    region = serializers.CharField(source="profile.region", required=False)
    zip_code = serializers.CharField(source="profile.zip_code", required=False)
    phone_number = serializers.CharField(source="profile.phone_number", required=False)
    country = serializers.CharField(source="profile.country", required=False)
    city = serializers.CharField(source="profile.city", required=False)
    age = serializers.CharField(source="profile.age", required=False)
    gender = serializers.CharField(source="profile.gender", required=False)
    skill_level = serializers.CharField(source="profile.skill_level", required=False)
    game_type = serializers.CharField(source="profile.game_type", required=False)
    address = serializers.CharField(source="profile.address", required=False)
    address_2 = serializers.CharField(source="profile.address_2", required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name',
        'region', 'zip_code','phone_number', 'gender', 'country', 'city', 'age', 'skill_level', 'game_type', 'address', 'address_2')

        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone_number': {'required': False},
            'zip_code': {'required': False},
            'gender': {'required': False},
            # 'country': {'required': True},
            # 'city': {'required': True},
            # 'region': {'required': False},
            # 'age': {'required': False},
            # 'skill_level': {'required': False},
            # 'game_type': {'required': False},
        }

    def validate(self, attrs):
        password = attrs['password']
        errors = dict() 
        try:
            # validate the password and catch the exception
            validate_password(password=password, user=User)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)
        
        return attrs


    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        # def check_json_input(user_info_args):
        #     # print(validated_data.get(user_info_args), False))
        #     if len(user)
        #     if bool(validated_data['profile'].get(user_info_args)) is False:
        #             print(user_info_args, " is empty")
        #             pass
        #
        #     user.profile.user_info_args = validated_data['profile'].get(user_info_args)
        #     user.set_password(validated_data['password'])
        #     user.save()
        #     #===================================================
        #     user.profile.save()
        #     #===================================================
        #     return user
        #     # return user.profile.user_info_args


        #==================================================='region', 'zip_code','phone_number', 'gender', 'country', 'city', 'age', 'skill_level', 'game_type')
        # array = ['region', 'zip_code','phone_number', 'gender', 'country', 'city', 'age', 'skill_level', 'game_type', 'address', 'address_2']
        # check_json_input(array)
        user.profile.region = validated_data["profile"].get("region")
        user.profile.zip_code = validated_data["profile"].get("zip_code")
        user.profile.phone_number = validated_data["profile"].get("phone_number")
        user.profile.gender = validated_data["profile"].get("gender")
        user.profile.country = validated_data["profile"].get("country")
        user.profile.city = validated_data["profile"].get("city")
        user.profile.age = validated_data["profile"].get("age")
        user.profile.skill_level = validated_data["profile"].get("skill_level")
        user.profile.game_type = validated_data["profile"].get("game_type")
        user.profile.address = validated_data["profile"].get("address")
        user.profile.address_2 = validated_data["profile"].get("address_2")

        #===================================================

        # validated_data.get("phone_number")
        # validated_data['profile'].save
        user.set_password(validated_data['password'])
        user.save()
        #===================================================
        user.profile.save()
        #===================================================
        return user

    def get_cleaned_data_profile(self):
        return {
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
        }
    
    def create_profile(self, user, validated_data):
        user.first_name = self.validated_data.get("first_name")
        user.last_name = self.validated_data.get("last_name")
        user.save()

        user.profile.phone_number = self.validated_data.get("phone_number")
        user.profile.zip_code = self.validated_data.get("zip_code")
        user.profile.gender = self.validated_data.get("gender")
        user.profile.country = self.validated_data.get("country")
        user.profile.city = self.validated_data.get("city")
        user.profile.region = self.validated_data.get("region")
        user.profile.save()

    def custom_signup(self, request, user):
        self.create_profile(user, self.get_cleaned_data_profile())


# class UserLoginSerializer(serializers.Serializer):
#
#     email = serializers.CharField(max_length=255)
#     password = serializers.CharField(max_length=128, write_only=True)
#     token = serializers.CharField(max_length=255, read_only=True)
#
#     def validate(self, data):
#         email = data.get("email", None)
#         password = data.get("password", None)
#         user = authenticate(email=email, password=password)
#
#         filtered_user_by_email = User.objects.filter(email=email)
#
#         if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
#             raise AuthenticationFailed(
#                 detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)
#
#         if user is None:
#             raise serializers.ValidationError(
#                 'An user with this email and password is not found.'
#             )
#         try:
#             payload = JWT_PAYLOAD_HANDLER(user)
#             jwt_token = JWT_ENCODE_HANDLER(payload)
#             update_last_login(None, user)
#         except User.DoesNotExist:
#             raise serializers.ValidationError(
#                 'User with given email and password does not exists'
#             )
#         return {
#             'email':user.email,
#             'token': jwt_token
#         }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = getattr(
            settings, "OLD_PASSWORD_FIELD_ENABLED", False
        )
        self.logout_on_password_change = getattr(
            settings, "LOGOUT_ON_PASSWORD_CHANGE", False
        )
        super(ChangePasswordSerializer, self).__init__(*args, **kwargs)

        self.request = self.context.get("request")
        self.user = getattr(self.request, "user", None)

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value),
        )

        if all(invalid_password_conditions):
            raise serializers.ValidationError("Invalid password")
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        old_password_match = (
            self.user,
            attrs["old_password"] == attrs["new_password1"],
        )

        if all(old_password_match):
            raise serializers.ValidationError(
                "your new password matching with old password"
            )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash

            update_session_auth_hash(self.request, self.user)


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
        print(user.pk, instance.pk)

        if user.pkid != instance.pk:
            raise serializers.ValidationError({"authorize": "You do not have permission for this user."})

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()

        return instance


# class LogoutSerializer(serializers.Serializer):
#     refresh = serializers.CharField()
#
#     def validate(self, attrs):
#         self.token = attrs['refresh']
#         return attrs
#
#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh_token"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#
#             return Response(status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def get_email_options(self):
        return {
            
        }

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        if not User.objects.filter(email=value).exists(): 
            raise serializers.ValidationError(_('Invalid e-mail address'))
            
        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)



class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()

    set_password_form_class = SetPasswordForm

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        self._errors = {}

        # Decode the uidb64 to uid to get User object
        try:
            uid = force_text(uid_decoder(attrs['uid']))
            self.user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        return attrs

    def save(self):
        return self.set_password_form.save()


class ProfileAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('available',)

    
    def update(self, instance, validated_data): 
        if not validated_data.get('available', instance.available):
            print('ok')
            instance.available = False
        else:
            instance.available = validated_data.get('available', instance.available)
        instance.save()
        return instance


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('favorite_players',)


class UserFilter(filters.FilterSet):
    username = filters.CharFilter(field_name="username", lookup_expr='icontains')
    last_name = filters.CharFilter(field_name="last_name", lookup_expr='icontains')
    profile__region = filters.CharFilter(field_name="profile__region", lookup_expr='icontains')
    first_name = filters.CharFilter(field_name="first_name", lookup_expr='icontains')
    region = filters.CharFilter(field_name="profile__region", lookup_expr='icontains')
    age = filters.CharFilter(field_name="profile__age")
    skill_level = filters.CharFilter(field_name="profile__skill_level")
    skill_level = filters.CharFilter(field_name="profile__country")
    profile__rating = filters.CharFilter(field_name="profile__rating")

    class Meta:
        model = User
        fields = [
            "username", 'first_name', 'last_name', 'profile__country', 'profile__region', 'profile__age', 'profile__skill_level', 'profile__rating'
        ]


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):

            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)

class UserFilterByID(filters.FilterSet):
    pk = filters.CharFilter(field_name="pk")
    
    class Meta:
        model = User
        fields = [
            "pk"
        ]