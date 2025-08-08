from rest_framework_simplejwt.tokens import RefreshToken


def set_jwt_cookies(response, user):
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token

    response.set_cookie(
        key='access_token',
        value=str(access_token),
        httponly=True, secure=False, samesite='Lax'
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh),
        httponly=True, secure=False, samesite='Lax'
    )