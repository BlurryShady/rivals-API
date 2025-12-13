from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from marvel_rivals.health import health_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_view),
    path('api/', include('heroes.urls')),
    path('api/', include('teams.urls')),
    path('api/auth/', include('accounts.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
