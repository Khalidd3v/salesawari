from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *


urlpatterns = [
    path('register-account/', register_user, name="register_user"),
    path('login-account/', login_user, name="login_user"),
    path('seller-registration/', seller_registration, name="seller_registration"),
    path('buyer-registration/', buyer_registration, name="buyer_registration"),
    path('seller-login/', seller_login, name="seller_login"),
    path('buyer-login/', buyer_login, name="buyer_login"),
    path('logout/', LogoutView.as_view(next_page='homepage'), name='logout'),
    path('login-superuser/', superuser_login_view, name='login_superuser'),
]
