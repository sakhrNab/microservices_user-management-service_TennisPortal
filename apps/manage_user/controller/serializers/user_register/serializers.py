from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core import exceptions

User = get_user_model()


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

        user.set_password(validated_data['password'])
        user.save()
        user.profile.save()
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

