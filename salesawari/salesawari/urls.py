from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include('apis.urls')),
    path('', include('landingpage.urls')),
    path('accounts/', include('accounts.urls')),
    path('seller/', include('seller.urls')),
    path('buyer/', include('buyer.urls')),
    path('dashboard/', include('dashboard.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
