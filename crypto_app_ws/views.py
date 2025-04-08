from django.shortcuts import render


def index(request):
    return render(request, "crypto_app_ws/index.html")
