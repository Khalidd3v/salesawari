from django.urls import path
from .views import *
urlpatterns = [
    path("buyer-dashboard/", buyer_dashboard, name="buyer_dashboard"),
    path("buyer-profile/", buyer_profile, name="buyer_profile"),
]