from django.urls import path
from .views import *


urlpatterns = [
    path('register-account/', register_user, name="register_user"),
    path('login-account/', login_user, name="login_user"),
    path('seller-registration/', seller_registration, name="seller_registration"),
    path('buyer-registration/', buyer_registration, name="buyer_registration"),
    path('seller-login/', seller_login, name="seller_login"),
]
