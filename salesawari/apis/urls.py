from django.urls import path
from .views import *

urlpatterns = [
     path('favorite-vehicle/', FavouriteVehicleToggleView.as_view()),
]
