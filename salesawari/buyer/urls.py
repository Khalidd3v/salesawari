from django.urls import path
from .views import *

urlpatterns = [
    path("dashboard/", buyer_dashboard, name="buyer_dashboard"),
    path("profile/", buyer_profile, name="buyer_profile"),
    path('chats/', buyer_chat_list_view, name='buyer_chat_list'),  # List of conversations
    path('conversation/<int:user_id>/', buyer_conversation_view, name='buyer_conversation'),  # Chat with a seller

]