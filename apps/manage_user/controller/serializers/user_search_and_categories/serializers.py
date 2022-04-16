from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework import serializers

User = get_user_model()


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

class UserFilterByID(filters.FilterSet):
    pk = filters.CharFilter(field_name="pk")

    class Meta:
        model = User
        fields = [
            "pk"
        ]
