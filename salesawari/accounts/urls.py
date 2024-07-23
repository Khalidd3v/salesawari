from django.urls import path
from .views import *


urlpatterns = [
    path('register-account/', register_user, name="register_user")
]
