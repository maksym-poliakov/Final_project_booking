from django.urls import path
from apps.booking.views.views_booking import BookingListView,BookingRetrieveUpdateDestroyView


urlpatterns = [
    path('list/',view=BookingListView.as_view(),name='booking-list'),
    path('create/<int:pk>',view=BookingRetrieveUpdateDestroyView.as_view(),name='booking-create'),
]