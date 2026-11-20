from django.contrib import admin
from django.urls import path

from portal import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("invoices/", views.invoice_list, name="invoice-list"),
]
