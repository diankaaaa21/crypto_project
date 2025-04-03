from django.urls import path

from .views import LoginView, Register, StartView, LogoutView

app_name = "crypto_project"

urlpatterns = [
    path("start/", StartView.as_view(), name="startpage"),
    path("register/", Register.as_view(), name="registration"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout")
]
