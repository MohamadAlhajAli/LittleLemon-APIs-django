from djoser.serializers import UserCreateSerializer
from rest_framework import serializers


class RegistrationSerializer(UserCreateSerializer):
   
    email = serializers.EmailField(
        required=True,
        allow_blank=False,
        max_length=254,
    )