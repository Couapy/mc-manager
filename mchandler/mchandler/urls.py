from django.conf import settings
from django.conf.urls.static import static
# from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('main.urls')),
    path('', include("social_django.urls", namespace="social")),
    path('', views.index),
] + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
) + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
