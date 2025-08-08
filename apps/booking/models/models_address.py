from django.db import models
from apps.user.models.models import UserProfileModel


class AddressModel(models.Model):
    user = models.ForeignKey(UserProfileModel, on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    postcode = models.CharField(max_length=12)
    haus_number = models.PositiveSmallIntegerField()
    house_letter = models.CharField(max_length=1,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.city} {self.street} {self.postcode} {self.haus_number}'


    class Meta:
        db_table = 'address'