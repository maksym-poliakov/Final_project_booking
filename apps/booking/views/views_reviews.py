from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
)

from apps.booking.models import BookingModel
from apps.booking.serializers.serializer_reviews import(
    ReviewsDetailSerializer,
    ReviewsCreateSerializer,
)

from apps.booking.models.models_reviews import ReviewModel
from apps.user.permissions.user_permissions import IsTenantOrLandlord
from apps.user.models.models import UserProfileModel
from rest_framework import serializers


class ReviewsListDetailView(ListAPIView):
    queryset = ReviewModel.objects.all()
    serializer_class = ReviewsDetailSerializer


    def get_queryset(self):
        if not hasattr(self.request, 'user') or not self.request.user.is_authenticated:
            return ReviewModel.objects.all()
        try:
            user_profile = UserProfileModel.objects.get(user=self.request.user)
            if user_profile.role == 'L':
                return (ReviewModel.objects.filter(booking__housing_details__address__user=user_profile)
                        .select_related('booking__housing_details__address__user'))
            return ReviewModel.objects.all()
        except UserProfileModel.DoesNotExist:
            return ReviewModel.objects.all()


class  ReviewsCreateView(ListCreateAPIView):
    queryset = ReviewModel.objects.filter(comment='',booking__status_order='completed')
    serializer_class =  ReviewsCreateSerializer
    permission_classes = [IsTenantOrLandlord]


    def get_serializer_context(self):
        context = super().get_serializer_context()
        pk = self.kwargs.get('pk')
        if pk:
            try:
                context['booking'] = BookingModel.objects.get(id=pk)
            except BookingModel.DoesNotExist:
                raise serializers.ValidationError({'message': 'Booking does not exist'})
        return context


    def perform_create(self, serializer):
        serializer.save()


