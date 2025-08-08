from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.urls import path
from apps.user.views.views_auth_user import (
    LoginView,
    RegistrationView,
    LogoutView,
)
from apps.user.views.views_user import UserProfileDetailView,UserListCreateView


urlpatterns = [
    path('api/token/', view=TokenObtainPairView.as_view(), name='token-obtain'),
    path('api/token/refresh/', view=TokenRefreshView.as_view(), name='token-refresh'),
    path('login/', view=LoginView.as_view(), name='user-login'),
    path('registration/', view=RegistrationView.as_view(), name='user-registration'),
    path('logout/', view=LogoutView.as_view(), name='user-logout'),
    path('profiles/<int:pk>', view=UserProfileDetailView.as_view(), name='user-profile-detail'),
    path('profiles/', view=UserListCreateView.as_view(), name='users-profiles-detail'),
]