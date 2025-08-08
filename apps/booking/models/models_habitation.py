from django.db import models
from django.db.models import Avg
from django.core.validators import MaxValueValidator
from apps.booking.models.models_address import AddressModel
from django.core.validators import MinValueValidator
from apps.booking.choices.habitation_choices import (
    CHOICES_HOUSING,
    CHOICES_STATUS
)


class HabitationModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    type_housing = models.CharField(choices=CHOICES_HOUSING)
    status = models.CharField(choices=CHOICES_STATUS,default='Actively')
    number_of_rooms = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    address = models.ForeignKey(AddressModel,on_delete=models.CASCADE,related_name='habitations')
    created_at = models.DateTimeField(auto_now_add=True)


    @property
    def avg_rating(self):
        return self.housing_detail_booking.aggregate(avg_rating=Avg('booking_reviews__rating'))['avg_rating'] or 0.0


    def __str__(self):
       return f'{self.title} {self.description} {self.type_housing} {self.status} {self.number_of_rooms}'


    class Meta:
        db_table = 'habitations'
        unique_together = ('title', 'description', 'type_housing', 'number_of_rooms', 'status', 'address')
