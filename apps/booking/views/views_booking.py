from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from apps.booking.models.models_booking import BookingModel
from apps.booking.models.models_habitation import HabitationModel
from apps.user.models.models import UserProfileModel
from apps.booking.serializers.serializer_booking import(
    BookingListSerializer,
    BookingLandlordUpdateSerializer,
    BookingRetrieveUpdateDestroyViewSerializer,
)
from apps.user.permissions.user_permissions import IsTenantOrLandlord,IsRoleMethod
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status,serializers


class BookingListView(ListAPIView):
    queryset = BookingModel.objects.all()
    serializer_class = BookingListSerializer
    permission_classes = [IsTenantOrLandlord]

    def get_queryset(self):
        try:
            user_profile = UserProfileModel.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'message':'user not found'})
        if user_profile.role == 'L' :
            return BookingModel.objects.filter(housing_details__address__user__user=self.request.user,is_active=1,
                                               confirmation='awaiting')
        return BookingModel.objects.filter(user=user_profile).exclude(confirmation='rejected')


class BookingRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = BookingModel.objects.all()
    permission_classes = [IsRoleMethod,IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        try:
            user_profile = UserProfileModel.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'message':'user not found'})

        if user_profile.role == 'L':
            return BookingLandlordUpdateSerializer(*args, **kwargs)
        return BookingRetrieveUpdateDestroyViewSerializer(*args, **kwargs)

    def get_queryset(self):
        try:
            user_profile = UserProfileModel.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'message': 'user not found'})
        if user_profile.role == 'L':
            return BookingModel.objects.filter(housing_details__address__user__user=self.request.user, is_active=1,
                                               confirmation='awaiting')
        return BookingModel.objects.filter(user=user_profile)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if not pk:
            return Response({'message':'pk is required'},status=status.HTTP_400_BAD_REQUEST)
        try:
            HabitationModel.objects.get(pk=pk)
        except HabitationModel.DoesNotExist:
            return Response({'message': 'Habitation not found'}, status=status.HTTP_404_NOT_FOUND)

        data = self.request.data.copy()
        data['housing_details'] = pk
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)







