from rest_framework import serializers
from .models import EmailRequest

class EmailRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailRequest
        fields = '__all__'

