from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from apps.user.models.models import UserProfileModel
from apps.booking.models.models_booking import BookingModel


class ReviewModel(models.Model):
    user = models.ForeignKey(UserProfileModel,on_delete=models.DO_NOTHING,related_name='reviews')
    booking = models.ForeignKey(BookingModel,on_delete=models.DO_NOTHING ,related_name='booking_reviews')
    comment = models.TextField(max_length=300)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user_id} {self.booking} {self.rating}'


    class Meta:
        db_table = 'review'
