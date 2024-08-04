from django.urls import path
from .views import *
urlpatterns = [
    path("dashboard/", buyer_dashboard, name="buyer_dashboard")
]