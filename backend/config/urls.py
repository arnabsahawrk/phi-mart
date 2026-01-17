from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import api_root_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", api_root_view),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/", include("api.urls"), name="api-root"),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
