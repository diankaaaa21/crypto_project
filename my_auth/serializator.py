from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

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
        phone_number = data.get("phone_number")
        password = data.get("password")

        user = authenticate(phone_number=phone_number, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credential")
        return data

        # class CustomTokenSerializer(serializers.ModelSerializer):
        #     username = serializers.CharField()
        #     phone_number = serializers.CharField()
        #     password = serializers.CharField()
        #
        #     def validate(self, data):
        #         username = data.get('username')
        #         phone_number = data.get('phone_number')
        #         password = data.get('password')
        #
        #
        #         user = authenticate(username=username, phone_number=phone_number, password=password)
        #         if user is None:
        #             raise serializers.ValidationError("Invalid credentials")

        refresh = RefreshToken.for_user(user)
        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }
