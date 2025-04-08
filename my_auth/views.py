from django.contrib.auth import login, logout
from django.db.utils import IntegrityError
from django.shortcuts import redirect, render
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import LoginSerializer, RegisterSerializer
from .throttling import LoginRateThrottle
from .utils import set_jwt_cookies


class StartView(APIView):
    def get(self, request):
        return render(request, "my_auth/startpage.html")


class RegisterView(APIView):
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
                response = redirect("/trades/")
                return set_jwt_cookies(response, user)
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
    throttle_classes = [LoginRateThrottle]

    def get(self, request):
        return render(request, "my_auth/login.html")

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            response = redirect("crypto_app/trades")
            return set_jwt_cookies(response, user)

        return render(request, "my_auth/login.html", {"errors": serializer.errors})


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        response = redirect("auth_app:startpage")
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
