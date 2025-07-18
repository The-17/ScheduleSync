from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path("api/schema", SpectacularAPIView.as_view(), name="api_schema"),
    path("api/", SpectacularSwaggerView.as_view(url_name="api_schema")),
    path("api/",include("apps.accounts.urls")),
    path("api/", include("apps.groups.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
