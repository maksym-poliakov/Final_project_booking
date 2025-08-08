from django.contrib import admin
from apps.booking.models.models_booking import BookingModel
from apps.booking.models.models_reviews import ReviewModel
from apps.booking.models.models_address import AddressModel
from apps.booking.models.models_habitation import HabitationModel
# Register your models here.

@admin.register(BookingModel)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user_id__first_name','start_date','end_date']

@admin.register(ReviewModel)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user_id__first_name','booking_id','rating']

@admin.register(AddressModel)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['city','street','postcode','haus_number','created_at']

@admin.register(HabitationModel)
class HousingDetailAdmin(admin.ModelAdmin):
    list_display = ['title','type_housing','number_of_rooms','price']

