from django.db import models
from django.contrib.auth.models import User

from apps.user.choices.user_choices import (
    GENDER_CHOICES,
    ANIMALS_CHOICES,
    ROLE_CHOICES,
)


class UserProfileModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone_number = models.CharField(unique=True)
    gender = models.CharField(choices=GENDER_CHOICES)
    animals = models.CharField(choices=ANIMALS_CHOICES , default='N')
    role = models.CharField(choices=ROLE_CHOICES, default='T')
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "user_profile"
        verbose_name = 'User profile'
        verbose_name_plural = 'Users profiles'
        ordering = ['-created_at']

    def __str__(self):
        return  self.user.username





