from django.urls import path
from apps.booking.views.views_reviews import (
    ReviewsListDetailView,
    ReviewsCreateView,
)


urlpatterns = [
    path('list', view=ReviewsListDetailView.as_view(), name='list-detail-reviews'),
    path('create/<int:pk>', view=ReviewsCreateView.as_view(), name='create-reviews')
]