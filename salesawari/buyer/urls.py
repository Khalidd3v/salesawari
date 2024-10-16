from django.urls import path
from .views import *

urlpatterns = [
    path("dashboard/", buyer_dashboard, name="buyer_dashboard"),
    path("profile/", buyer_profile, name="buyer_profile"),
    path('chats/', buyer_chat_list_view, name='buyer_chat_list'),
    path('my-fav-vehicles/', fav_vehicles, name='fav_vehicles'),
    path('conversation/<int:user_id>/', buyer_conversation_view, name='buyer_conversation'),
    path('bargain/<int:vehicle_id>/', bargain, name='bargain'),
    path('my-orders', my_orders, name='my_orders'),
    path('invoice/<int:order_id>/', invoice, name='invoice'),

]