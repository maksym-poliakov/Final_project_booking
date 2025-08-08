from django.utils import timezone
from django.core.cache import cache
from apps.booking.utils.start_date import get_start_date
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)

from apps.booking.models import BookingModel
from apps.booking.serializers.serializer_habitation import (
    HabitationListSerializer,
    HabitationListCreateSerializer,
    HabitationRetrieveUpdateDestroySerializer
)
from apps.booking.models.models_habitation import HabitationModel
from apps.user.models.models import UserProfileModel
from rest_framework import serializers,filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError


class HabitationListView(ListAPIView):
    queryset = HabitationModel.objects.all().select_related('address').order_by('-created_at')
    serializer_class = HabitationListSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['price','address__city','number_of_rooms','type_housing']
    search_fields = ['title','description']
    ordering_fields = ['price','created_at']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_date = get_start_date()


    def filter_queryset(self, queryset):
        if not hasattr(self.request, 'user') or not self.request.user.is_authenticated:
            return HabitationModel.objects.filter(status='A').order_by('-created_at')
        try:
            user_profile = UserProfileModel.objects.get(user=self.request.user)

            if user_profile.role == 'L':
                return super().filter_queryset(queryset)

            return queryset
        except UserProfileModel.DoesNotExist:
            raise serializers.ValidationError({'message':'User not found'})


    def get_queryset(self):
        self.update_booking_status()

        if not hasattr(self.request, 'user') or not self.request.user.is_authenticated:
            return HabitationModel.objects.filter(status='A')
        try:
            user_profile = UserProfileModel.objects.get(user=self.request.user)

            if user_profile.role == 'L':
                raise serializers.ValidationError({'message':'The landlord cannot view all ads, only his own.'})

            return  (HabitationModel.objects.filter(status='A')
                     .exclude(address__user_id=user_profile.id).order_by('-created_at'))
        except UserProfileModel.DoesNotExist:
            raise serializers.ValidationError({'message':'User not found'})


    def update_booking_status(self):
        current_data = timezone.now().date()
        start_date = cache.get('start_date', get_start_date())
        if start_date < current_data:
            bookings_to_update = BookingModel.objects.filter(
                end_date__lt=current_data,
                status_order='active',
                confirmation='confirmed'
            )
            if bookings_to_update.exists():
                bookings_to_update.update(status_order='completed')
            cache.set('start_date', current_data, timeout=None)


class HabitationListCreateView(ListCreateAPIView):
    serializer_class = HabitationListCreateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields = ['status']


    def get_queryset(self):
        try:
            user_profile = UserProfileModel.objects.get(user=self.request.user)
            queryset = HabitationModel.objects.filter(address__user__user=self.request.user)
            if user_profile.role == 'L':
                return queryset
            raise serializers.ValidationError({'message':'Only the Landlord can view'})
        except UserProfileModel.DoesNotExist:
            raise ValidationError({'message':'User not found'})


    def get_serializer_context(self):
        try:
            context = super().get_serializer_context()
            user_profile = UserProfileModel.objects.get(user=self.request.user)
            context.update({'user_profile': user_profile})
            return context
        except UserProfileModel.DoesNotExist:
            raise ValidationError({'message': 'User not found'})


    def perform_create(self, serializer):
        try :
            user_profile = UserProfileModel.objects.get(user=self.request.user)
            if not user_profile.role == 'L':
                raise serializers.ValidationError({'message': 'Only the Landlord can create'})
            serializer.save()
        except UserProfileModel.DoesNotExist:
            raise ValidationError({'message': 'User not found'})


class HabitationRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = HabitationRetrieveUpdateDestroySerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        try :
            user_profile = UserProfileModel.objects.get(user=self.request.user)
            queryset = HabitationModel.objects.filter(address__user__user=self.request.user)
            if user_profile.role == 'L':
                return queryset
            raise serializers.ValidationError({'message':'Only the Landlord can view'})
        except UserProfileModel.DoesNotExist:
            raise ValidationError({'message': 'User not found'})


    def get_serializer_context(self):
        try:
            context = super().get_serializer_context()
            user_profile = UserProfileModel.objects.filter(user=self.request.user).first()
            if not user_profile:
                raise serializers.ValidationError({"user": "User profile not found."})
            context.update({'user_profile': user_profile})
            return context
        except UserProfileModel.DoesNotExist:
            raise ValidationError({'message': 'User not found'})