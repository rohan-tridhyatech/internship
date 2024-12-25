# myapp/serializers.py
from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'contact', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

