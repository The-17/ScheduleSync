from rest_framework import serializers
from .models import User


PROVIDER_CHOICES = (
        ("google", "Google")
    )

class SocialAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField()
    provider = serializers.ChoiceField(choices=PROVIDER_CHOICES)


class SocialAuthResponseSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    avatar = serializers.URLField(read_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)