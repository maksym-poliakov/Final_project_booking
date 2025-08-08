from rest_framework import serializers
from django.db.models.signals import pre_save
from django.dispatch import receiver
from apps.booking.models.models_booking import BookingModel
from datetime import timedelta
from django.utils import timezone


prev_start_date = {}
@receiver(pre_save,sender=BookingModel)
def pre_save_start_data(sender,instance,**kwargs):
    try:
        old_start_date = BookingModel.objects.get(pk=instance.pk)
        role = old_start_date.housing_details.address.user.role
        prev_start_date[instance.pk] = old_start_date.start_date
    except sender.DoesNotExist:
        prev_start_date[instance.pk] = None

    if prev_start_date[instance.pk] is not None and not role == 'L':
        current_data = timezone.now().date()
        time_difference = prev_start_date[instance.pk] - current_data
        timedelta_days = timedelta(days=2)
        if time_difference < timedelta_days:
            raise serializers.ValidationError(
                {'message': f'Cannot edit booking with less than {timedelta_days.days} day remaining.'})


