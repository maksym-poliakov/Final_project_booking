from django.contrib import admin
from apps.user.models.models import UserProfileModel
# Register your models here.

@admin.register(UserProfileModel)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name']