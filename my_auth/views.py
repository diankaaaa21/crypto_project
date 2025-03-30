from django.contrib.auth import authenticate, login, logout
from django.db.utils import IntegrityError
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializator import LoginSerializer, RegisterSerializer


class StartView(APIView):
    def get(self, request):
        return render(request, "my_auth/startpage.html")


class Register(APIView):
    def get(self, request):
        return render(request, "my_auth/registration.html")

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            first_name = serializer.validated_data["first_name"]
            phone_number = serializer.validated_data["phone_number"]
            password = serializer.validated_data["password"]
            try:
                user = CustomUser.objects.create_user(
                    phone_number=phone_number, first_name=first_name, password=password
                )
                return self._set_tokens(user)
            except IntegrityError:
                return render(
                    request,
                    "my_auth/registration.html",
                    {"error": "Phone number already exist"},
                )

        return render(
            request, "my_auth/registration.html", {"errors": serializer.errors}
        )


class LoginView(APIView):
    def get(self, request):
        return render(request, "my_auth/login.html")

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            password = serializer.validated_data["password"]
            user = authenticate(phone_number=phone_number, password=password)
            if not user:
                return render(
                    request, "my_auth/login.html", {"error": "User doesn't exist"}
                )
            login(request, user)
            return self._set_tokens(user)
        return render(request, "my_auth/login.html", {"errors": serializer.errors})

    def _set_tokens(self, user):
        """Генерирует и сохраняет JWT-токены в cookies"""
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = redirect("crypto_app/trades/")
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="Lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
        )
        return response

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        response = redirect("/login/")
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
