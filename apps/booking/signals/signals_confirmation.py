from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from apps.booking.models.models_booking import BookingModel


pre_confirmation = {}
@receiver(pre_save,sender=BookingModel)
def pre_save_confirmation(sender,instance,**kwargs):
    try:
        old_confirmation = BookingModel.objects.get(pk=instance.pk)
        pre_confirmation[instance.pk] = old_confirmation.confirmation
    except sender.DoesNotExist:
        pre_confirmation[instance.pk] = None


@receiver(post_save,sender=BookingModel)
def post_save_confirmation(sender,instance,created,**kwargs):
    current_confirmation = instance.confirmation
    previous_confirmation = pre_confirmation.get(instance.pk)
    if not created and pre_confirmation is not None and current_confirmation != previous_confirmation:
        try:
            start_date = instance.start_date
            end_date = instance.end_date
            owner = instance.housing_details.address.user.user
            bookings_confirmation = BookingModel.objects.filter(housing_details__address__user__user=owner,start_date__lte=end_date,
                                                end_date__gte=start_date ).exclude(confirmation='confirmed')
            if bookings_confirmation.exists():
                bookings_confirmation.update(confirmation='rejected')
            bookings_status_order = BookingModel.objects.filter(housing_details__address__user__user=owner,start_date__lte=end_date,
                                                end_date__gte=start_date,confirmation='confirmed')
            if bookings_status_order.exists():
                bookings_status_order.update(status_order='active')
        except ObjectDoesNotExist:
            raise ValidationError('User profile not found')


