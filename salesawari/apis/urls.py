from django.urls import path
from .views import *

urlpatterns = [
     path('favorite-vehicle/', FavouriteVehicleToggleView.as_view()),
     path('send_message/', SendMessageView.as_view(), name='send_message'),
     path('fetch_messages/', FetchMessagesView.as_view(), name='fetch_messages'),
]
