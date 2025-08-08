from django.urls import path
from apps.booking.views.views_habitation import (
    HabitationListCreateView,
    HabitationListView,
    HabitationRetrieveUpdateDestroyView,
)


urlpatterns = [
    path('detail/',view=HabitationListCreateView.as_view(), name='housing-detail'),
    path('list/',view=HabitationListView.as_view(),name='habitation-list'),
    path('create/',view=HabitationListCreateView.as_view(),name='habitation-create'),
    path('update/<int:pk>',view=HabitationRetrieveUpdateDestroyView.as_view(),name='habitation-update-destroy'),
]
