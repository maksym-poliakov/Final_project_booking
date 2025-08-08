from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework import status
from apps.user.utils.set_jwt_cookies import set_jwt_cookies
from apps.user.serializers.user_serializers import (
    UserRegistrationSerializer,
)


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user_profile = serializer.save()

            response = Response({
                'user':{
                    'id': user_profile.user.id,
                    'username': user_profile.user.username,
                    'email': user_profile.user.email
                }
            }, status=status.HTTP_201_CREATED)

            set_jwt_cookies(response,user_profile.user)

            return response
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self,request,*args,**kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user:
            response = Response(f"{user}",status=status.HTTP_200_OK)

            set_jwt_cookies(response,user)

            return response

        else:
            return Response({'message':'User not found'}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:

            response = Response({'detail':'Token not found'},status=status.HTTP_400_BAD_REQUEST)
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response
        try:

            RefreshToken(refresh_token).blacklist()
            response = Response({"detail": "Successfully logged out"},status=status.HTTP_200_OK)
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response

        except TokenError as e:

            response = Response({"detail": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response