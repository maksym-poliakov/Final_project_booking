from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from apps.user.serializers.user_serializers import (
    UserProfileDetailSerializers,
)
from apps.user.models.models import UserProfileModel
from apps.user.permissions.user_permissions import IsUser
from rest_framework.permissions import IsAdminUser


class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfileModel.objects.all()
    serializer_class = UserProfileDetailSerializers
    permission_classes = [IsUser]


class UserListCreateView(ListCreateAPIView):
    queryset = UserProfileModel.objects.all()
    serializer_class = UserProfileDetailSerializers
    permission_classes = [IsAdminUser]

