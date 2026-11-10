"""
Enrutador principal de URLs para game_backend.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Personalización del encabezado del Django Admin
admin.site.site_header = "Dashboard ISO & Compliance - Administración del Videojuego"
admin.site.site_title = "Admin Portal - ISO Game"
admin.site.index_title = "Panel de Control y Analítica Global"

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from core.views import custom_login_view, custom_logout_view

urlpatterns = [
    path('admin/login/', custom_login_view, name='admin_login'),
    path('admin/logout/', custom_logout_view, name='admin_logout'),
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
