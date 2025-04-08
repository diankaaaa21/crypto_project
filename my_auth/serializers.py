from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["phone_number", "first_name", "password"]
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 8},
            "first_name": {"required": False, "default": ""},
        }

    def validate_phone_number(self, value):
        if CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        user = authenticate(
            phone_number=data["phone_number"], password=data["password"]
        )
        if not user:
            raise serializers.ValidationError(
                "Invalid phone number or your is not registered."
            )
        data["user"] = user
        return data
