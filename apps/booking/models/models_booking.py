from django.core.validators import MinValueValidator
from django.db import models

from apps.user.models.models import UserProfileModel
from apps.booking.models.models_habitation import HabitationModel
from apps.booking.choices.booking_choices import (
    CHOICES_IS_ACTIVE,
    CHOICES_CONFIRMATION,
    CHOICES_STATUS_ORDER
)


class BookingModel(models.Model):
    user = models.ForeignKey(UserProfileModel,on_delete=models.CASCADE,related_name='bookings')
    housing_details = models.ForeignKey(HabitationModel,on_delete=models.CASCADE,related_name='housing_detail_booking')
    is_active = models.CharField(choices=CHOICES_IS_ACTIVE,default=True)
    start_date = models.DateField()
    end_date = models.DateField()
    confirmation = models.CharField(choices=CHOICES_CONFIRMATION,default='awaiting')
    status_order = models.CharField(choices=CHOICES_STATUS_ORDER,null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user_id} {self.housing_details}  {self.is_active}'


    class Meta:
        db_table = 'booking'

