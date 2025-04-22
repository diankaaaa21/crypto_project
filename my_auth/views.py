from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .serializers import LoginSerializer, RegisterSerializer
from .services.auth_service import create_user
from .throttling import LoginRateThrottle
from .utils import set_jwt_cookies


class StartView(APIView):
    def get(self, request):
        return render(request, "my_auth/startpage.html")


@method_decorator(csrf_protect, name="dispatch")
class RegisterView(APIView):
    def get(self, request):
        return render(request, "my_auth/registration.html")

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user, error = create_user(
                first_name=serializer.validated_data["first_name"],
                phone_number=serializer.validated_data["phone_number"],
                password=serializer.validated_data["password"],
            )

            if error:
                return render(
                    request,
                    "my_auth/registration.html",
                    {"error": {"phone_number": [error]}},
                )
            response = redirect(reverse("crypto_app:trade_html"))
            return set_jwt_cookies(response, user)
        return render(
            request, "my_auth/registration.html", {"errors": serializer.errors}
        )


@method_decorator(csrf_protect, name="dispatch")
class LoginView(APIView):
    throttle_classes = [LoginRateThrottle]

    def get(self, request):
        return render(request, "my_auth/login.html")

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            response = redirect(reverse("crypto_app:trade_html"))
            return set_jwt_cookies(response, user)

        return render(request, "my_auth/login.html", {"errors": serializer.errors})


@method_decorator(csrf_protect, name="dispatch")
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        response = redirect("my_auth:startpage")
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
