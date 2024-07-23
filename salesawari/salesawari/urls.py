from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('landingpage.urls')),
    path('accounts/', include('accounts.urls')),
    path('seller/', include('seller.urls')),
    path('buyer/', include('buyer.urls')),
    path('dashboard/', include('dashboard.urls'))
]
