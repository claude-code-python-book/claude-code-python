"""Project URLs: the admin and the API."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("bookings.urls")),
]
