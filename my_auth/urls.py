from django.urls import path

from .views import LoginView, LogoutView, RegisterView, StartView

app_name = "my_auth"

urlpatterns = [
    path("start/", StartView.as_view(), name="startpage"),
    path("register/", RegisterView.as_view(), name="registration"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
