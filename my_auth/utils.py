from rest_framework_simplejwt.tokens import RefreshToken


def set_jwt_cookies(response, user):
    refresh = RefreshToken.for_user(user)
    response.set_cookie(
        key="access_token",
        value=str(refresh.access_token),
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=3600,
    )
    response.set_cookie(
        key="refresh_token",
        value=str(refresh),
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=3600,
    )
    return response
