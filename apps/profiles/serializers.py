from django_countries.serializer_fields import CountryField
from rest_framework import fields, serializers

from apps.ratings.serializers import RatingSerializer

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    full_name = serializers.SerializerMethodField(read_only=True)
    country = CountryField(name_only=True)
    reviews = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "id",
            "phone_number",
            "profile_photo",
            "about_me",
            "gender",
            "age",
            "country",
            "city",
            "region",
            "zip_code",
            "game_type",
            "skill_level",
            "rating",
            "num_reviews",
            "reviews",
            "is_opponent",
        ]

    def get_full_name(self, obj):
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"

    def get_reviews(self, obj):
        # opponent_review: in ratings.models, related_name
        reviews = obj.opponent_review.all()
        serializer = RatingSerializer(reviews, many=True)
        return serializer.data

    # because i am reviewing the opponent
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.is_opponent:
            representation["is_opponent"] = True
        return representation


class UpdateProfileSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "phone_number",
            "profile_photo",
            "about_me",
            "gender",
            "country",
            "city",
            "region",
            "zip_code",
            "game_type",
            "skill_level",
            "is_opponent",
            # maybe: is_opponent (Gesucht), is_looking (sucher)
        ]

    #validate
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.is_opponent:
            representation["is_opponent"] = True
        return representation
