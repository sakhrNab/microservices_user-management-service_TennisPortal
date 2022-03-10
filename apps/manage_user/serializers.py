from rest_framework import serializers
from .models import User
# , UserProfile
from django.core import validators
from django.utils import timezone

from django.core.validators import EmailValidator
from rest_framework.validators import UniqueTogetherValidator
from django.utils.translation import gettext_lazy as _

class DeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(validators=[validators.validate_email],required=True)
# )
    # user_name = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        # fields = ('email', 'user_name', 'password')
        fields=[
            'id',
            'first_name',
            'last_name',
            'email',
            # 'country',
            # 'address',
            # 'address_2',
            # 'mobile_no',
            # 'zip_code',
            # 'city',
            # 'region',
            # 'age',
            # 'skill_level',
            # 'game_type',
            'password',
            # 'confirm_password',
            # 'gender',
            'date_created',
        ]
        extra_kwargs = {
            # 'email': {
            #     'validators': [
            #         EmailValidator,
            #         UniqueValidator(
            #             queryset=NewUser.objects.all(),
            #             message="This email already exist!"
            #         )
            #     ]
            # },

            'password': {'write_only': True}}

    def create(self, validated_data):

        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)


        instance.save()
        return instance


    def validate_email(self, value):
        print("#!$$$!$!$!$!!", " i am here")
        if User.objects.filter(email=value).exists():
            print("#!$$$!$!$!$!!", " i am here")
            raise serializers.ValidationError(
                _('email is a duplicate'),
                code={'invalid'}
            )
        return value

# class CustomUserProfileSerializer(serializers.ModelSerializer):
#     user_profile = CustomUserSerializer(read_only=True, many=False)
#     class Meta:
#         model = UserProfile
#         # fields = ('email', 'user_name', 'password')
#         fields= [
#             'id',
#             'user_profile',
#             'country',
#             'profile_picture',
#             'address',
#             'address_2',
#             'mobile_no',
#             'zip_code',
#             'city',
#             'region',
#             'age',
#             'skill_level',
#             'game_type',
#             'password',
#             # 'confirm_password',
#             'gender',
#             # 'date_created',
#         ]
#         def create(self, validated_data):
#             password = validated_data.pop('password', None)
#             # as long as the fields are the same, we can just use this
#             instance = self.Meta.model(**validated_data)
#             if password is not None:
#                 instance.set_password(password)
#
#             instance.save()
#             return instance
#
#
#     def validate_email(self, value):
#         print("#!$$$!$!$!$!!", " i am here")
#         if UserProfile.objects.filter(email=value).exists():
#             print("#!$$$!$!$!$!!", " i am here")
#             raise serializers.ValidationError(
#                 _('email is a duplicate'),
#                 code={'invalid'}
#             )
#         return value